# Part 7: トラブルシューティング - チュートリアルガイド

**所要時間**: 20分
**難易度**: 中級

---

## 🔧 よくある問題と解決策

### 問題1: インストールエラー

**症状**:
```
ERROR: Could not install shinka-qa
```

**解決策**:
```bash
# 仮想環境を作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 最新pipにアップグレード
pip install --upgrade pip

# 再インストール
pip install -e .
```

---

### 問題2: メモリ不足

**症状**:
```
MemoryError: Unable to allocate...
```

**解決策**:
```yaml
# quality_config.yaml
evolution:
  population_per_island: 4    # 8 → 4
  num_islands: 2              # 4 → 2

optimization:
  memory_limit: 2GB
  store_intermediate: false
```

---

### 問題3: 実行時間が長すぎる

**症状**: 30分以上かかる

**解決策1**: 世代数削減
```yaml
evolution:
  num_generations: 3    # 10 → 3
```

**解決策2**: 早期停止
```yaml
evolution:
  early_stopping:
    enabled: true
    patience: 2
```

**解決策3**: モジュール分割
```bash
# 大きなプロジェクトを分割
shinka-qa evolve --target core/
shinka-qa evolve --target api/
shinka-qa evolve --target utils/
```

---

### 問題4: カバレッジが上がらない

**症状**: 改善 +5%未満

**原因と解決策**:

| 原因 | 解決策 |
|------|--------|
| 世代数不足 | `num_generations: 10` |
| 重み設定不適切 | `coverage: 0.7` に増やす |
| 初期カバレッジが高い | これ以上の改善困難 |
| デッドコードあり | デッドコード削除 |

---

### 問題5: 生成されたテストが不適切

**症状**: 意味のないテストが生成される

**解決策**:
```yaml
# 戦略を絞る
mutation_strategies:
  - add_edge_case
  - add_error_handling
  # 他の戦略を一時的に無効化
```

レビューして不要なテストは削除する。

---

## 🐛 デバッグテクニック

### ログレベル設定

```bash
# デバッグモード
shinka-qa evolve --config quality_config.yaml --log-level DEBUG

# ログファイル出力
shinka-qa evolve --config quality_config.yaml --log-file debug.log
```

### 中間結果の確認

```yaml
output:
  save_intermediate: true
```

```bash
# 各世代の結果を確認
ls results/run_*/best_test_gen*.py
cat results/run_*/best_test_gen3.py
```

---

## 📊 パフォーマンス分析

### プロファイリング

```bash
# 実行時間分析
python -m cProfile -o profile.stats \
  -m shinka_quality.cli.main evolve --config quality_config.yaml

# 結果表示
python -m pstats profile.stats
```

### ボトルネック特定

```python
# プロファイル結果を読む
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(10)
```

---

## 💡 予防策

### 1. 段階的な適用
```bash
# 小規模モジュールから開始
target:
  module: core/single_module.py
```

### 2. 設定の妥当性チェック
```bash
shinka-qa validate --config quality_config.yaml
```

### 3. ドライラン
```bash
shinka-qa evolve --config quality_config.yaml --dry-run
```

---

## 📝 チェックリスト

- [ ] よくある問題の解決策を理解
- [ ] デバッグ方法を習得
- [ ] パフォーマンス分析方法を理解
- [ ] 予防策を実施

---

**作成日**: 2025-11-07
**バージョン**: 1.0
