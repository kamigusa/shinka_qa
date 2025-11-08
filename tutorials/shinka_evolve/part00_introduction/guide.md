# Part 0: イントロダクション - チュートリアルガイド

**所要時間**: 15分
**難易度**: 入門

---

## 🎯 このパートで学ぶこと

1. 進化計算とは何か
2. Shinka Evolveの概要
3. 基本概念の理解

---

## 🧬 進化計算とは

### 生物進化の原理

進化計算は、**自然選択**と**遺伝**の原理を模倣した最適化手法です。

```
世代1: 個体群（ランダム）
        ↓
     適応度評価
        ↓
      選択
        ↓
    交叉・変異
        ↓
世代2: 個体群（改善）
        ↓
      ...
        ↓
世代N: 最適解
```

### 基本用語

| 用語 | 説明 | 例 |
|------|------|-----|
| **個体** | 解の候補 | [0.5, 0.3, 0.8] |
| **個体群** | 個体の集合 | 100個体 |
| **遺伝子** | 個体のパラメータ | 0.5, 0.3, 0.8 |
| **適応度** | 解の良さ | 0.95 |
| **世代** | 進化の繰り返し | 50世代 |
| **選択** | 良い個体を選ぶ | トーナメント選択 |
| **交叉** | 個体を組み合わせる | 2点交叉 |
| **変異** | ランダムに変化 | ガウス変異 |

---

## 🌟 Shinka Evolve の特徴

### 1. 島モデル

```python
Island 1    Island 2    Island 3    Island 4
  ↓           ↓           ↓           ↓
 進化        進化        進化        進化
  ↓           ↓           ↓           ↓
  └───────── 移住交換 ──────────┘
              ↓
           最良個体
```

**メリット**:
- 並列化による高速化
- 多様性の維持
- 局所最適解の回避

---

### 2. シンプルなAPI

```python
from shinka_evolve import Island, Evolution

# 適応度関数
def fitness(individual):
    return sum(individual)  # 最大化

# 進化実行
evolution = Evolution(
    fitness_function=fitness,
    num_genes=10,
    num_islands=4,
    population_per_island=50
)

best = evolution.evolve(num_generations=100)
print(f"Best solution: {best}")
```

---

### 3. カスタマイズ可能

```python
# カスタム交叉
def custom_crossover(parent1, parent2):
    # 独自の交叉ロジック
    return child1, child2

# カスタム変異
def custom_mutation(individual, rate=0.1):
    # 独自の変異ロジック
    return mutated

evolution = Evolution(
    crossover=custom_crossover,
    mutation=custom_mutation
)
```

---

## 📊 適用例

### 例1: 関数最適化

**問題**: `f(x, y) = -x^2 - y^2` を最大化

```python
import numpy as np

def fitness(individual):
    x, y = individual
    return -(x**2 + y**2)  # 最大化（最小値は0）

evolution = Evolution(
    fitness_function=fitness,
    num_genes=2,
    bounds=[(-10, 10), (-10, 10)]  # xとyの範囲
)

best = evolution.evolve(num_generations=50)
print(f"Best: x={best[0]:.2f}, y={best[1]:.2f}")
print(f"Fitness: {fitness(best):.2f}")
```

**期待される出力**:
```
Best: x=0.00, y=0.00
Fitness: 0.00
```

---

### 例2: ハイパーパラメータ最適化

**問題**: 機械学習モデルの最適なハイパーパラメータを見つける

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score

# データロード
X, y = load_iris(return_X_y=True)

def fitness(individual):
    n_estimators, max_depth, min_samples_split = individual

    # 整数に変換
    n_estimators = int(n_estimators)
    max_depth = int(max_depth)
    min_samples_split = int(min_samples_split)

    # モデル作成
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split
    )

    # 交差検証
    scores = cross_val_score(model, X, y, cv=5)
    return scores.mean()

evolution = Evolution(
    fitness_function=fitness,
    num_genes=3,
    bounds=[
        (10, 200),   # n_estimators
        (1, 20),     # max_depth
        (2, 20)      # min_samples_split
    ]
)

best = evolution.evolve(num_generations=20)
print(f"Best hyperparameters: {best}")
print(f"Best score: {fitness(best):.4f}")
```

---

## 🔑 重要な概念

### 1. 適応度関数

**最も重要な部分**です。進化の方向性を決めます。

**良い適応度関数**:
- 明確な目的
- 高速な計算
- 適切なスケール

**悪い例**:
```python
def fitness(individual):
    # 遅い
    time.sleep(1)
    return sum(individual)
```

**良い例**:
```python
def fitness(individual):
    # 高速
    return np.sum(individual)
```

---

### 2. パラメータ設定

| パラメータ | 推奨値 | 説明 |
|-----------|-------|------|
| `num_generations` | 50-200 | 世代数 |
| `population_per_island` | 50-100 | 島ごとの個体数 |
| `num_islands` | 4-8 | 島の数 |
| `mutation_rate` | 0.01-0.1 | 変異率 |
| `crossover_rate` | 0.7-0.9 | 交叉率 |

---

### 3. 収束判定

```python
evolution = Evolution(
    fitness_function=fitness,
    early_stopping=True,
    patience=10,  # 10世代改善なしで停止
    min_improvement=0.001  # 最小改善率
)
```

---

## 💡 ベストプラクティス

### 1. 境界を設定

```python
# 探索範囲を制限
bounds = [(0, 1), (0, 1), (0, 1)]
```

### 2. 正規化

```python
def fitness(individual):
    # 複数の目的を正規化
    obj1 = f1(individual) / max_f1
    obj2 = f2(individual) / max_f2
    return obj1 + obj2
```

### 3. ログ記録

```python
evolution = Evolution(
    fitness_function=fitness,
    verbose=True,  # 進捗表示
    log_file="evolution.log"
)
```

---

## ❓ よくある質問

### Q1: 進化計算はいつ使うべき？

**A**: 以下の場合に有効

- 勾配が計算できない
- 離散的な探索空間
- 多峰性関数（局所最適解が多い）
- ブラックボックス最適化

### Q2: 他の最適化手法との違いは？

| 手法 | 勾配 | 並列化 | 離散 |
|------|------|-------|------|
| 勾配降下法 | 必要 | 難しい | × |
| ベイズ最適化 | 不要 | 難しい | × |
| 進化計算 | 不要 | 容易 | ○ |

### Q3: どのくらい速い？

**A**: 問題サイズによる

- 小規模（10変数）: 数秒〜数分
- 中規模（100変数）: 数分〜数時間
- 大規模（1000変数）: 数時間〜数日

並列化で大幅に高速化可能。

---

## 📝 チェックリスト

- [ ] 進化計算の基本原理を理解した
- [ ] Shinka Evolveの特徴を理解した
- [ ] 基本的なコード例を読んだ
- [ ] 適用例を確認した
- [ ] 重要な概念を理解した

**全てチェックできたら、Part 1に進みましょう！**

---

## 🔗 次のステップ

[Part 1: 基本的な進化](../part01_basic_evolution/) で、実際に進化アルゴリズムを実装します。

---

**作成日**: 2025-11-07
**バージョン**: 1.0
