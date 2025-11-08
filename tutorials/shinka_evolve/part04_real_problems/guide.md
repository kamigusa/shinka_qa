# Part 4: 実問題への適用 - チュートリアルガイド

**所要時間**: 40分
**難易度**: 上級

---

## 🎯 このパートで学ぶこと

1. 実世界の最適化問題への適用
2. 大規模問題の扱い
3. ハイパーパラメータ自動チューニング
4. ベストプラクティス

---

## 🤖 ケース1: 機械学習ハイパーパラメータ最適化

### 問題設定

LightGBMのハイパーパラメータを最適化して、MNIST分類の精度を最大化する。

```python
import lightgbm as lgb
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score
from shinka_evolve import Evolution
import numpy as np

# データロード
X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

def lightgbm_fitness(individual):
    """
    individual: [learning_rate, num_leaves, max_depth,
                 min_child_samples, subsample, colsample_bytree]
    """
    learning_rate, num_leaves, max_depth, min_child_samples, subsample, colsample_bytree = individual

    # パラメータ変換
    params = {
        'objective': 'multiclass',
        'num_class': 10,
        'metric': 'multi_logloss',
        'learning_rate': learning_rate,
        'num_leaves': int(num_leaves),
        'max_depth': int(max_depth),
        'min_child_samples': int(min_child_samples),
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'verbose': -1
    }

    # 交差検証
    try:
        dtrain = lgb.Dataset(X_train, label=y_train)
        cv_results = lgb.cv(
            params,
            dtrain,
            num_boost_round=100,
            nfold=3,
            early_stopping_rounds=10,
            verbose_eval=False
        )

        # 最良スコア
        best_score = max(cv_results['valid multi_logloss-mean'])
        return -best_score  # 最小化なので負にする

    except Exception as e:
        # エラー時は低い適応度
        return -10.0

# 進化設定
evolution = Evolution(
    fitness_function=lightgbm_fitness,
    num_genes=6,
    gene_type='real',
    bounds=[
        (0.001, 0.3),   # learning_rate
        (10, 200),      # num_leaves
        (3, 15),        # max_depth
        (5, 100),       # min_child_samples
        (0.5, 1.0),     # subsample
        (0.5, 1.0)      # colsample_bytree
    ],
    num_islands=4,
    population_per_island=20,
    mutation_rate=0.1
)

# 進化実行
print("Optimizing LightGBM hyperparameters...")
best = evolution.evolve(num_generations=50, verbose=True)

print(f"\nBest hyperparameters:")
print(f"  learning_rate: {best[0]:.4f}")
print(f"  num_leaves: {int(best[1])}")
print(f"  max_depth: {int(best[2])}")
print(f"  min_child_samples: {int(best[3])}")
print(f"  subsample: {best[4]:.4f}")
print(f"  colsample_bytree: {best[5]:.4f}")
print(f"\nBest fitness: {lightgbm_fitness(best):.6f}")

# 最終モデルで評価
final_params = {
    'objective': 'multiclass',
    'num_class': 10,
    'learning_rate': best[0],
    'num_leaves': int(best[1]),
    'max_depth': int(best[2]),
    'min_child_samples': int(best[3]),
    'subsample': best[4],
    'colsample_bytree': best[5]
}

final_model = lgb.train(final_params, lgb.Dataset(X_train, label=y_train), num_boost_round=100)
test_pred = final_model.predict(X_test)
test_accuracy = (np.argmax(test_pred, axis=1) == y_test).mean()

print(f"\nTest accuracy: {test_accuracy:.4f}")
```

---

## 📊 ケース2: ニューラルネットワーク構造探索

### 問題設定

CNNの構造（層数、フィルター数など）を最適化する。

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# データロード
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('./data', train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000)

def build_cnn(individual):
    """
    individual: [num_conv_layers, num_filters, kernel_size, dropout, learning_rate]
    """
    num_conv_layers = int(individual[0])
    num_filters = int(individual[1])
    kernel_size = int(individual[2])
    dropout = individual[3]
    lr = individual[4]

    layers = []
    in_channels = 1

    # 畳み込み層
    for i in range(num_conv_layers):
        layers.append(nn.Conv2d(in_channels, num_filters, kernel_size))
        layers.append(nn.ReLU())
        layers.append(nn.MaxPool2d(2))
        in_channels = num_filters

    layers.append(nn.Flatten())

    # 全結合層のサイズを計算
    dummy_input = torch.zeros(1, 1, 28, 28)
    with torch.no_grad():
        for layer in layers:
            dummy_input = layer(dummy_input)
        fc_input_size = dummy_input.shape[1]

    layers.append(nn.Linear(fc_input_size, 128))
    layers.append(nn.ReLU())
    layers.append(nn.Dropout(dropout))
    layers.append(nn.Linear(128, 10))

    return nn.Sequential(*layers), lr

def cnn_fitness(individual):
    """CNNを訓練して評価"""
    try:
        model, lr = build_cnn(individual)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)

        # 訓練（エポック数を制限）
        model.train()
        for epoch in range(3):  # 短期訓練
            for batch_idx, (data, target) in enumerate(train_loader):
                if batch_idx > 50:  # 一部のバッチのみ
                    break
                data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()

        # 評価
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                pred = output.argmax(dim=1)
                correct += pred.eq(target).sum().item()
                total += target.size(0)

        accuracy = correct / total

        # モデルサイズペナルティ
        num_params = sum(p.numel() for p in model.parameters())
        size_penalty = num_params / 1e6  # 100万パラメータで1.0

        return accuracy - 0.05 * size_penalty

    except Exception as e:
        print(f"Error: {e}")
        return 0.0

# 進化実行
evolution = Evolution(
    fitness_function=cnn_fitness,
    num_genes=5,
    bounds=[
        (1, 3),      # num_conv_layers
        (16, 64),    # num_filters
        (3, 5),      # kernel_size
        (0, 0.5),    # dropout
        (1e-4, 1e-2) # learning_rate
    ],
    num_islands=2,  # GPU使用の場合は少なめ
    population_per_island=10
)

best = evolution.evolve(num_generations=10, verbose=True)
print(f"\nBest CNN architecture: {best}")
print(f"Best accuracy: {cnn_fitness(best):.4f}")
```

---

## 🎮 ケース3: ゲームAIの最適化

### 問題設定

CartPole環境でニューラルネットワークポリシーを最適化する。

```python
import gym
import numpy as np

def create_policy(weights):
    """重みからポリシーを作成"""
    def policy(observation):
        # 単純なニューラルネットワーク
        hidden = np.tanh(observation @ weights[:4].reshape(4, 8))
        output = hidden @ weights[4:].reshape(8, 2)
        return np.argmax(output)
    return policy

def evaluate_policy(weights, num_episodes=5):
    """ポリシーを評価"""
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

    env.close()
    return total_reward / num_episodes

def cartpole_fitness(individual):
    """適応度関数"""
    return evaluate_policy(individual)

# 進化実行
evolution = Evolution(
    fitness_function=cartpole_fitness,
    num_genes=4*8 + 8*2,  # 重みの数
    gene_type='real',
    bounds=[(-1, 1)] * (4*8 + 8*2),
    num_islands=4,
    population_per_island=30
)

best = evolution.evolve(num_generations=50, verbose=True)
print(f"\nBest average reward: {cartpole_fitness(best):.2f}")

# ベストポリシーを可視化
env = gym.make('CartPole-v1', render_mode='human')
observation = env.reset()
for _ in range(500):
    env.render()
    action = create_policy(best)(observation)
    observation, reward, done, _ = env.step(action)
    if done:
        break
env.close()
```

---

## 🏆 ベストプラクティス

### 1. 適応度関数の高速化

```python
# キャッシング
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_fitness(individual_tuple):
    individual = np.array(individual_tuple)
    return compute_fitness(individual)

def fitness(individual):
    return cached_fitness(tuple(individual))
```

---

### 2. 早期停止

```python
evolution = Evolution(
    fitness_function=fitness,
    early_stopping=True,
    patience=10,
    min_improvement=0.001
)
```

---

### 3. ログ記録

```python
import logging

logging.basicConfig(
    filename='evolution.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def fitness_with_logging(individual):
    result = compute_fitness(individual)
    logging.info(f"Fitness: {result:.6f}, Individual: {individual}")
    return result
```

---

### 4. チェックポイント

```python
import pickle

def evolve_with_checkpoint(evolution, num_generations):
    for gen in range(num_generations):
        evolution.evolve(num_generations=1)

        # 10世代ごとにチェックポイント
        if gen % 10 == 0:
            with open(f'checkpoint_gen{gen}.pkl', 'wb') as f:
                pickle.dump(evolution, f)

    return evolution.best_individual()
```

---

## 📝 チェックリスト

- [ ] 機械学習ハイパーパラメータ最適化を実装
- [ ] ニューラルネットワーク構造探索を試した
- [ ] ゲームAIを最適化した
- [ ] ベストプラクティスを理解
- [ ] 自分の問題に適用できる

**おめでとうございます！Shinka Evolveをマスターしました！**

---

## 🎯 次のステップ

1. **自分の問題に適用**
   - 実際の業務で使ってみる
   - 結果を測定する

2. **コミュニティに貢献**
   - 成功事例を共有
   - 新しい適応度関数を公開

3. **高度なトピック**
   - 共進化
   - ニッチング
   - 適応的パラメータ制御

---

**作成日**: 2025-11-07
**バージョン**: 1.0
