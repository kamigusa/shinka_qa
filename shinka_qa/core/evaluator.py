"""
適応度関数の実装
テストスイートの品質を多角的に評価する
"""

import subprocess
import time
import ast
import tempfile
import shutil
from typing import Dict, Tuple
from pathlib import Path


class QualityEvaluator:
    """テストスイートの品質評価クラス"""

    def __init__(
        self,
        target_module_path: Path,
        seeded_bugs_path: Path = None,
        weights: Dict[str, float] = None
    ):
        """
        Args:
            target_module_path: テスト対象モジュールのパス
            seeded_bugs_path: バグを仕込んだバージョンのパス
            weights: 各指標の重み（デフォルト: coverage=0.4, bugs=0.35, efficiency=0.15, quality=0.1）
        """
        self.target_module = Path(target_module_path)
        self.seeded_bugs = Path(seeded_bugs_path) if seeded_bugs_path else None

        # デフォルトの重み設定
        self.weights = weights or {
            'coverage': 0.4,
            'bug_detection': 0.35,
            'efficiency': 0.15,
            'maintainability': 0.1
        }

        # ベースライン値（初期テストでの測定値）
        self.baseline_coverage = 0.0
        self.baseline_time = 1.0
        self.total_seeded_bugs = 5  # デフォルト値

    def evaluate(self, test_file_path: Path) -> Tuple[float, Dict[str, float]]:
        """
        テストファイルを評価して適応度スコアを返す

        Args:
            test_file_path: 評価するテストファイルのパス

        Returns:
            (total_fitness, metrics_dict): 総合スコアと各指標の詳細
        """
        metrics = {}

        # 1. カバレッジ測定
        metrics['coverage'] = self._measure_coverage(test_file_path)
        metrics['coverage_improvement'] = self._calculate_coverage_improvement(
            metrics['coverage']
        )

        # 2. バグ検出率測定
        metrics['bugs_detected'] = self._measure_bug_detection(test_file_path)

        # 3. 実行効率測定
        metrics['execution_time'], metrics['efficiency'] = self._measure_efficiency(
            test_file_path
        )

        # 4. コード品質測定
        metrics['maintainability'] = self._measure_code_quality(test_file_path)

        # 5. 総合スコア計算
        fitness = (
            self.weights['coverage'] * metrics['coverage_improvement'] +
            self.weights['bug_detection'] * metrics['bugs_detected'] +
            self.weights['efficiency'] * metrics['efficiency'] +
            self.weights['maintainability'] * metrics['maintainability']
        )

        return fitness, metrics

    def _measure_coverage(self, test_file: Path) -> float:
        """pytest-covを使用してカバレッジを測定"""
        # EVOLVE-BLOCK-START: coverage_measurement
        try:
            # pytest-covを使用してカバレッジを測定
            result = subprocess.run(
                [
                    'pytest',
                    str(test_file),
                    f'--cov={self.target_module.stem}',
                    '--cov-report=term-missing',
                    '--tb=short',
                    '-v'
                ],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(self.target_module.parent)
            )

            # カバレッジ結果を解析
            output = result.stdout + result.stderr

            # "TOTAL" 行からカバレッジパーセンテージを抽出
            for line in output.split('\n'):
                if 'TOTAL' in line or self.target_module.stem in line:
                    parts = line.split()
                    for part in parts:
                        if '%' in part:
                            try:
                                coverage_percentage = float(part.rstrip('%'))
                                return coverage_percentage
                            except ValueError:
                                continue

            # カバレッジ情報が見つからない場合は0を返す
            return 0.0

        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"Coverage measurement error: {e}")
            return 0.0
        # EVOLVE-BLOCK-END

    def _calculate_coverage_improvement(self, current_coverage: float) -> float:
        """ベースラインからのカバレッジ改善率を計算"""
        if self.baseline_coverage >= 100:
            return 0.0

        improvement = (
            (current_coverage - self.baseline_coverage) /
            (100 - self.baseline_coverage)
        )
        return max(0.0, min(1.0, improvement))  # 0-1に正規化

    def _measure_bug_detection(self, test_file: Path) -> float:
        """バグ検出率を測定"""
        if not self.seeded_bugs or not self.seeded_bugs.exists():
            # バグファイルがない場合はスキップ
            return 0.0

        # EVOLVE-BLOCK-START: bug_detection
        try:
            # 一時ディレクトリを作成してバグ版をコピー
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)

                # バグ版モジュールをコピー
                buggy_module = tmp_path / self.target_module.name
                shutil.copy(self.seeded_bugs, buggy_module)

                # テストファイルをコピー
                tmp_test = tmp_path / test_file.name
                shutil.copy(test_file, tmp_test)

                # バグを仕込んだバージョンに対してテストを実行
                result = subprocess.run(
                    ['pytest', str(tmp_test), '-v', '--tb=short'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(tmp_path)
                )

                # 失敗したテストの数をカウント（= 検出されたバグ）
                output = result.stdout + result.stderr

                # "FAILED" または "ERROR" の数をカウント
                failures = output.count('FAILED') + output.count('ERROR')

                detection_rate = min(1.0, failures / self.total_seeded_bugs)
                return detection_rate

        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"Bug detection error: {e}")
            return 0.0
        # EVOLVE-BLOCK-END

    def _measure_efficiency(self, test_file: Path) -> Tuple[float, float]:
        """テスト実行時間を測定"""
        start_time = time.time()

        try:
            result = subprocess.run(
                ['pytest', str(test_file), '-v', '--quiet'],
                capture_output=True,
                timeout=10,
                cwd=str(self.target_module.parent)
            )
        except subprocess.TimeoutExpired:
            return 10.0, 0.0

        execution_time = time.time() - start_time

        # 効率スコア: 速いほど高スコア
        efficiency = self.baseline_time / max(execution_time, 0.1)

        # 5秒以上かかる場合はペナルティ
        if execution_time > 5.0:
            efficiency *= 0.5

        return execution_time, min(1.0, efficiency)

    def _measure_code_quality(self, test_file: Path) -> float:
        """テストコードの品質を測定"""
        # EVOLVE-BLOCK-START: code_quality
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                code = f.read()

            tree = ast.parse(code)

            # 品質指標を収集
            total_assertions = 0
            quality_assertions = 0
            test_functions = 0
            total_complexity = 0

            for node in ast.walk(tree):
                # テスト関数を検出
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_functions += 1

                    # 複雑度を簡易計算（if/for/while文の数）
                    complexity = sum(
                        1 for n in ast.walk(node)
                        if isinstance(n, (ast.If, ast.For, ast.While))
                    )
                    total_complexity += complexity

                    # アサーションを検出
                    for stmt in ast.walk(node):
                        if isinstance(stmt, ast.Assert):
                            total_assertions += 1
                            # 品質の高いアサーション（比較演算を含む）
                            if isinstance(stmt.test, ast.Compare):
                                quality_assertions += 1

            # 指標を計算
            assertion_quality = (
                quality_assertions / total_assertions
                if total_assertions > 0 else 0.5
            )

            avg_complexity = (
                total_complexity / test_functions
                if test_functions > 0 else 0
            )
            complexity_score = 1.0 if avg_complexity < 5 else 0.5

            # 独立性スコア（グローバル変数の使用を検出）
            global_vars = sum(
                1 for node in ast.walk(tree)
                if isinstance(node, ast.Global)
            )
            independence = 1.0 if global_vars == 0 else 0.5

            quality_score = (
                0.4 * assertion_quality +
                0.3 * independence +
                0.3 * complexity_score
            )
            return quality_score

        except Exception as e:
            print(f"Code quality measurement error: {e}")
            return 0.5
        # EVOLVE-BLOCK-END

    def set_baseline(self, initial_test_file: Path):
        """初期テストでベースライン値を設定"""
        self.baseline_coverage = self._measure_coverage(initial_test_file)
        self.baseline_time, _ = self._measure_efficiency(initial_test_file)

        print(f"Baseline set: Coverage={self.baseline_coverage:.1f}%, Time={self.baseline_time:.2f}s")
