# Part 1: 基本的な進化 - チュートリアルガイド

**所要時間**: 25分
**難易度**: 入門

---

## 🎯 このパートで学ぶこと

1. 遺伝的アルゴリズムの実装
2. 選択、交叉、変異の実践
3. 基本的な最適化問題の解決

---

## 🧬 遺伝的アルゴリズムの実装

### ステップ1: 簡単な例（One Max問題）

**問題**: ビット列の1の数を最大化

```python
import numpy as np
from shinka_evolve import Evolution

# 適応度関数: 1の数を数える
def fitness(individual):
    return np.sum(individual)

# 進化設定
evolution = Evolution(
    fitness_function=fitness,
    num_genes=20,              # 20ビット
    gene_type='binary',        # バイナリ遺伝子
    population_per_island=50,
    num_islands=1,             # 単一島から開始
    mutation_rate=0.05
)

# 進化実行
best = evolution.evolve(num_generations=50, verbose=True)

print(f"\nBest solution: {best}")
print(f"Fitness (1の数): {fitness(best)}")
```

**期待される出力**:
```
Generation 1: Best fitness = 12
Generation 10: Best fitness = 16
Generation 20: Best fitness = 19
Generation 30: Best fitness = 20

Best solution: [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
Fitness (1の数): 20
```

---

### ステップ2: 連続値最適化

**問題**: Sphere関数を最小化 `f(x) = sum(x_i^2)`

```python
import numpy as np

def fitness(individual):
    # 最小化問題なので負の値を返す（最大化に変換）
    return -np.sum(individual ** 2)

evolution = Evolution(
    fitness_function=fitness,
    num_genes=10,
    gene_type='real',          # 実数遺伝子
    bounds=[(-5, 5)] * 10,     # 各遺伝子の範囲
    population_per_island=50,
    num_islands=1,
    mutation_rate=0.1
)

best = evolution.evolve(num_generations=100, verbose=True)

print(f"\nBest solution: {best}")
print(f"Function value: {-fitness(best):.6f}")
```

**期待される出力**:
```
Generation 1: Best fitness = -15.234
Generation 25: Best fitness = -2.145
Generation 50: Best fitness = -0.234
Generation 100: Best fitness = -0.001

Best solution: [0.001 -0.002 0.001 ...]
Function value: 0.000100
```

---

### ステップ3: Rastrigin関数（難しい問題）

**問題**: 多峰性関数を最小化

```python
import numpy as np

def rastrigin(individual):
    n = len(individual)
    A = 10
    return -(A * n + np.sum(individual**2 - A * np.cos(2 * np.pi * individual)))

evolution = Evolution(
    fitness_function=rastrigin,
    num_genes=5,
    gene_type='real',
    bounds=[(-5.12, 5.12)] * 5,
    population_per_island=100,  # 難しいので個体数を増やす
    num_islands=1,
    mutation_rate=0.15          # 変異率も増やす
)

best = evolution.evolve(num_generations=200, verbose=True)

print(f"\nBest solution: {best}")
print(f"Function value: {-rastrigin(best):.6f}")
print(f"Global minimum: 0 at [0, 0, 0, 0, 0]")
```

---

## 🔀 選択・交叉・変異の理解

### 選択戦略

```python
# トーナメント選択
evolution = Evolution(
    selection='tournament',
    tournament_size=3  # 3個体から最良を選択
)

# ルーレット選択
evolution = Evolution(
    selection='roulette'  # 適応度に比例した確率
)

# ランク選択
evolution = Evolution(
    selection='rank'  # ランクに基づく選択
)
```

---

### 交叉戦略

```python
# 1点交叉
evolution = Evolution(
    crossover='single_point',
    crossover_rate=0.8
)

# 2点交叉
evolution = Evolution(
    crossover='two_point'
)

# 一様交叉
evolution = Evolution(
    crossover='uniform',
    uniform_rate=0.5  # 各遺伝子を50%の確率で交換
)

# 算術交叉（実数用）
evolution = Evolution(
    crossover='arithmetic',
    alpha=0.5  # 重み
)
```

---

### 変異戦略

```python
# ビット反転変異（バイナリ用）
evolution = Evolution(
    mutation='bit_flip',
    mutation_rate=0.05
)

# ガウス変異（実数用）
evolution = Evolution(
    mutation='gaussian',
    mutation_rate=0.1,
    mutation_sigma=0.5  # 標準偏差
)

# 一様変異（実数用）
evolution = Evolution(
    mutation='uniform',
    mutation_rate=0.1
)

# 多項式変異（実数用）
evolution = Evolution(
    mutation='polynomial',
    mutation_rate=0.1,
    eta=20  # 分布指数
)
```

---

## 📊 進化過程の可視化

```python
import matplotlib.pyplot as plt

def fitness_with_history(individual, history=[]):
    f = np.sum(individual ** 2)
    history.append(f)
    return -f

history = []

evolution = Evolution(
    fitness_function=lambda x: fitness_with_history(x, history),
    num_genes=10,
    gene_type='real',
    bounds=[(-5, 5)] * 10
)

best = evolution.evolve(num_generations=100)

# プロット
plt.figure(figsize=(10, 6))
plt.plot(history)
plt.xlabel('Evaluations')
plt.ylabel('Function Value')
plt.title('Convergence Plot')
plt.grid(True)
plt.savefig('convergence.png')
plt.show()
```

---

## 🎯 実践演習

### 演習1: Rosenbrock関数

**問題**: Rosenbrock関数を最小化

```python
def rosenbrock(individual):
    result = 0
    for i in range(len(individual) - 1):
        result += 100 * (individual[i+1] - individual[i]**2)**2 + (1 - individual[i])**2
    return -result

# あなたのコード
evolution = Evolution(
    # TODO: パラメータを設定
)

best = evolution.evolve(num_generations=?)
```

**ヒント**:
- `num_genes = 5`
- `bounds = [(-2, 2)] * 5`
- 大きめの`population_per_island`（100以上）

---

### 演習2: Knapsack問題（ナップザック問題）

**問題**: 重量制限内で価値を最大化

```python
# アイテムデータ
items = [
    {'weight': 10, 'value': 60},
    {'weight': 20, 'value': 100},
    {'weight': 30, 'value': 120},
    # ... 他のアイテム
]
max_weight = 50

def fitness(individual):
    # individual: [0, 1, 1, 0, ...] (選択/非選択)
    total_weight = sum(items[i]['weight'] for i, x in enumerate(individual) if x == 1)
    total_value = sum(items[i]['value'] for i, x in enumerate(individual) if x == 1)

    if total_weight > max_weight:
        return 0  # ペナルティ

    return total_value

# あなたのコード
evolution = Evolution(
    fitness_function=fitness,
    num_genes=len(items),
    gene_type='binary'
)

best = evolution.evolve(num_generations=50)
selected_items = [i for i, x in enumerate(best) if x == 1]
print(f"Selected items: {selected_items}")
```

---

## ⚙️ パラメータチューニング

### 個体数の影響

```python
# 実験: 個体数を変えて比較
for pop_size in [20, 50, 100, 200]:
    evolution = Evolution(
        fitness_function=fitness,
        population_per_island=pop_size
    )
    best = evolution.evolve(num_generations=100)
    print(f"Pop size {pop_size}: {fitness(best)}")
```

**観察**:
- 小さい個体数: 速いが精度低い
- 大きい個体数: 遅いが精度高い
- 推奨: 50-100

---

### 変異率の影響

```python
for mut_rate in [0.01, 0.05, 0.1, 0.2]:
    evolution = Evolution(
        fitness_function=fitness,
        mutation_rate=mut_rate
    )
    best = evolution.evolve(num_generations=100)
    print(f"Mutation rate {mut_rate}: {fitness(best)}")
```

**観察**:
- 低い変異率: 収束速いが局所最適
- 高い変異率: 探索広いが収束遅い
- 推奨: 0.05-0.1

---

## 📝 チェックリスト

- [ ] One Max問題を解いた
- [ ] 連続値最適化を実装した
- [ ] 選択・交叉・変異を理解した
- [ ] 進化過程を可視化した
- [ ] 演習問題を解いた
- [ ] パラメータチューニングを実験した

**全てチェックできたら、Part 2に進みましょう！**

---

**作成日**: 2025-11-07
**バージョン**: 1.0
