# Part 3: カスタム適応度関数 - チュートリアルガイド

**所要時間**: 35分
**難易度**: 中級〜上級

---

## 🎯 このパートで学ぶこと

1. 適応度関数の設計原則
2. 多目的最適化
3. 制約条件の扱い
4. ドメイン固有の適応度関数

---

## 🎨 適応度関数の設計原則

### 原則1: 明確な目的

**悪い例**:
```python
def fitness(individual):
    # 何を最適化している？
    return sum(individual) * np.mean(individual) / len(individual)
```

**良い例**:
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

---

### 原則2: 適切なスケール

**問題**:
```python
def fitness(individual):
    obj1 = expensive_computation(individual)  # 0-1000
    obj2 = cheap_metric(individual)          # 0-1
    return obj1 + obj2  # obj2が無視される
```

**解決**:
```python
def fitness(individual):
    obj1 = expensive_computation(individual) / 1000  # 正規化
    obj2 = cheap_metric(individual)
    return obj1 + obj2
```

---

### 原則3: 計算効率

**遅い例**:
```python
def fitness(individual):
    # ファイルI/O（非効率）
    with open('data.txt', 'r') as f:
        data = f.read()
    return process(individual, data)
```

**速い例**:
```python
# データを事前ロード
DATA = load_data()

def fitness(individual):
    return process(individual, DATA)
```

---

## 🎯 多目的最適化

### スカラー化（重み付き和）

```python
def multi_objective_fitness(individual):
    # 複数の目的
    accuracy = compute_accuracy(individual)     # 最大化
    complexity = compute_complexity(individual) # 最小化
    training_time = compute_time(individual)    # 最小化

    # 重み付き和
    w1, w2, w3 = 0.6, 0.2, 0.2

    # スケール調整
    accuracy_normalized = accuracy  # 0-1
    complexity_normalized = complexity / 1000
    time_normalized = training_time / 100

    return (w1 * accuracy_normalized
            - w2 * complexity_normalized
            - w3 * time_normalized)
```

---

### パレート最適化

```python
from shinka_evolve import NSGA2

def fitness_vector(individual):
    """複数の目的を返す"""
    accuracy = compute_accuracy(individual)
    complexity = compute_complexity(individual)
    return [accuracy, -complexity]  # 両方最大化

# NSGA-II（非支配ソート遺伝的アルゴリズム）
evolution = NSGA2(
    fitness_function=fitness_vector,
    num_objectives=2,
    num_genes=10
)

pareto_front = evolution.evolve(num_generations=100)

# パレートフロントのプロット
import matplotlib.pyplot as plt
objectives = [fitness_vector(ind) for ind in pareto_front]
acc, comp = zip(*objectives)
plt.scatter(acc, comp)
plt.xlabel('Accuracy')
plt.ylabel('Complexity')
plt.title('Pareto Front')
plt.show()
```

---

## 🚧 制約条件の扱い

### ペナルティ法

```python
def fitness_with_constraint(individual):
    # 目的関数
    objective = compute_objective(individual)

    # 制約条件
    constraint_violation = 0

    # 制約1: 合計が100以下
    if sum(individual) > 100:
        constraint_violation += (sum(individual) - 100) ** 2

    # 制約2: 各要素が正
    for x in individual:
        if x < 0:
            constraint_violation += abs(x) ** 2

    # ペナルティ係数
    penalty = 1000

    return objective - penalty * constraint_violation
```

---

### 修復法

```python
def repair(individual):
    """制約を満たすように修正"""
    # 範囲外の値を修正
    individual = np.clip(individual, 0, 10)

    # 合計が100を超える場合、正規化
    if sum(individual) > 100:
        individual = individual * (100 / sum(individual))

    return individual

def fitness_with_repair(individual):
    # 修復
    individual = repair(individual)

    # 評価
    return compute_objective(individual)
```

---

## 🧠 ドメイン固有の適応度関数

### 例1: ニューラルネットワーク構造探索（NAS）

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# データセット
train_loader, val_loader = load_data()

def nas_fitness(individual):
    """
    individual: [num_layers, neurons_per_layer, dropout_rate, learning_rate]
    """
    num_layers = int(individual[0])
    neurons = int(individual[1])
    dropout = individual[2]
    lr = individual[3]

    # ネットワーク構築
    layers = []
    for i in range(num_layers):
        layers.append(nn.Linear(neurons if i > 0 else 784, neurons))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout))
    layers.append(nn.Linear(neurons, 10))

    model = nn.Sequential(*layers)

    # 訓練
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(5):  # 短期訓練
        for batch in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(batch[0]), batch[1])
            loss.backward()
            optimizer.step()

    # 評価
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in val_loader:
            outputs = model(batch[0])
            _, predicted = torch.max(outputs, 1)
            total += batch[1].size(0)
            correct += (predicted == batch[1]).sum().item()

    accuracy = correct / total

    # ペナルティ（複雑性）
    num_params = sum(p.numel() for p in model.parameters())
    complexity_penalty = num_params / 1e6  # 100万パラメータで1.0

    return accuracy - 0.1 * complexity_penalty

# 進化実行
evolution = Evolution(
    fitness_function=nas_fitness,
    num_genes=4,
    bounds=[
        (1, 5),      # num_layers
        (32, 512),   # neurons
        (0, 0.5),    # dropout
        (1e-4, 1e-2) # learning_rate
    ],
    num_islands=4,
    population_per_island=20
)

best = evolution.evolve(num_generations=20)
print(f"Best architecture: {best}")
print(f"Fitness: {nas_fitness(best):.4f}")
```

---

### 例2: スケジューリング問題

```python
# タスクとリソース
tasks = [
    {'duration': 5, 'dependencies': []},
    {'duration': 3, 'dependencies': [0]},
    {'duration': 7, 'dependencies': [0]},
    {'duration': 2, 'dependencies': [1, 2]},
]

def scheduling_fitness(individual):
    """
    individual: タスクの開始時刻のリスト
    """
    # 制約チェック
    violation = 0

    # 依存関係の制約
    for i, task in enumerate(tasks):
        for dep in task['dependencies']:
            # 依存タスクが完了してから開始
            if individual[i] < individual[dep] + tasks[dep]['duration']:
                violation += 1

    # 目的: 全体の完了時間を最小化
    completion_time = max(
        individual[i] + tasks[i]['duration']
        for i in range(len(tasks))
    )

    # ペナルティ付き目的関数
    return -(completion_time + 1000 * violation)

evolution = Evolution(
    fitness_function=scheduling_fitness,
    num_genes=len(tasks),
    gene_type='real',
    bounds=[(0, 100)] * len(tasks)
)

best = evolution.evolve(num_generations=100)
print(f"Optimal schedule: {best}")
print(f"Completion time: {-scheduling_fitness(best)}")
```

---

### 例3: ポートフォリオ最適化

```python
import numpy as np

# 資産データ
returns = np.array([0.12, 0.18, 0.15, 0.10])  # 期待収益率
risks = np.array([0.05, 0.10, 0.08, 0.04])    # リスク（標準偏差）
correlations = np.array([
    [1.0, 0.3, 0.2, 0.1],
    [0.3, 1.0, 0.4, 0.2],
    [0.2, 0.4, 1.0, 0.3],
    [0.1, 0.2, 0.3, 1.0]
])

def portfolio_fitness(individual):
    """
    individual: 各資産への投資比率 [w1, w2, w3, w4]
    """
    # 正規化（合計を1にする）
    weights = individual / np.sum(individual)

    # 期待収益率
    expected_return = np.dot(weights, returns)

    # ポートフォリオのリスク
    portfolio_risk = np.sqrt(
        weights @ (correlations * np.outer(risks, risks)) @ weights
    )

    # シャープレシオ（リスク調整済みリターン）
    risk_free_rate = 0.02
    sharpe_ratio = (expected_return - risk_free_rate) / portfolio_risk

    return sharpe_ratio

evolution = Evolution(
    fitness_function=portfolio_fitness,
    num_genes=4,
    bounds=[(0, 1)] * 4,  # 投資比率 0-100%
    gene_type='real'
)

best = evolution.evolve(num_generations=100)
optimal_weights = best / np.sum(best)
print(f"Optimal allocation: {optimal_weights}")
print(f"Sharpe ratio: {portfolio_fitness(best):.4f}")
```

---

## 🎯 実践演習

### 演習1: ハイパーパラメータ最適化

**タスク**: scikit-learnのRandomForestのハイパーパラメータを最適化

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import cross_val_score

X, y = load_digits(return_X_y=True)

def fitness(individual):
    n_estimators, max_depth, min_samples_split = individual

    # 整数変換
    n_estimators = int(n_estimators)
    max_depth = int(max_depth) if max_depth > 0 else None
    min_samples_split = int(min_samples_split)

    # モデル
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42
    )

    # 交差検証
    scores = cross_val_score(model, X, y, cv=3, n_jobs=-1)
    return scores.mean()

# あなたのコード
evolution = Evolution(
    # TODO: 設定
)

best = evolution.evolve(num_generations=30)
```

---

### 演習2: 制約付き最適化

**タスク**: 制約条件を満たしながら関数を最適化

```python
def fitness_constrained(individual):
    # 目的: f(x, y) = x^2 + y^2 を最小化
    objective = individual[0]**2 + individual[1]**2

    # 制約: x + y >= 1
    constraint = individual[0] + individual[1] - 1

    if constraint < 0:
        # ペナルティ
        penalty = 1000 * constraint**2
        return -objective - penalty
    else:
        return -objective

# あなたのコード
```

---

## 📝 チェックリスト

- [ ] 適応度関数の設計原則を理解
- [ ] 多目的最適化を実装
- [ ] 制約条件を扱った
- [ ] ドメイン固有の適応度関数を作成
- [ ] 演習問題を解いた

**全てチェックできたら、Part 4に進みましょう！**

---

**作成日**: 2025-11-07
**バージョン**: 1.0
