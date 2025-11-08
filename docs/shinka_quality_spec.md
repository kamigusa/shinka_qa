# Shinka Quality - Project Specification v1.0

## プロジェクト概要

### 目的
ShinkaEvolveをフォークし、ソフトウェア品質改善に特化したツール「Shinka Quality」を開発する。
テストコードとテスト戦略を進化させ、テストカバレッジとバグ検出率を自動的に向上させる。

### ターゲットユーザー
- ソフトウェアエンジニア（特にPython開発者）
- QAエンジニア
- テックリード・CTOなどの技術マネージャー

### コアバリュープロポジション
「テストコードを書く時間を削減しながら、品質を向上させる」

---

## スモールサンプル仕様（MVP）

### 対象
単一のPythonモジュール（関数5-10個程度）に対するpytestテストスイートの自動生成・最適化

### 入力
1. **テスト対象ファイル**: `target_module.py`（ユーザーが提供）
2. **初期テストファイル**: `test_target_module_initial.py`（基本的なテンプレート）
3. **設定ファイル**: `quality_config.yaml`

### 出力
1. **最適化されたテストファイル**: `test_target_module_evolved.py`
2. **進化レポート**: カバレッジ・バグ検出の推移を可視化
3. **発見された洞察**: どのテスト戦略が有効だったか

---

## 適応度関数の設計

### 複合スコア計算式

```python
fitness_score = (
    coverage_weight * coverage_improvement +
    bug_detection_weight * bugs_found +
    efficiency_weight * (1 / execution_time) +
    maintainability_weight * code_quality_score
)
```

### 各指標の詳細

#### 1. テストカバレッジ (coverage_improvement)
```python
# coverage.py または pytest-cov を使用
coverage_improvement = (new_coverage - baseline_coverage) / (100 - baseline_coverage)

# 測定項目
- Statement Coverage (行カバレッジ)
- Branch Coverage (分岐カバレッジ)
- Function Coverage (関数カバレッジ)
```

**重み**: 40%

#### 2. バグ検出率 (bugs_found)
```python
# 事前に仕込んだバグを検出できたか
bugs_found = detected_bugs / total_seeded_bugs

# バグシードの種類
- Off-by-one errors
- Null/None handling
- Type errors
- Edge cases (empty list, negative numbers, etc.)
- Boundary conditions
```

**重み**: 35%

#### 3. 実行効率 (execution_time)
```python
# テストスイート全体の実行時間
efficiency_score = baseline_time / current_time

# ペナルティ: 5秒以上かかる場合はスコアを減算
if current_time > 5.0:
    efficiency_score *= 0.5
```

**重み**: 15%

#### 4. 保守性 (code_quality_score)
```python
# テストコードの品質指標
code_quality_score = (
    0.4 * assertion_quality +      # 適切なアサーションを使用
    0.3 * test_independence +      # テスト間の独立性
    0.3 * readability              # 可読性（行数、複雑度）
)

# assertion_quality: assert True/False を避け、具体的なアサーションを使用
# test_independence: グローバル状態への依存を最小化
# readability: McCabe複雑度 < 10、1テスト関数 < 50行
```

**重み**: 10%

---

## プロジェクト構造

```
shinka-qa/
├── README.md
├── pyproject.toml
├── setup.py
├── shinka_qa/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── evaluator.py          # 適応度関数の実装
│   │   ├── coverage_analyzer.py  # カバレッジ測定
│   │   ├── bug_detector.py       # バグ検出システム
│   │   └── quality_metrics.py    # コード品質測定
│   ├── evolution/
│   │   ├── __init__.py
│   │   ├── test_mutator.py       # テストコード変異オペレータ
│   │   └── archive_manager.py    # ShinkaEvolveから継承
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── ast_parser.py         # ASTベースのコード解析
│   │   └── test_runner.py        # pytest実行ラッパー
│   └── cli/
│       ├── __init__.py
│       └── main.py                # CLIエントリーポイント
├── examples/
│   ├── simple_calculator/
│   │   ├── calculator.py          # テスト対象コード
│   │   ├── test_calculator_initial.py
│   │   └── quality_config.yaml
│   └── string_processor/
│       ├── processor.py
│       ├── test_processor_initial.py
│       └── quality_config.yaml
├── tests/
│   └── test_shinka_qa.py
└── docs/
    ├── getting_started.md
    └── api_reference.md
```

---

## 実装の核心ロジック

### 1. evaluator.py - 適応度関数

```python
"""
適応度関数の実装
テストスイートの品質を多角的に評価する
"""

import subprocess
import time
from typing import Dict, Tuple
from pathlib import Path
import coverage
import ast


class QualityEvaluator:
    """テストスイートの品質評価クラス"""
    
    def __init__(
        self,
        target_module_path: Path,
        seeded_bugs_path: Path,
        weights: Dict[str, float] = None
    ):
        """
        Args:
            target_module_path: テスト対象モジュールのパス
            seeded_bugs_path: バグを仕込んだバージョンのパス
            weights: 各指標の重み（デフォルト: coverage=0.4, bugs=0.35, efficiency=0.15, quality=0.1）
        """
        self.target_module = target_module_path
        self.seeded_bugs = seeded_bugs_path
        
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
        cov = coverage.Coverage()
        cov.start()
        
        # pytestを実行
        result = subprocess.run(
            ['pytest', str(test_file), '-v'],
            capture_output=True,
            timeout=10
        )
        
        cov.stop()
        cov.save()
        
        # カバレッジレポートを解析
        total_statements = 0
        covered_statements = 0
        
        for filename in cov.get_data().measured_files():
            if self.target_module.name in filename:
                analysis = cov.analysis(filename)
                total_statements += len(analysis[1])  # 実行可能な文
                covered_statements += len(analysis[1]) - len(analysis[2])  # 未実行文を引く
        
        coverage_percentage = (
            (covered_statements / total_statements * 100) 
            if total_statements > 0 else 0.0
        )
        # EVOLVE-BLOCK-END
        
        return coverage_percentage
    
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
        # EVOLVE-BLOCK-START: bug_detection
        # バグを仕込んだバージョンに対してテストを実行
        result = subprocess.run(
            ['pytest', str(test_file), '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # 失敗したテストの数をカウント（= 検出されたバグ）
        output = result.stdout + result.stderr
        
        # "FAILED" または "ERROR" の数をカウント
        failures = output.count('FAILED') + output.count('ERROR')
        
        # 仕込んだバグの総数（設定ファイルから取得または固定値）
        total_seeded_bugs = 5  # この例では5つのバグを仕込む想定
        
        detection_rate = min(1.0, failures / total_seeded_bugs)
        # EVOLVE-BLOCK-END
        
        return detection_rate
    
    def _measure_efficiency(self, test_file: Path) -> Tuple[float, float]:
        """テスト実行時間を測定"""
        start_time = time.time()
        
        result = subprocess.run(
            ['pytest', str(test_file), '-v', '--quiet'],
            capture_output=True,
            timeout=10
        )
        
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
        # EVOLVE-BLOCK-END
        
        return quality_score
    
    def set_baseline(self, initial_test_file: Path):
        """初期テストでベースライン値を設定"""
        self.baseline_coverage = self._measure_coverage(initial_test_file)
        self.baseline_time, _ = self._measure_efficiency(initial_test_file)
        
        print(f"Baseline set: Coverage={self.baseline_coverage:.1f}%, Time={self.baseline_time:.2f}s")
```

### 2. test_mutator.py - テストコード変異オペレータ

```python
"""
テストコードの変異オペレータ
LLMを使用してテストコードを進化させる
"""

from typing import List, Dict
from pathlib import Path


class TestMutator:
    """テストコード変異クラス"""
    
    # LLMへのプロンプトテンプレート
    MUTATION_PROMPTS = {
        'add_edge_cases': """
以下のテストコードに、エッジケースのテストを追加してください。

考慮すべきエッジケース:
- 空の入力（空文字列、空リスト、None）
- 境界値（0, -1, 最大値、最小値）
- 無効な型（期待される型と異なる入力）
- 特殊文字（Unicode, エスケープシーケンス）

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

改善されたテストコードを出力してください。
""",
        
        'improve_assertions': """
以下のテストコードのアサーションを改善してください。

改善ポイント:
- 単純な assert True/False を具体的な比較に置き換える
- assertEqual, assertIn, assertRaises などの専用メソッドを使用
- エラーメッセージを追加して、失敗時の原因を明確にする

現在のテストコード:
```python
{current_test_code}
```

改善されたテストコードを出力してください。
""",
        
        'add_parametrize': """
以下のテストコードに pytest.mark.parametrize を使用して、
複数のテストケースを効率的に実行できるようにしてください。

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

パラメータ化されたテストコードを出力してください。
""",
        
        'add_fixtures': """
以下のテストコードに pytest fixtures を追加して、
テストのセットアップとクリーンアップを改善してください。

現在のテストコード:
```python
{current_test_code}
```

改善されたテストコード（fixtureを含む）を出力してください。
""",
        
        'add_mocks': """
以下のテストコードに unittest.mock または pytest-mock を使用して、
外部依存をモック化し、テストの独立性を向上させてください。

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

モックを使用した改善されたテストコードを出力してください。
"""
    }
    
    def __init__(self, llm_client):
        """
        Args:
            llm_client: LLMクライアント（OpenAI, Anthropic等）
        """
        self.llm = llm_client
    
    def mutate(
        self,
        test_code: str,
        target_code: str,
        strategy: str,
        context: Dict = None
    ) -> str:
        """
        テストコードを変異させる
        
        Args:
            test_code: 現在のテストコード
            target_code: テスト対象のコード
            strategy: 変異戦略（'add_edge_cases', 'improve_assertions'等）
            context: 追加コンテキスト（カバレッジ情報等）
        
        Returns:
            変異後のテストコード
        """
        # プロンプトを構築
        prompt = self._build_prompt(test_code, target_code, strategy, context)
        
        # LLMで変異を生成
        mutated_code = self._call_llm(prompt)
        
        # コードブロックを抽出（```python ... ``` を除去）
        mutated_code = self._extract_code_block(mutated_code)
        
        return mutated_code
    
    def _build_prompt(
        self,
        test_code: str,
        target_code: str,
        strategy: str,
        context: Dict
    ) -> str:
        """変異プロンプトを構築"""
        base_prompt = self.MUTATION_PROMPTS.get(strategy, self.MUTATION_PROMPTS['add_edge_cases'])
        
        prompt = base_prompt.format(
            current_test_code=test_code,
            target_function=target_code
        )
        
        # コンテキスト情報を追加
        if context and 'uncovered_lines' in context:
            prompt += f"\n\n未カバーの行: {context['uncovered_lines']}"
        
        if context and 'previous_failures' in context:
            prompt += f"\n\n以前の失敗: {context['previous_failures']}"
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """LLMを呼び出してコードを生成"""
        # EVOLVE-BLOCK-START: llm_call
        response = self.llm.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは優秀なソフトウェアテストエンジニアです。"
                               "高品質なpytestテストコードを生成してください。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        # EVOLVE-BLOCK-END
    
    def _extract_code_block(self, llm_response: str) -> str:
        """LLMの応答からコードブロックを抽出"""
        # ```python ... ``` を検出
        if '```python' in llm_response:
            start = llm_response.find('```python') + 9
            end = llm_response.find('```', start)
            return llm_response[start:end].strip()
        
        # コードブロックがない場合はそのまま返す
        return llm_response.strip()
```

---

## 設定ファイル例

### quality_config.yaml

```yaml
# Shinka Quality 設定ファイル

# テスト対象
target:
  module_path: "examples/simple_calculator/calculator.py"
  test_initial_path: "examples/simple_calculator/test_calculator_initial.py"
  seeded_bugs_path: "examples/simple_calculator/calculator_buggy.py"

# 適応度関数の重み
fitness_weights:
  coverage: 0.4          # テストカバレッジ
  bug_detection: 0.35    # バグ検出率
  efficiency: 0.15       # 実行効率
  maintainability: 0.1   # コード品質

# 進化パラメータ
evolution:
  generations: 30              # 世代数
  population_size: 20          # 各島の個体数
  num_islands: 4               # 島の数
  migration_interval: 10       # 移住間隔（世代）
  migration_rate: 0.1          # 移住率
  elite_ratio: 0.3             # エリート選択比率

# LLM設定
llm:
  provider: "openai"           # openai, anthropic, deepseek
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
  
  # UCB1パラメータ
  bandit:
    exploration_coefficient: 1.0
    models:
      - "gpt-4"
      - "gpt-4-turbo"
      - "claude-3-opus"

# 変異戦略
mutation_strategies:
  - "add_edge_cases"
  - "improve_assertions"
  - "add_parametrize"
  - "add_fixtures"
  - "add_mocks"

# 実行制限
limits:
  max_test_time: 10.0          # 単一テストの最大実行時間（秒）
  max_total_time: 300.0        # 全体の最大実行時間（秒）
  max_test_file_size: 5000     # テストファイルの最大行数

# 出力
output:
  results_dir: "results/"
  save_all_generations: true
  visualization: true
```

---

## サンプルコード：電卓モジュール

### examples/simple_calculator/calculator.py

```python
"""
簡単な電卓モジュール
Shinka Quality のテスト対象サンプル
"""

def add(a, b):
    """2つの数値を加算"""
    return a + b


def subtract(a, b):
    """2つの数値を減算"""
    return a - b


def multiply(a, b):
    """2つの数値を乗算"""
    return a * b


def divide(a, b):
    """2つの数値を除算"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base, exponent):
    """べき乗を計算"""
    if not isinstance(base, (int, float)) or not isinstance(exponent, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return base ** exponent


def factorial(n):
    """階乗を計算"""
    if not isinstance(n, int):
        raise TypeError("Argument must be an integer")
    if n < 0:
        raise ValueError("Argument must be non-negative")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n):
    """素数判定"""
    if not isinstance(n, int):
        raise TypeError("Argument must be an integer")
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

### examples/simple_calculator/test_calculator_initial.py

```python
"""
初期テストファイル（カバレッジ約40%想定）
Shinka Qualityがこれを進化させる
"""

import pytest
from calculator import add, subtract, multiply, divide, power, factorial, is_prime


def test_add_positive():
    """正の数の加算"""
    assert add(2, 3) == 5


def test_subtract_positive():
    """正の数の減算"""
    assert subtract(5, 3) == 2


def test_multiply():
    """乗算"""
    result = multiply(3, 4)
    assert result == 12


def test_divide_simple():
    """単純な除算"""
    result = divide(10, 2)
    assert result == 5.0


def test_power_simple():
    """単純なべき乗"""
    assert power(2, 3) == 8


# 以下のエッジケースは未実装
# - ゼロ除算のテスト
# - 負の数のテスト
# - 階乗のエッジケース
# - 素数判定のエッジケース
# - 型エラーのテスト
```

### examples/simple_calculator/calculator_buggy.py

```python
"""
バグを仕込んだバージョン（バグ検出率測定用）
"""

def add(a, b):
    return a + b


def subtract(a, b):
    # バグ1: 符号が逆
    return b - a  # 本来は a - b


def multiply(a, b):
    # バグ2: ゼロの扱いが間違っている
    if a == 0:
        return 1  # 本来は 0
    return a * b


def divide(a, b):
    # バグ3: ゼロチェックが不完全
    if b == 0:
        return 0  # 本来は例外を投げる
    return a / b


def power(base, exponent):
    # バグ4: 型チェックがない
    return base ** exponent  # 文字列などが渡された場合エラー


def factorial(n):
    # バグ5: 負の数のチェックがない
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result  # n < 0 の場合に無限ループ


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

---

## CLIインターフェース

### 基本的な使用方法

```bash
# インストール
git clone https://github.com/yourusername/shinka-qa.git
cd shinka-qa
pip install -e .

# 実行
shinka-qa evolve --config examples/simple_calculator/quality_config.yaml

# 結果の可視化
shinka-qa visualize --results-dir results/run_20250107_123456

# ベンチマーク比較
shinka-qa benchmark --config examples/simple_calculator/quality_config.yaml
```

### CLI引数

```python
# cli/main.py

import click
from pathlib import Path

@click.group()
def cli():
    """Shinka Quality - ソフトウェア品質改善のための進化的フレームワーク"""
    pass


@cli.command()
@click.option('--config', type=click.Path(exists=True), required=True,
              help='設定ファイルのパス')
@click.option('--output-dir', type=click.Path(), default='results/',
              help='出力ディレクトリ')
@click.option('--verbose', is_flag=True, help='詳細ログを表示')
def evolve(config, output_dir, verbose):
    """テストスイートを進化させる"""
    click.echo(f"Starting evolution with config: {config}")
    # 実装はここに


@cli.command()
@click.option('--results-dir', type=click.Path(exists=True), required=True,
              help='結果ディレクトリのパス')
@click.option('--port', default=8888, help='Webサーバーのポート')
def visualize(results_dir, port):
    """進化の結果を可視化する"""
    click.echo(f"Starting visualization server on port {port}")
    # 実装はここに


@cli.command()
@click.option('--config', type=click.Path(exists=True), required=True,
              help='設定ファイルのパス')
def benchmark(config):
    """初期テストとの性能比較を実行"""
    click.echo(f"Running benchmark with config: {config}")
    # 実装はここに


if __name__ == '__main__':
    cli()
```

---

## 期待される出力例

### ターミナル出力

```
$ shinka-qa evolve --config examples/simple_calculator/quality_config.yaml

🧬 Shinka Quality v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Configuration:
  Target: calculator.py
  Initial Coverage: 42.5%
  Seeded Bugs: 5

🏝️  Island Evolution:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generation 1/30:
  Island 0: Coverage=45.2% Bugs=1/5 Fitness=0.42
  Island 1: Coverage=48.1% Bugs=2/5 Fitness=0.51
  Island 2: Coverage=43.7% Bugs=1/5 Fitness=0.38
  Island 3: Coverage=46.9% Bugs=2/5 Fitness=0.48
  Best: Island 1 (Fitness=0.51)

Generation 5/30:
  Island 0: Coverage=58.3% Bugs=3/5 Fitness=0.67
  Island 1: Coverage=62.5% Bugs=3/5 Fitness=0.71
  Island 2: Coverage=55.1% Bugs=2/5 Fitness=0.59
  Island 3: Coverage=60.2% Bugs=4/5 Fitness=0.72 ⭐
  Best: Island 3 (Fitness=0.72)
  
  💡 Insight: parametrize decorators improved edge case coverage

Generation 10/30 [Migration]:
  🔄 Migrating top solutions between islands...
  Island 0: Coverage=71.2% Bugs=4/5 Fitness=0.81
  Island 1: Coverage=68.9% Bugs=4/5 Fitness=0.78
  Island 2: Coverage=70.5% Bugs=3/5 Fitness=0.75
  Island 3: Coverage=73.8% Bugs=5/5 Fitness=0.89 ⭐
  Best: Island 3 (Fitness=0.89)
  
  💡 Insight: Mock objects improved test independence

...

Generation 30/30:
  Island 0: Coverage=92.1% Bugs=5/5 Fitness=0.95
  Island 1: Coverage=89.7% Bugs=5/5 Fitness=0.93
  Island 2: Coverage=91.3% Bugs=5/5 Fitness=0.94
  Island 3: Coverage=94.6% Bugs=5/5 Fitness=0.98 ⭐
  Best: Island 3 (Fitness=0.98)

✨ Evolution Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Final Results:
  Initial Coverage: 42.5%
  Final Coverage:   94.6% (+52.1%)
  
  Initial Bugs Detected: 1/5 (20%)
  Final Bugs Detected:   5/5 (100%)
  
  Test Execution Time: 1.23s
  Code Quality Score:  0.91/1.0

💾 Saved to: results/run_20250107_123456/
  ├── test_calculator_evolved.py
  ├── evolution_report.html
  ├── metrics.json
  └── lineage_tree.png

🌐 View results: shinka-qa visualize --results-dir results/run_20250107_123456
```

---

## 次のステップ（MVPの後）

1. **多様なサンプルプロジェクト**
   - REST API（Flask/FastAPI）
   - データ処理パイプライン（Pandas）
   - 機械学習モデル（scikit-learn）

2. **CI/CD統合**
   - GitHub Actions プラグイン
   - GitLab CI テンプレート
   - 自動プルリクエスト生成

3. **高度な機能**
   - 変異テスト（mutmut統合）
   - プロパティベーステスト（hypothesis統合）
   - パフォーマンステスト生成

4. **エコシステム統合**
   - VS Code拡張機能
   - pytest プラグイン
   - pre-commit フック

---

## 技術的課題と解決策

### 課題1: LLMが生成するコードの構文エラー
**解決策**: 
```python
def validate_and_fix_code(code: str) -> str:
    """生成されたコードを検証し、必要に応じて修正"""
    try:
        ast.parse(code)
        return code
    except SyntaxError as e:
        # LLMに修正を依頼
        fix_prompt = f"以下のコードに構文エラーがあります。修正してください:\n{code}\n\nエラー: {e}"
        fixed_code = call_llm(fix_prompt)
        return fixed_code
```

### 課題2: テスト実行のタイムアウト
**解決策**:
```python
import signal

def run_with_timeout(func, timeout=10):
    """タイムアウト付きで関数を実行"""
    def handler(signum, frame):
        raise TimeoutError()
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        result = func()
        signal.alarm(0)
        return result
    except TimeoutError:
        return None
```

### 課題3: カバレッジの局所最適化
**解決策**: 
- 新規性フィルタリングで多様性を維持
- 島モデルで並行探索
- メタスクラッチパッドで戦略を共有

---

## 実装の優先順位

### Phase 1: コア機能（1-2週間）
1. ✅ evaluator.py - 適応度関数
2. ✅ test_mutator.py - 基本的な変異
3. ✅ CLI - evolve コマンド
4. ✅ サンプルプロジェクト（電卓）

### Phase 2: 進化ループ（1週間）
1. ✅ 島モデルの実装
2. ✅ UCB1バンディット
3. ✅ 新規性フィルタリング
4. ✅ メタスクラッチパッド

### Phase 3: 可視化とレポート（1週間）
1. ✅ WebUI（進化の可視化）
2. ✅ HTML/PDFレポート生成
3. ✅ 系譜ツリー可視化

### Phase 4: 拡張機能（2週間）
1. ✅ 追加のサンプルプロジェクト
2. ✅ CI/CD統合
3. ✅ ドキュメント整備

---

## Claude Codeへの指示テンプレート

```
以下の仕様に基づいて、Shinka Qualityプロジェクトを実装してください。

# プロジェクト概要
ShinkaEvolveをフォークし、ソフトウェア品質改善（テストカバレッジとバグ検出）に特化したツール「Shinka Quality」を開発する。

# 実装するファイル
1. shinka_qa/core/evaluator.py - 適応度関数（上記仕様参照）
2. shinka_qa/evolution/test_mutator.py - テスト変異オペレータ
3. shinka_qa/cli/main.py - CLIインターフェース
4. examples/simple_calculator/calculator.py - サンプルコード
5. examples/simple_calculator/test_calculator_initial.py - 初期テスト
6. examples/simple_calculator/calculator_buggy.py - バグ版
7. examples/simple_calculator/quality_config.yaml - 設定ファイル

# 実装の指針
- Python 3.11以上を使用
- pytest, coverage.py, astモジュールを活用
- 型ヒントを適切に使用
- ドキュメント文字列を日本語で記述
- EVOLVE-BLOCK-START/ENDマーカーを変異可能領域に配置
- エラーハンドリングを適切に実装

# 最初のステップ
Phase 1のコア機能（evaluator.py, test_mutator.py, CLI, サンプル）から実装を開始してください。

実装が完了したら、以下のコマンドでテスト実行できることを確認してください：
```bash
shinka-qa evolve --config examples/simple_calculator/quality_config.yaml
```
```

---

## まとめ

この仕様書は、ShinkaEvolveをフォークして「Shinka Quality」という品質改善特化ツールを作成するための完全な設計図です。

**主要な特徴:**
1. ✅ テストカバレッジとバグ検出に特化した適応度関数
2. ✅ LLMベースのテスト変異オペレータ
3. ✅ 実用的なサンプルコード（電卓モジュール）
4. ✅ 段階的な実装計画

**次のアクション:**
Claude Codeに上記の指示テンプレートを渡して実装を開始できます。

ご質問や追加の要望があればお知らせください！
