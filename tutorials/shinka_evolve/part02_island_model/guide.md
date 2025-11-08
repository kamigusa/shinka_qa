# Part 2: 島モデル - チュートリアルガイド

**所要時間**: 30分
**難易度**: 中級

---

## 🎯 このパートで学ぶこと

1. 島モデルの原理
2. 並列進化の実装
3. 移住戦略の理解
4. パフォーマンス最適化

---

## 🏝️ 島モデルとは

### 基本概念

```
Island 1        Island 2        Island 3        Island 4
50 individuals  50 individuals  50 individuals  50 individuals
    ↓               ↓               ↓               ↓
  進化(独立)      進化(独立)      進化(独立)      進化(独立)
    ↓               ↓               ↓               ↓
    └───────────── 移住交換 ──────────────┘
                    ↓
              各島の最良個体を集約
                    ↓
                 全体の最良
```

**メリット**:
1. **並列化**: 複数コアで同時実行
2. **多様性維持**: 各島が独立に進化
3. **局所最適回避**: 島間移住で探索範囲拡大

---

## 🚀 島モデルの実装

### 基本的な使用

```python
from shinka_evolve import Evolution
import numpy as np

def fitness(individual):
    return -np.sum(individual ** 2)

# 単一島（従来）
evolution_single = Evolution(
    fitness_function=fitness,
    num_genes=10,
    num_islands=1,              # 単一島
    population_per_island=200   # 200個体
)

# 島モデル（4島）
evolution_islands = Evolution(
    fitness_function=fitness,
    num_genes=10,
    num_islands=4,              # 4島
    population_per_island=50    # 各島50個体（合計200）
)

# 速度比較
import time

start = time.time()
best_single = evolution_single.evolve(num_generations=100)
time_single = time.time() - start

start = time.time()
best_islands = evolution_islands.evolve(num_generations=100)
time_islands = time.time() - start

print(f"Single island: {time_single:.2f}s")
print(f"Island model: {time_islands:.2f}s")
print(f"Speedup: {time_single / time_islands:.2f}x")
```

**期待される結果**:
```
Single island: 45.23s
Island model: 12.45s
Speedup: 3.63x
```

---

## 🔄 移住戦略

### 移住パラメータ

```python
evolution = Evolution(
    fitness_function=fitness,
    num_islands=4,

    # 移住設定
    migration_interval=10,      # 10世代ごとに移住
    migration_size=2,           # 各島から2個体を移住
    migration_policy='best',    # 最良個体を移住
)
```

---

### 移住ポリシー

#### 1. Best Policy（最良個体移住）

```python
evolution = Evolution(
    migration_policy='best',
    migration_size=2  # 各島の最良2個体を移住
)
```

**特徴**:
- 最良解の拡散が速い
- 収束が速い
- 多様性が失われやすい

---

#### 2. Random Policy（ランダム移住）

```python
evolution = Evolution(
    migration_policy='random',
    migration_size=5  # ランダムに5個体
)
```

**特徴**:
- 多様性維持
- 収束が遅い
- 探索範囲が広い

---

#### 3. Tournament Policy（トーナメント移住）

```python
evolution = Evolution(
    migration_policy='tournament',
    migration_size=3,
    tournament_size=5  # 5個体から3個体を選択
)
```

**特徴**:
- BestとRandomの中間
- バランスが良い
- **推奨**

---

### 移住トポロジー

#### リング型

```python
evolution = Evolution(
    migration_topology='ring'
)

# Island 1 → Island 2 → Island 3 → Island 4 → Island 1
```

#### 完全グラフ型

```python
evolution = Evolution(
    migration_topology='fully_connected'
)

# すべての島が相互に移住
```

#### ハブ型

```python
evolution = Evolution(
    migration_topology='hub'
)

# Island 1（ハブ）↔ Island 2, 3, 4
```

---

## 📊 実験: 島モデルの効果

### 実験1: 島数の影響

```python
import matplotlib.pyplot as plt

def run_experiment(num_islands):
    evolution = Evolution(
        fitness_function=fitness,
        num_islands=num_islands,
        population_per_island=50
    )
    best = evolution.evolve(num_generations=100)
    return fitness(best)

results = []
for n in [1, 2, 4, 8]:
    score = run_experiment(n)
    results.append((n, score))
    print(f"{n} islands: {score:.6f}")

# プロット
islands, scores = zip(*results)
plt.plot(islands, scores, marker='o')
plt.xlabel('Number of Islands')
plt.ylabel('Best Fitness')
plt.title('Effect of Number of Islands')
plt.grid(True)
plt.show()
```

**観察**:
- 1島: 最も遅く、精度も低い
- 2-4島: 良いバランス
- 8島: 速いが、過度な並列化でオーバーヘッド

**推奨**: CPUコア数に合わせる（4-8島）

---

### 実験2: 移住間隔の影響

```python
for interval in [5, 10, 20, 50]:
    evolution = Evolution(
        fitness_function=fitness,
        num_islands=4,
        migration_interval=interval
    )
    best = evolution.evolve(num_generations=100)
    print(f"Interval {interval}: {fitness(best):.6f}")
```

**観察**:
- 短い間隔（5）: 多様性低下
- 長い間隔（50）: 独立性高いが収束遅い
- **推奨**: 10-20世代

---

## 🎯 実践演習

### 演習1: 並列化の効果測定

**タスク**: 以下の設定で速度を比較

```python
configs = [
    {'num_islands': 1, 'population_per_island': 200},
    {'num_islands': 2, 'population_per_island': 100},
    {'num_islands': 4, 'population_per_island': 50},
    {'num_islands': 8, 'population_per_island': 25},
]

for config in configs:
    # 実行時間を測定
    pass
```

---

### 演習2: 移住戦略の比較

**タスク**: 3つの移住ポリシーを比較

```python
for policy in ['best', 'random', 'tournament']:
    evolution = Evolution(
        fitness_function=fitness,
        migration_policy=policy
    )
    best = evolution.evolve(num_generations=100)
    print(f"{policy}: {fitness(best):.6f}")
```

**質問**:
- どのポリシーが最良？
- なぜそうなった？

---

## ⚡ パフォーマンス最適化

### 1. 適応度関数の高速化

```python
# 遅い
def fitness_slow(individual):
    result = 0
    for x in individual:
        result += x ** 2
    return -result

# 速い（NumPy）
def fitness_fast(individual):
    return -np.sum(individual ** 2)
```

**速度差**: 10-100倍

---

### 2. 並列評価

```python
evolution = Evolution(
    fitness_function=fitness,
    parallel_fitness=True,  # 適応度評価を並列化
    num_workers=4
)
```

**注意**: 適応度関数が重い場合のみ有効

---

### 3. メモリ最適化

```python
evolution = Evolution(
    fitness_function=fitness,
    store_history=False,  # 履歴を保存しない
    cache_fitness=True    # 適応度をキャッシュ
)
```

---

## 📊 高度なトピック

### 適応的移住

```python
class AdaptiveMigration:
    def __init__(self):
        self.interval = 10

    def should_migrate(self, generation, diversity):
        # 多様性が低い場合は頻繁に移住
        if diversity < 0.1:
            self.interval = 5
        else:
            self.interval = 20

        return generation % self.interval == 0

evolution = Evolution(
    migration_callback=AdaptiveMigration()
)
```

---

### 非同期島モデル

```python
evolution = Evolution(
    asynchronous=True,  # 各島が独立に進化
    sync_interval=50    # 50世代ごとに同期
)
```

**メリット**:
- 負荷分散
- より並列化
- スケーラビリティ向上

---

## 📝 チェックリスト

- [ ] 島モデルの原理を理解
- [ ] 移住戦略を実装
- [ ] 並列化の効果を確認
- [ ] パラメータを実験
- [ ] パフォーマンス最適化を試した

**全てチェックできたら、Part 3に進みましょう！**

---

**作成日**: 2025-11-07
**バージョン**: 1.0
