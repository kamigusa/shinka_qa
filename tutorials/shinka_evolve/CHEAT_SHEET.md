# Shinka Evolve チートシート

**最終更新**: 2025-11-07

---

## ⚡ クイックスタート

```python
from shinka_evolve import Evolution
import numpy as np

# 適応度関数
def fitness(individual):
    return -np.sum(individual ** 2)  # Sphere関数最小化

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

## 📋 基本設定

### 遺伝子タイプ

```python
# バイナリ
gene_type='binary'

# 実数
gene_type='real'
bounds=[(-5, 5)] * num_genes

# 整数
gene_type='integer'
bounds=[(0, 100)] * num_genes
```

---

### 進化パラメータ

| パラメータ | デフォルト | 推奨範囲 |
|-----------|----------|---------|
| `num_generations` | 100 | 50-200 |
| `population_per_island` | 50 | 30-100 |
| `num_islands` | 4 | 2-8 |
| `mutation_rate` | 0.05 | 0.01-0.2 |
| `crossover_rate` | 0.8 | 0.6-0.9 |

---

## 🏝️ 島モデル

```python
evolution = Evolution(
    num_islands=4,
    migration_interval=10,      # 10世代ごと
    migration_size=2,           # 2個体移住
    migration_policy='best',    # 'best', 'random', 'tournament'
    migration_topology='ring'   # 'ring', 'fully_connected', 'hub'
)
```

---

## 🔀 選択・交叉・変異

### 選択

```python
selection='tournament'         # トーナメント選択（推奨）
selection='roulette'          # ルーレット選択
selection='rank'              # ランク選択
```

### 交叉

```python
crossover='single_point'      # 1点交叉
crossover='two_point'         # 2点交叉
crossover='uniform'           # 一様交叉
crossover='arithmetic'        # 算術交叉（実数用）
```

### 変異

```python
mutation='bit_flip'           # ビット反転（バイナリ用）
mutation='gaussian'           # ガウス変異（実数用）
mutation='uniform'            # 一様変異（実数用）
mutation='polynomial'         # 多項式変異（実数用）
```

---

## 🎯 多目的最適化

```python
from shinka_evolve import NSGA2

def fitness_vector(individual):
    obj1 = compute_objective1(individual)
    obj2 = compute_objective2(individual)
    return [obj1, obj2]

evolution = NSGA2(
    fitness_function=fitness_vector,
    num_objectives=2,
    num_genes=10
)

pareto_front = evolution.evolve(num_generations=100)
```

---

## 🚧 制約条件

### ペナルティ法

```python
def fitness(individual):
    objective = compute_objective(individual)

    # 制約違反
    violation = 0
    if sum(individual) > 100:
        violation += (sum(individual) - 100) ** 2

    return objective - 1000 * violation  # ペナルティ
```

### 修復法

```python
def repair(individual):
    individual = np.clip(individual, 0, 10)
    if sum(individual) > 100:
        individual *= (100 / sum(individual))
    return individual

def fitness(individual):
    individual = repair(individual)
    return compute_objective(individual)
```

---

## ⚙️ 高度な設定

### 早期停止

```python
evolution = Evolution(
    early_stopping=True,
    patience=10,
    min_improvement=0.001
)
```

### 並列化

```python
evolution = Evolution(
    parallel_fitness=True,
    num_workers=4
)
```

### キャッシング

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def fitness(individual_tuple):
    individual = np.array(individual_tuple)
    return compute(individual)
```

---

## 📊 よく使う適応度関数

### 関数最適化

```python
# Sphere
def sphere(x):
    return -np.sum(x ** 2)

# Rastrigin
def rastrigin(x):
    n = len(x)
    return -(10*n + np.sum(x**2 - 10*np.cos(2*np.pi*x)))

# Rosenbrock
def rosenbrock(x):
    result = 0
    for i in range(len(x)-1):
        result += 100*(x[i+1]-x[i]**2)**2 + (1-x[i])**2
    return -result
```

---

## 🐛 トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 収束が遅い | `num_islands`, `population_per_island`を増やす |
| 局所最適 | `mutation_rate`を上げる、島数を増やす |
| メモリ不足 | `population_per_island`を減らす |
| 実行時間長い | `num_generations`を減らす、早期停止を有効化 |

---

## 📈 パラメータチューニングガイド

### 小規模問題（10変数未満）

```python
num_genes=5,
num_islands=2,
population_per_island=30,
num_generations=50
```

### 中規模問題（10-100変数）

```python
num_genes=50,
num_islands=4,
population_per_island=50,
num_generations=100
```

### 大規模問題（100変数以上）

```python
num_genes=200,
num_islands=8,
population_per_island=100,
num_generations=200
```

---

## 🔗 リンク

- [チュートリアル](README.md)
- [GitHub](https://github.com/SakanaAI/ShinkaEvolve)

---

**作成日**: 2025-11-07
**バージョン**: 1.0
