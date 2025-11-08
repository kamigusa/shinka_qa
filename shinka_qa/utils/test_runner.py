"""
pytest実行ラッパー
テストの実行と結果の解析を行う
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class TestRunner:
    """pytestテスト実行ラッパークラス"""

    def __init__(self, timeout: int = 10):
        """
        Args:
            timeout: テスト実行のタイムアウト（秒）
        """
        self.timeout = timeout

    def run_tests(self, test_file: Path, target_dir: Path = None) -> Dict[str, any]:
        """
        テストを実行して結果を返す

        Args:
            test_file: テストファイルのパス
            target_dir: 実行ディレクトリ（Noneの場合はテストファイルの親ディレクトリ）

        Returns:
            テスト実行結果の辞書
        """
        if target_dir is None:
            target_dir = test_file.parent

        try:
            result = subprocess.run(
                ['pytest', str(test_file), '-v', '--tb=short'],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=str(target_dir)
            )

            return self._parse_result(result)

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'timeout': True,
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'output': 'Test execution timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'output': str(e)
            }

    def run_with_coverage(
        self,
        test_file: Path,
        module_name: str,
        target_dir: Path = None
    ) -> Dict[str, any]:
        """
        カバレッジ測定付きでテストを実行

        Args:
            test_file: テストファイルのパス
            module_name: カバレッジ対象モジュール名
            target_dir: 実行ディレクトリ

        Returns:
            テスト実行結果とカバレッジ情報の辞書
        """
        if target_dir is None:
            target_dir = test_file.parent

        try:
            result = subprocess.run(
                [
                    'pytest',
                    str(test_file),
                    f'--cov={module_name}',
                    '--cov-report=term-missing',
                    '-v'
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=str(target_dir)
            )

            parsed = self._parse_result(result)
            parsed['coverage'] = self._parse_coverage(result.stdout + result.stderr)

            return parsed

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'timeout': True,
                'coverage': 0.0,
                'output': 'Test execution timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'coverage': 0.0,
                'output': str(e)
            }

    def _parse_result(self, result: subprocess.CompletedProcess) -> Dict[str, any]:
        """pytestの実行結果を解析"""
        output = result.stdout + result.stderr

        # テスト結果のカウント
        passed = output.count(' PASSED')
        failed = output.count(' FAILED')
        errors = output.count(' ERROR')

        success = result.returncode == 0

        return {
            'success': success,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'output': output,
            'return_code': result.returncode
        }

    def _parse_coverage(self, output: str) -> float:
        """カバレッジ情報を解析"""
        # "TOTAL" 行または モジュール名の行からカバレッジを抽出
        for line in output.split('\n'):
            if 'TOTAL' in line or '%' in line:
                parts = line.split()
                for part in parts:
                    if '%' in part:
                        try:
                            return float(part.rstrip('%'))
                        except ValueError:
                            continue

        return 0.0

    def validate_test_file(self, test_file: Path) -> Tuple[bool, str]:
        """
        テストファイルの妥当性を検証

        Args:
            test_file: 検証するテストファイル

        Returns:
            (is_valid, error_message)
        """
        if not test_file.exists():
            return False, f"Test file not found: {test_file}"

        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 基本的な検証
            if 'def test_' not in content and 'class Test' not in content:
                return False, "No test functions or classes found"

            # 構文チェック
            compile(content, str(test_file), 'exec')

            return True, ""

        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
