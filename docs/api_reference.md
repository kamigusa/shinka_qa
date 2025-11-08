# API Reference

Shinka Qualityの主要なクラスと関数のリファレンスドキュメント。

## Core Modules

### QualityEvaluator

テストスイートの品質を評価するクラス。

```python
from shinka_qa.core.evaluator import QualityEvaluator
```

#### Constructor

```python
QualityEvaluator(
    target_module_path: Path,
    seeded_bugs_path: Path = None,
    weights: Dict[str, float] = None
)
```

**Parameters:**
- `target_module_path`: テスト対象モジュールのパス
- `seeded_bugs_path`: バグを仕込んだバージョンのパス（オプション）
- `weights`: 各指標の重み（デフォルト: coverage=0.4, bug_detection=0.35, efficiency=0.15, maintainability=0.1）

#### Methods

##### evaluate()

```python
evaluate(test_file_path: Path) -> Tuple[float, Dict[str, float]]
```

テストファイルを評価して適応度スコアを返す。

**Returns:**
- `float`: 総合適応度スコア（0.0〜1.0）
- `Dict[str, float]`: 各指標の詳細

**Example:**
```python
evaluator = QualityEvaluator(
    target_module_path=Path("calculator.py"),
    seeded_bugs_path=Path("calculator_buggy.py")
)

fitness, metrics = evaluator.evaluate(Path("test_calculator.py"))
print(f"Fitness: {fitness:.3f}")
print(f"Coverage: {metrics['coverage']:.1f}%")
```

##### set_baseline()

```python
set_baseline(initial_test_file: Path)
```

初期テストでベースライン値を設定。

## Evolution Modules

### TestMutator

テストコードを変異させるクラス。

```python
from shinka_qa.evolution.test_mutator import TestMutator
```

#### Constructor

```python
TestMutator(llm_client=None)
```

**Parameters:**
- `llm_client`: LLMクライアント（OpenAI, Anthropic等）。Noneの場合は簡易変異を使用。

#### Methods

##### mutate()

```python
mutate(
    test_code: str,
    target_code: str,
    strategy: str,
    context: Dict = None
) -> str
```

テストコードを変異させる。

**Parameters:**
- `test_code`: 現在のテストコード
- `target_code`: テスト対象のコード
- `strategy`: 変異戦略（'add_edge_cases', 'improve_assertions'等）
- `context`: 追加コンテキスト（オプション）

**Returns:**
- `str`: 変異後のテストコード

**Available Strategies:**
- `add_edge_cases`: エッジケースのテストを追加
- `improve_assertions`: アサーションを改善
- `add_parametrize`: pytest.mark.parametrizeを追加
- `add_fixtures`: pytestフィクスチャを追加
- `add_mocks`: モックを追加

### IslandModel

島モデル進化を管理するクラス。

```python
from shinka_qa.evolution.island_model import IslandModel
```

#### Constructor

```python
IslandModel(
    num_islands: int = 4,
    population_size: int = 20,
    migration_interval: int = 10,
    migration_rate: float = 0.1,
    elite_ratio: float = 0.3
)
```

#### Methods

##### initialize()

```python
initialize(initial_code: str, fitness_func: Callable)
```

全ての島を初期化。

##### evolve()

```python
evolve(
    generations: int,
    mutate_func: Callable,
    fitness_func: Callable,
    target_code: str = "",
    callback: Callable = None
) -> Individual
```

指定世代数だけ進化させる。

**Example:**
```python
from shinka_qa.evolution.island_model import IslandModel

island_model = IslandModel(
    num_islands=4,
    population_size=20,
    migration_interval=10
)

def mutate_func(code, target):
    # 変異ロジック
    return modified_code

def fitness_func(code):
    # 適応度評価ロジック
    return fitness, metrics

island_model.initialize(initial_code, fitness_func)
best_individual = island_model.evolve(
    generations=30,
    mutate_func=mutate_func,
    fitness_func=fitness_func
)
```

### UCB1Bandit

Upper Confidence Bound バンディットアルゴリズム。

```python
from shinka_qa.evolution.ucb_bandit import UCB1Bandit, AdaptiveBanditSelector
```

#### AdaptiveBanditSelector

```python
AdaptiveBanditSelector(
    strategies: List[str],
    models: List[str] = None,
    exploration_coefficient: float = 1.0
)
```

戦略とモデルの両方を選択する統合バンディット。

**Methods:**

```python
# 戦略とモデルを選択
selection = selector.select()  # {'strategy': '...', 'model': '...'}

# 報酬を更新
selector.update(
    strategy='add_edge_cases',
    fitness_improvement=0.15,
    model='gemini-2.5-flash'
)

# 統計情報を取得
stats = selector.get_statistics()
```

### NoveltyFilter

新規性フィルタリング。

```python
from shinka_qa.evolution.novelty_filter import NoveltyFilter
```

#### Constructor

```python
NoveltyFilter(
    similarity_threshold: float = 0.9,
    archive_size: int = 100
)
```

#### Methods

```python
# 新規性をチェック
is_novel = filter.is_novel(code)

# アーカイブに追加
filter.add_to_archive(code, fitness=0.85)

# 多様性スコアを取得
diversity = filter.get_diversity_score()
```

### MetaScratchpad

進化過程の知見を記録・共有。

```python
from shinka_qa.evolution.meta_scratchpad import MetaScratchpad
```

#### Methods

```python
scratchpad = MetaScratchpad()

# 洞察を追加
scratchpad.add_insight(
    generation=10,
    strategy='add_edge_cases',
    fitness_improvement=0.15,
    description='Edge cases significantly improved coverage'
)

# 最適な戦略を取得
best_strategies = scratchpad.get_best_strategies(top_k=3)

# 推奨戦略を取得
recommendation = scratchpad.get_strategy_recommendation(
    current_coverage=65.0
)

# 進捗サマリーを取得
summary = scratchpad.get_progress_summary()
```

## Visualization Modules

### ReportGenerator

HTMLレポートを生成。

```python
from shinka_qa.visualization.report_generator import ReportGenerator
```

#### Methods

```python
report_gen = ReportGenerator(results_dir=Path("results/run_123"))

# HTMLレポートを生成
html_file = report_gen.generate_html_report()

# サマリーテキストを生成
summary = report_gen.generate_summary_text()
```

### LineageTreeVisualizer

系譜ツリーを可視化。

```python
from shinka_qa.visualization.lineage_tree import LineageTreeVisualizer
```

#### Methods

```python
visualizer = LineageTreeVisualizer(results_dir=Path("results/run_123"))

# ノードを追加
visualizer.add_node(
    node_id="gen1_0",
    generation=1,
    fitness=0.75,
    parent_id="gen0_0",
    strategy="add_edge_cases"
)

# ASCIIツリーを生成
tree_text = visualizer.generate_ascii_tree()

# HTMLツリーを生成
tree_html = visualizer.generate_html_tree()

# ファイルに保存
tree_file = visualizer.save_tree()
```

## Utility Modules

### TestRunner

pytest実行ラッパー。

```python
from shinka_qa.utils.test_runner import TestRunner
```

#### Methods

```python
runner = TestRunner(timeout=10)

# テストを実行
result = runner.run_tests(
    test_file=Path("test_calculator.py"),
    target_dir=Path(".")
)

# カバレッジ測定付きで実行
result = runner.run_with_coverage(
    test_file=Path("test_calculator.py"),
    module_name="calculator",
    target_dir=Path(".")
)

# テストファイルを検証
is_valid, error_msg = runner.validate_test_file(
    Path("test_calculator.py")
)
```

## Type Definitions

### Individual

```python
@dataclass
class Individual:
    test_code: str
    fitness: float
    metrics: Dict[str, float]
    generation: int
    island_id: int
```

### Insight

```python
@dataclass
class Insight:
    generation: int
    strategy: str
    fitness_improvement: float
    description: str
    timestamp: str
    metadata: Dict[str, Any]
```

## Configuration Schema

### quality_config.yaml

```yaml
# テスト対象
target:
  module_path: str              # 必須
  test_initial_path: str        # 必須
  seeded_bugs_path: str         # オプション

# 適応度関数の重み
fitness_weights:
  coverage: float               # 0.0〜1.0
  bug_detection: float          # 0.0〜1.0
  efficiency: float             # 0.0〜1.0
  maintainability: float        # 0.0〜1.0

# 進化パラメータ
evolution:
  generations: int              # デフォルト: 30
  population_size: int          # デフォルト: 20
  num_islands: int              # デフォルト: 4
  migration_interval: int       # デフォルト: 10
  migration_rate: float         # デフォルト: 0.1
  elite_ratio: float            # デフォルト: 0.3

# LLM設定
llm:
  provider: str                 # "openai", "anthropic", etc.
  model: str                    # "gpt-5-nano", "claude-4.5-haiku", etc.
  temperature: float            # デフォルト: 0.7
  max_tokens: int               # デフォルト: 2000

# 変異戦略
mutation_strategies:
  - str                         # 戦略名のリスト

# 実行制限
limits:
  max_test_time: float          # 秒
  max_total_time: float         # 秒
  max_test_file_size: int       # 行数

# 出力
output:
  results_dir: str              # 結果ディレクトリ
  save_all_generations: bool
  visualization: bool
```

## Error Handling

### Common Exceptions

```python
# FileNotFoundError: テスト対象ファイルが見つからない
try:
    evaluator = QualityEvaluator(
        target_module_path=Path("nonexistent.py")
    )
except FileNotFoundError as e:
    print(f"Error: {e}")

# TimeoutError: テスト実行がタイムアウト
try:
    runner.run_tests(test_file, timeout=5)
except TimeoutError:
    print("Test execution timed out")

# SyntaxError: 生成されたコードに構文エラー
try:
    compile(mutated_code, '<string>', 'exec')
except SyntaxError as e:
    print(f"Syntax error in generated code: {e}")
```

## Performance Tips

### 1. 並列実行

複数の島を活用して並列化：

```python
island_model = IslandModel(
    num_islands=8,  # CPUコア数に応じて調整
    population_size=20
)
```

### 2. キャッシング

同じコードの評価を避ける：

```python
novelty_filter = NoveltyFilter(
    similarity_threshold=0.95,
    archive_size=200
)
```

### 3. タイムアウト設定

長時間実行を防ぐ：

```python
runner = TestRunner(timeout=5)  # 5秒でタイムアウト
```

## CLI Reference

### shinka-qa evolve

テストスイートを進化させます。

**Usage:**
```bash
shinka-qa evolve [OPTIONS]
```

**Options:**
- `--config PATH`: 設定ファイルのパス（必須）
- `--output-dir PATH`: 出力ディレクトリ（デフォルト: results/）
- `--verbose`: 詳細ログを表示
- `--llm / --no-llm`: LLMを使用するかどうか（デフォルト: 無効）

**Examples:**
```bash
# LLMなし（高速・無料）
shinka-qa evolve --config quality_config.yaml

# LLMあり（高品質なテスト生成）
shinka-qa evolve --config quality_config.yaml --llm

# 詳細ログ付き
shinka-qa evolve --config quality_config.yaml --verbose --llm
```

**Note:** LLMを使用する場合は、`.env`ファイルにAPIキーを設定してください。詳細は[Multi-Provider Setup Guide](multi_provider_setup.md)を参照してください。

## See Also

- [Getting Started Guide](getting_started.md)
- [Multi-Provider Setup Guide](multi_provider_setup.md)
- [GitHub Repository](https://github.com/yourusername/shinka-qa)
- [Issue Tracker](https://github.com/yourusername/shinka-qa/issues)
