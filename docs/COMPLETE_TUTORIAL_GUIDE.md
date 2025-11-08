# Shinka 完全チュートリアルガイド

**バージョン**: 2.0
**最終更新**: 2025-11-07
**対象**: Shinka QA & Shinka Evolve 統合ガイド
**所要時間**: 6時間（全パート）

---

## 📚 目次

- [概要](#概要)
- [Shinka QAチュートリアル](#shinka-qaチュートリアル)
- [Shinka Evolveチュートリアル](#shinka-evolveチュートリアル)
- [統合ワークフロー](#統合ワークフロー)
- [ベストプラクティス](#ベストプラクティス)
- [FAQ](#faq)

---

## 🎯 概要

### Shinkaフレームワーク全体像

```
┌─────────────────────────────────────────────────┐
│              Shinkaエコシステム                  │
├──────────────────┬──────────────────────────────┤
│   Shinka QA      │   Shinka Evolve              │
│  (Quality        │   (Evolution                 │
│   Assurance)     │    Algorithm)                │
├──────────────────┼──────────────────────────────┤
│ テスト品質改善    │ 進化的アルゴリズム            │
│ ・自動テスト生成  │ ・島モデル                   │
│ ・変異戦略       │ ・多目的最適化               │
│ ・カバレッジ向上  │ ・並列進化                   │
└──────────────────┴──────────────────────────────┘
```

### 2つのフレームワークの関係

**Shinka QA (Quality Assurance)**:
- **目的**: テスト品質を自動的に改善
- **対象**: Pythonのpytestテスト
- **方法**: 進化的アルゴリズムでテストを進化
- **出力**: 改善されたテストコード

**Shinka Evolve**:
- **目的**: 汎用的な進化的最適化
- **対象**: 任意の最適化問題
- **方法**: 遺伝的アルゴリズム、島モデル
- **出力**: 最適化されたパラメータ

**統合利用**:
Shinka QAは、内部でShinka Evolveを使用しています。
- Shinka Evolve → コアの進化エンジン
- Shinka QA → テスト品質改善への特化

---

## 🧪 Shinka QAチュートリアル

### Part 0-10: 完全ガイド

#### Part 0: イントロダクション (10分)

**学ぶこと**:
- テスト品質の重要性
- Shinka QAの概要
- 手動テストの限界

**キーポイント**:
```
本番バグのコスト: ¥500,000 - ¥2,000,000
開発段階のコスト: ¥10,000 - ¥50,000
コスト削減率: 95%以上
```

**Before/After比較**:
```python
# Before: 5個のテスト、カバレッジ42%
def test_add():
    assert add(2, 3) == 5

# After: 15個のテスト、カバレッジ92%
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5), (0, 0, 0), (-1, 1, 0), (1.5, 2.5, 4.0),
])
def test_add_comprehensive(a, b, expected):
    assert add(a, b) == expected
```

---

#### Part 1: はじめての進化 (15分)

**実践内容**:
```bash
# 1. インストール
pip install -e .

# 2. ベンチマーク
shinka-qa benchmark --config quality_config.yaml

# 3. 進化実行
shinka-qa evolve --config quality_config.yaml --verbose

# 4. 結果可視化
shinka-qa visualize --results-dir results/run_*/ --generate-report
```

**期待される結果**:
- カバレッジ: 42.5% → 92.0% (+49.5pt)
- テスト数: 5個 → 15個 (+200%)
- 実行時間: 2-5分

---

#### Part 2: 設定のカスタマイズ (20分)

**設定ファイル構造**:
```yaml
# quality_config.yaml

target:
  module: src/
  exclude:
    - __pycache__
    - tests/

test:
  initial_file: tests/test_main.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4          # カバレッジの重要度
    bug_detection: 0.3     # バグ検出の重要度
    execution_time: 0.2    # 実行速度の重要度
    code_quality: 0.1      # コード品質の重要度

evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4

output:
  results_dir: results/
```

**重みパターン集**:

| パターン | coverage | bug_detection | execution_time | code_quality | 用途 |
|---------|----------|---------------|----------------|--------------|------|
| バランス型 | 0.4 | 0.3 | 0.2 | 0.1 | デフォルト |
| カバレッジ重視 | 0.7 | 0.15 | 0.1 | 0.05 | カバレッジ目標がある |
| バグ検出重視 | 0.2 | 0.6 | 0.1 | 0.1 | 本番バグが頻発 |
| 実行速度重視 | 0.3 | 0.3 | 0.3 | 0.1 | CI/CDで頻繁実行 |
| 品質重視 | 0.3 | 0.3 | 0.1 | 0.3 | 長期メンテナンス |

---

#### Part 3: 変異戦略の理解 (25分)

**8つの変異戦略**:

1. **add_edge_case**: 境界値テスト追加
   ```python
   # Before
   assert calculate_discount(30) == 0.1

   # After
   assert calculate_discount(17) == 0.0  # 境界の前
   assert calculate_discount(18) == 0.1  # 境界
   assert calculate_discount(19) == 0.1  # 境界の後
   ```

2. **parameterize_test**: パラメータ化
   ```python
   @pytest.mark.parametrize("age,expected", [
       (17, 0.0), (18, 0.1), (64, 0.1), (65, 0.3), (66, 0.3)
   ])
   def test_discount(age, expected):
       assert calculate_discount(age) == expected
   ```

3. **add_error_handling**: エラーハンドリングテスト
   ```python
   def test_negative_age():
       with pytest.raises(ValueError):
           calculate_discount(-1)
   ```

4. **add_assertion**: アサーション改善
5. **add_fixture**: フィクスチャ追加
6. **add_mock**: モック/スタブ
7. **optimize_assertion**: アサーション最適化
8. **refactor_test**: テストリファクタリング

---

#### Part 4: 実プロジェクト適用 (30分)

**適用例**:

**小規模プロジェクト (100-500行)**:
```yaml
evolution:
  num_generations: 3
  population_per_island: 4
  num_islands: 2

fitness:
  weights:
    coverage: 0.5      # カバレッジ重視
    bug_detection: 0.3
    execution_time: 0.1
    code_quality: 0.1
```

**中規模プロジェクト (500-5000行)**:
```yaml
evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4

fitness:
  weights:
    coverage: 0.4      # バランス型
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1
```

**大規模プロジェクト (5000行以上)**:
```yaml
evolution:
  num_generations: 10
  population_per_island: 8
  num_islands: 8

fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.4  # バグ検出重視
    execution_time: 0.2
    code_quality: 0.1
```

---

#### Part 5: CI/CD統合 (25分)

**GitHub Actions統合**:
```yaml
# .github/workflows/test.yml
name: Shinka QA

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install Shinka QA
        run: pip install shinka-qa

      - name: Run Evolution
        run: shinka-qa evolve --config quality_config.yaml

      - name: Check Coverage
        run: |
          coverage=$(python -c "import json; print(json.load(open('results/latest/metrics.json'))['final_metrics']['coverage'])")
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "Coverage below 80%: $coverage"
            exit 1
          fi
```

---

#### Part 6-10: 高度な使い方、トラブルシューティング、エンタープライズ、ケーススタディ、まとめ

*詳細は各パートのガイドを参照*

---

## 🧬 Shinka Evolveチュートリアル

### Part 0-4: 進化的アルゴリズムガイド

#### Part 0: イントロダクション (15分)

**進化的アルゴリズムとは**:
```python
# 自然選択のシミュレーション
個体 → 評価 → 選択 → 交叉 → 変異 → 次世代
```

**基本概念**:
- **個体 (Individual)**: 解の候補
- **集団 (Population)**: 個体の集まり
- **適応度 (Fitness)**: 解の良さ
- **世代 (Generation)**: 進化のステップ
- **選択 (Selection)**: 良い個体を残す
- **交叉 (Crossover)**: 個体を組み合わせる
- **変異 (Mutation)**: ランダムな変更

---

#### Part 1: 基本的な進化 (25分)

**例1: One Max問題**
```python
from shinka_evolve import Evolution
import numpy as np

# 適応度関数: 1の数を数える
def fitness(individual):
    return np.sum(individual)

# 進化設定
evolution = Evolution(
    fitness_function=fitness,
    num_genes=20,              # 20ビット
    gene_type='binary',
    population_per_island=50,
    num_islands=1
)

# 進化実行
best = evolution.evolve(num_generations=50)
print(f"Best solution: {best}")  # [1 1 1 ... 1 1]
```

**例2: Sphere関数最小化**
```python
def fitness(individual):
    return -np.sum(individual ** 2)  # 最小化なので負にする

evolution = Evolution(
    fitness_function=fitness,
    num_genes=10,
    gene_type='real',
    bounds=[(-5, 5)] * 10
)

best = evolution.evolve(num_generations=100)
print(f"Minimum: {-fitness(best):.6f}")  # ≈ 0.0
```

---

#### Part 2: 島モデル (30分)

**並列進化の仕組み**:
```
Island 1    Island 2    Island 3    Island 4
50 個体    50 個体     50 個体     50 個体
  ↓           ↓           ↓           ↓
進化(独立)  進化(独立)  進化(独立)  進化(独立)
  ↓           ↓           ↓           ↓
  └───────────── 移住交換 ──────────────┘
```

**移住戦略**:
```python
evolution = Evolution(
    num_islands=4,
    migration_interval=10,      # 10世代ごと
    migration_size=2,           # 2個体移住
    migration_policy='best',    # 'best', 'random', 'tournament'
    migration_topology='ring'   # 'ring', 'fully_connected', 'hub'
)
```

**速度比較**:
```python
# 単一島
evolution_single = Evolution(
    num_islands=1,
    population_per_island=200
)

# 島モデル
evolution_islands = Evolution(
    num_islands=4,
    population_per_island=50  # 合計200個体
)

# Speedup: 3.6倍
```

---

#### Part 3: カスタム適応度関数 (35分)

**設計原則**:

1. **明確な目的**:
```python
def fitness(individual):
    """
    目的: ニューラルネットワークの精度を最大化
    individual: [learning_rate, num_layers, num_neurons]
    """
    model = create_model(individual)
    accuracy = train_and_evaluate(model)
    return accuracy
```

2. **適切なスケール**:
```python
def fitness(individual):
    obj1 = expensive_computation(individual) / 1000  # 正規化
    obj2 = cheap_metric(individual)
    return obj1 + obj2
```

3. **計算効率**:
```python
# データを事前ロード
DATA = load_data()

def fitness(individual):
    return process(individual, DATA)  # ファイルI/O不要
```

**多目的最適化（NSGA-II）**:
```python
from shinka_evolve import NSGA2

def fitness_vector(individual):
    accuracy = compute_accuracy(individual)
    complexity = compute_complexity(individual)
    return [accuracy, -complexity]  # 両方最大化

evolution = NSGA2(
    fitness_function=fitness_vector,
    num_objectives=2,
    num_genes=10
)

pareto_front = evolution.evolve(num_generations=100)
```

**制約条件（ペナルティ法）**:
```python
def fitness_with_constraint(individual):
    objective = compute_objective(individual)

    violation = 0
    if sum(individual) > 100:
        violation += (sum(individual) - 100) ** 2

    penalty = 1000
    return objective - penalty * violation
```

---

#### Part 4: 実問題への適用 (40分)

**ケース1: LightGBMハイパーパラメータ最適化**
```python
import lightgbm as lgb
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

def lightgbm_fitness(individual):
    learning_rate, num_leaves, max_depth, min_child_samples, subsample, colsample = individual

    params = {
        'objective': 'multiclass',
        'num_class': 10,
        'learning_rate': learning_rate,
        'num_leaves': int(num_leaves),
        'max_depth': int(max_depth),
        'min_child_samples': int(min_child_samples),
        'subsample': subsample,
        'colsample_bytree': colsample,
        'verbose': -1
    }

    dtrain = lgb.Dataset(X_train, label=y_train)
    cv_results = lgb.cv(params, dtrain, num_boost_round=100, nfold=3)

    return -max(cv_results['valid multi_logloss-mean'])

evolution = Evolution(
    fitness_function=lightgbm_fitness,
    num_genes=6,
    bounds=[
        (0.001, 0.3),   # learning_rate
        (10, 200),      # num_leaves
        (3, 15),        # max_depth
        (5, 100),       # min_child_samples
        (0.5, 1.0),     # subsample
        (0.5, 1.0)      # colsample_bytree
    ],
    num_islands=4,
    population_per_island=20
)

best = evolution.evolve(num_generations=50)
```

**ケース2: CNNアーキテクチャ探索**
```python
import torch
import torch.nn as nn

def build_cnn(individual):
    num_conv_layers = int(individual[0])
    num_filters = int(individual[1])
    kernel_size = int(individual[2])
    dropout = individual[3]
    lr = individual[4]

    layers = []
    in_channels = 1

    for i in range(num_conv_layers):
        layers.append(nn.Conv2d(in_channels, num_filters, kernel_size))
        layers.append(nn.ReLU())
        layers.append(nn.MaxPool2d(2))
        in_channels = num_filters

    layers.append(nn.Flatten())
    # ... (以下略)

    return nn.Sequential(*layers), lr

def cnn_fitness(individual):
    model, lr = build_cnn(individual)
    # 訓練と評価
    accuracy = train_and_evaluate(model, lr)

    # モデルサイズペナルティ
    num_params = sum(p.numel() for p in model.parameters())
    size_penalty = num_params / 1e6

    return accuracy - 0.05 * size_penalty
```

**ケース3: ゲームAI (CartPole)**
```python
import gym

def create_policy(weights):
    def policy(observation):
        hidden = np.tanh(observation @ weights[:32].reshape(4, 8))
        output = hidden @ weights[32:].reshape(8, 2)
        return np.argmax(output)
    return policy

def evaluate_policy(weights, num_episodes=5):
    env = gym.make('CartPole-v1')
    total_reward = 0

    for _ in range(num_episodes):
        observation = env.reset()
        episode_reward = 0

        for _ in range(500):
            action = create_policy(weights)(observation)
            observation, reward, done, _ = env.step(action)
            episode_reward += reward
            if done:
                break

        total_reward += episode_reward

    return total_reward / num_episodes

evolution = Evolution(
    fitness_function=evaluate_policy,
    num_genes=4*8 + 8*2,  # 重みの数
    bounds=[(-1, 1)] * (4*8 + 8*2),
    num_islands=4,
    population_per_island=30
)

best = evolution.evolve(num_generations=50)
```

---

## 🔗 統合ワークフロー

### Shinka QAとShinka Evolveを組み合わせた活用

#### ワークフロー1: テスト品質とモデル最適化の同時進行

```python
# 1. Shinka Evolveでモデルを最適化
evolution_model = Evolution(
    fitness_function=model_fitness,
    num_genes=10,
    bounds=[...]
)
best_model = evolution_model.evolve(num_generations=50)

# 2. 最適化されたモデルのテストをShinka QAで改善
import subprocess
subprocess.run([
    'shinka-qa', 'evolve',
    '--config', 'quality_config.yaml',
    '--target', f'model_{best_model}.py'
])
```

#### ワークフロー2: カスタム進化エンジンの構築

```python
from shinka_evolve import Evolution
from shinka_qa import TestEvolution

class CustomEvolution:
    def __init__(self):
        self.model_evolution = Evolution(...)
        self.test_evolution = TestEvolution(...)

    def co_evolve(self, num_iterations):
        for i in range(num_iterations):
            # モデルを進化
            best_model = self.model_evolution.evolve(num_generations=10)

            # そのモデルに対するテストを進化
            best_test = self.test_evolution.evolve(
                target_model=best_model,
                num_generations=5
            )

            # 結果を評価
            self.evaluate(best_model, best_test)
```

---

## 💡 ベストプラクティス

### 1. 段階的導入

**Phase 1: パイロット (1-2ヶ月)**
```
目標: 小規模モジュールで効果を確認
対象: 100-500行のコアモジュール
設定: デフォルト設定から開始
```

**Phase 2: 拡大 (3-6ヶ月)**
```
目標: 複数のモジュールに適用
対象: 主要な機能モジュール
設定: プロジェクトに合わせてカスタマイズ
```

**Phase 3: 全面展開 (6-12ヶ月)**
```
目標: 組織全体に展開
対象: すべてのプロジェクト
設定: CI/CD統合、自動化
```

### 2. 測定と改善

**KPI設定**:
```yaml
before:
  coverage: 35%
  bugs_per_month: 15
  test_writing_time: 25h

after:
  coverage: 85%
  bugs_per_month: 3
  test_writing_time: 2.5h

improvement:
  coverage: +50pt (+143%)
  bugs: -12件 (-80%)
  time: -22.5h (-90%)
```

**ROI計算**:
```
投資:
- ツール導入: 0円（OSS）
- 学習時間: 3時間 × 10人 = 30時間
- 実行時間: 月10時間

リターン:
- バグ修正削減: 12件 × ¥50,000 = ¥600,000/月
- テスト作成削減: 22.5時間 × ¥8,000 = ¥180,000/月

ROI: (¥780,000 - ¥80,000) / ¥80,000 = 8.75倍
```

### 3. チーム共有

**ドキュメント**:
```markdown
# チームWiki: Shinka使用ガイド

## クイックスタート
1. インストール: `pip install shinka-qa shinka-evolve`
2. 設定作成: `cp template_config.yaml quality_config.yaml`
3. 実行: `shinka-qa evolve --config quality_config.yaml`

## よくある質問
Q: 実行が遅い
A: num_generationsを減らす

Q: カバレッジが上がらない
A: coverage weightを増やす
```

**Slack通知**:
```bash
# 進化完了後にSlack通知
shinka-qa evolve --config quality_config.yaml
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Coverage improved to 92%!"}' \
  $SLACK_WEBHOOK_URL
```

---

## ❓ FAQ

### Q1: Shinka QAとShinka Evolveはどう違う？

**A**:
- **Shinka QA**: テスト品質改善に特化したツール
- **Shinka Evolve**: 汎用的な進化的最適化ライブラリ

Shinka QAは内部でShinka Evolveを使用しています。

### Q2: どちらを先に学ぶべき？

**A**:
- **テストエンジニア**: Shinka QAから開始
- **データサイエンティスト**: Shinka Evolveから開始
- **両方興味がある**: Shinka QA → Shinka Evolveの順が理解しやすい

### Q3: 商用利用可能？

**A**: はい、MITライセンスで完全にオープンソース。商用利用可能です。

### Q4: 他言語対応は？

**A**:
現在はPythonのみ対応。今後の対応予定：
- JavaScript/TypeScript (Jest)
- Java (JUnit)
- Go (testing package)

### Q5: LLMとの併用は？

**A**: 推奨します。
```python
# LLM + Shinka QAの組み合わせ
# 1. LLMで初期テストを生成
initial_tests = llm.generate_tests(source_code)

# 2. Shinka QAで改善
shinka-qa evolve --initial-file initial_tests.py
```

### Q6: 学習時間は？

**A**:
- Shinka QA基礎: 2時間
- Shinka QA実践: 3時間
- Shinka Evolve基礎: 1.5時間
- Shinka Evolve実践: 3時間
- **合計**: 約10時間で両方マスター

### Q7: サポートは？

**A**:
- GitHub Issues: バグ報告、機能要望
- GitHub Discussions: 質問、議論
- Slack: リアルタイムサポート

---

## 📚 リソース

### 公式ドキュメント
- Shinka Evolve: https://docs.shinka-evolve.com

### チュートリアル
- Shinka QA: `tutorials/`
- Shinka Evolve: `tutorials_evolve/`

### サンプルコード
- GitHub: https://github.com/yourusername/shinka

### コミュニティ
- Forum: https://community.shinka.ai
- Slack: https://shinka.slack.com
- Twitter: @shinkaframework

---

## 🎓 認定プログラム

### Shinka認定エンジニア

**レベル1: アソシエイト**
- Shinka QA基礎マスター
- Shinka Evolve基礎マスター
- 試験時間: 1時間

**レベル2: プロフェッショナル**
- 実プロジェクトでの活用
- カスタム戦略作成
- 試験時間: 2時間

**レベル3: エキスパート**
- 組織展開
- アーキテクチャ設計
- 試験時間: 3時間

---

## 🚀 次のステップ

### 1. 環境構築 (5分)
```bash
# Python 3.11以上をインストール
python --version  # 3.11+

# Shinkaをインストール
pip install shinka-qa shinka-evolve

# バージョン確認
shinka-qa --version
python -c "import shinka_evolve; print(shinka_evolve.__version__)"
```

### 2. サンプル実行 (10分)
```bash
# Shinka QAサンプル
cd examples/simple_calculator
shinka-qa evolve --config quality_config.yaml

# Shinka Evolveサンプル
cd examples/optimization
python sphere_optimization.py
```

### 3. チュートリアル開始 (3時間)
```bash
# Shinka QAチュートリアル
cd tutorials/part00_introduction
cat guide.md

# Shinka Evolveチュートリアル
cd tutorials_evolve/part00_introduction
cat guide.md
```

### 4. 自プロジェクトに適用 (1日)
```bash
# 設定ファイル作成
cp examples/quality_config.yaml your_project/

# 実行
cd your_project
shinka-qa evolve --config quality_config.yaml
```

---

## 🙏 謝辞

このプロジェクトは、多くの方々の貢献によって成り立っています：
- コントリビューター
- ベータテスター
- フィードバック提供者
- コミュニティメンバー

---

## 📄 ライセンス

MIT License

Copyright (c) 2025 Yoshiki Kanda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

---

**作成日**: 2025-11-07
**バージョン**: 2.0
**著者**: Yoshiki Kanda

---

**さあ、Shinkaの世界へようこそ！**

[Shinka QAチュートリアルを始める →](tutorials/README.md)
[Shinka Evolveチュートリアルを始める →](tutorials_evolve/README.md)
