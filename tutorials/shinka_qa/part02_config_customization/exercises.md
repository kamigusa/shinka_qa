# Part 2: 設定のカスタマイズ - 演習と解答

**所要時間**: 20分
**難易度**: 入門〜中級
**形式**: 実践演習（設定編集と実行）

---

## 📝 演習の目的

このPartでは、設定ファイルのカスタマイズを実践的に学びます。
手を動かして、重みの調整やパラメータ変更の効果を体感しましょう。

---

## 問題1: 重みの計算（基礎）

### 質問

以下の重み設定には問題があります。何が問題で、どう修正すべきですか？

#### ケースA
```yaml
fitness:
  weights:
    coverage: 0.5
    bug_detection: 0.3
    execution_time: 0.15
    code_quality: 0.1
```

#### ケースB
```yaml
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: -0.1
```

#### ケースC
```yaml
fitness:
  weights:
    coverage: 0.7
    bug_detection: 0.2
    execution_time: 0.1
```

### 解答

#### ケースA: 合計が1.0を超えている

**問題**:
```
0.5 + 0.3 + 0.15 + 0.1 = 1.05
```

合計が1.05で、1.0を超えています。

**修正案1** (execution_timeを調整):
```yaml
fitness:
  weights:
    coverage: 0.5
    bug_detection: 0.3
    execution_time: 0.1      # 0.15 → 0.1
    code_quality: 0.1
  # 合計 = 1.0 ✓
```

**修正案2** (全体的に調整):
```yaml
fitness:
  weights:
    coverage: 0.48           # 0.5 → 0.48
    bug_detection: 0.29      # 0.3 → 0.29
    execution_time: 0.14     # 0.15 → 0.14
    code_quality: 0.09       # 0.1 → 0.09
  # 合計 = 1.0 ✓
```

#### ケースB: 負の値がある

**問題**:
```yaml
code_quality: -0.1  # マイナスは不可
```

重みは0.0〜1.0の範囲でなければなりません。

**修正**:
```yaml
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1        # -0.1 → 0.1
  # 合計 = 1.0 ✓
```

**代替案** (コード品質を重視しない):
```yaml
fitness:
  weights:
    coverage: 0.45           # 0.4 → 0.45
    bug_detection: 0.35      # 0.3 → 0.35
    execution_time: 0.2
    code_quality: 0.0        # ゼロでもOK（重視しない）
  # 合計 = 1.0 ✓
```

#### ケースC: 項目が不足している

**問題**:
```yaml
# code_quality が欠けている
```

4つ全ての項目が必要です。

**修正**:
```yaml
fitness:
  weights:
    coverage: 0.7
    bug_detection: 0.2
    execution_time: 0.1
    code_quality: 0.0        # 追加（重視しない場合は0でOK）
  # 合計 = 1.0 ✓
```

### 検証方法

```bash
# 設定ファイルをバリデート
shinka-qa validate --config quality_config.yaml
```

**期待される出力**:
```
Validating configuration...
✓ Weights sum to 1.0
✓ All values in range [0.0, 1.0]
✓ All required fields present
✓ Configuration is valid
```

---

## 問題2: プロジェクトに合った設定（シナリオ）

### 質問

以下の3つのプロジェクトに対して、最適な設定を作成してください。

#### プロジェクトA
```
名称: 個人の趣味プロジェクト
サイズ: 200行
現在のカバレッジ: 30%
目標: カバレッジを95%以上にしたい
時間制約: 特になし
```

#### プロジェクトB
```
名称: スタートアップのWebアプリ
サイズ: 3,000行
現在のカバレッジ: 45%
問題: 月に2-3回の本番バグ
優先順位: バグを減らしたい
時間制約: CI/CDで5分以内
```

#### プロジェクトC
```
名称: エンタープライズの基幹システム
サイズ: 15,000行
現在のカバレッジ: 25%
問題: レガシーコード、テストがほぼない
優先順位: まずはカバレッジを上げたい
時間制約: 夜間バッチで実行（30分OK）
```

### 解答

#### プロジェクトA: 小規模・カバレッジ重視

```yaml
# quality_config_projectA.yaml

target:
  module: src/
  exclude:
    - __pycache__

test:
  initial_file: tests/test_main.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.7           # カバレッジ最優先
    bug_detection: 0.2
    execution_time: 0.05    # 時間制約なし
    code_quality: 0.05

evolution:
  num_generations: 3        # 小規模なので3世代で十分
  population_per_island: 4  # 小さめ
  num_islands: 2            # 少なめ
  mutation_strategies:
    - add_edge_case
    - parameterize_test

output:
  results_dir: results/
  save_intermediate: true
  generate_report: true
```

**理由**:
- 小規模なので、カバレッジ95%以上が現実的
- 世代数を3に抑えて高速化（1分以内）
- エラーハンドリングは個人プロジェクトでは優先度低

**期待される結果**:
```
Execution Time: 45秒
Initial Coverage: 30%
Final Coverage: 96%
Improvement: +66pt
```

#### プロジェクトB: 中規模・バグ検出重視

```yaml
# quality_config_projectB.yaml

target:
  module: src/
  exclude:
    - __pycache__
    - tests/
    - migrations/

test:
  initial_file: tests/test_suite.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.25
    bug_detection: 0.5      # バグ検出最優先
    execution_time: 0.15    # CI/CDで使うので考慮
    code_quality: 0.1

evolution:
  num_generations: 5        # バランス
  population_per_island: 6
  num_islands: 4
  mutation_strategies:
    - add_edge_case
    - add_error_handling    # バグ検出に重要
    - add_assertion

output:
  results_dir: results/
  save_intermediate: true
  generate_report: true
```

**理由**:
- 本番バグが頻発 → バグ検出を最優先（0.5）
- CI/CDで使う → 実行時間も考慮（0.15）
- 5世代で5分以内に収まる

**期待される結果**:
```
Execution Time: 4分
Initial Coverage: 45%
Final Coverage: 75%
Bug Detection: 0.40 → 0.95
Improvement: バグ検出率 +0.55
```

#### プロジェクトC: 大規模・段階的改善

```yaml
# quality_config_projectC.yaml

target:
  module: src/
  exclude:
    - __pycache__
    - tests/
    - migrations/
    - venv/
    - legacy/              # レガシー部分は一旦除外

test:
  initial_file: tests/test_minimal.py  # 最小限のテストから
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4           # カバレッジ重視
    bug_detection: 0.35     # バグ検出も重要
    execution_time: 0.15    # 30分以内ならOK
    code_quality: 0.1

evolution:
  num_generations: 8        # 大規模なので多めに
  population_per_island: 8  # 大きめ
  num_islands: 6            # 並列化
  mutation_strategies:
    - add_edge_case
    - parameterize_test
    - add_error_handling
    - add_assertion

output:
  results_dir: results/
  save_intermediate: true
  generate_report: true
```

**理由**:
- 大規模 → 世代数を増やして徹底的に改善
- レガシー部分は一旦除外（リスク管理）
- 夜間実行なので30分OK

**期待される結果**:
```
Execution Time: 25分
Initial Coverage: 25%
Final Coverage: 65%
Improvement: +40pt
（レガシー除外分を考慮）
```

**段階的アプローチ**:
```
Phase 1 (Week 1-2):
  - legacy以外を対象
  - カバレッジ 25% → 65%

Phase 2 (Week 3-4):
  - legacyの一部を追加
  - カバレッジ 65% → 75%

Phase 3 (Week 5-8):
  - legacy全体を追加
  - カバレッジ 75% → 85%
```

---

## 問題3: 重みの効果を実験（実践）

### 質問

以下の3つの設定で実際に進化を実行し、結果を比較してください。

#### 設定1: デフォルト
```yaml
fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1
```

#### 設定2: カバレッジ重視
```yaml
fitness:
  weights:
    coverage: 0.7
    bug_detection: 0.15
    execution_time: 0.1
    code_quality: 0.05
```

#### 設定3: バグ検出重視
```yaml
fitness:
  weights:
    coverage: 0.2
    bug_detection: 0.6
    execution_time: 0.1
    code_quality: 0.1
```

### 解答フォーマット

```
【実験結果】

設定1 (デフォルト):
  カバレッジ: ___%
  バグ検出: ___
  実行時間: ___分
  テスト数: ___個

設定2 (カバレッジ重視):
  カバレッジ: ___%
  バグ検出: ___
  実行時間: ___分
  テスト数: ___個

設定3 (バグ検出重視):
  カバレッジ: ___%
  バグ検出: ___
  実行時間: ___分
  テスト数: ___個

【観察】
- 最もカバレッジが高かったのは: ___
- 最もバグ検出が高かったのは: ___
- 最も速かったのは: ___

【結論】
自分のプロジェクトに最適なのは: ___
理由: ___
```

### 解答例

```
【実験結果】

設定1 (デフォルト):
  カバレッジ: 92%
  バグ検出: 1.00
  実行時間: 2.0分
  テスト数: 15個

設定2 (カバレッジ重視):
  カバレッジ: 95%
  バグ検出: 0.95
  実行時間: 3.2分
  テスト数: 24個

設定3 (バグ検出重視):
  カバレッジ: 88%
  バグ検出: 1.00
  実行時間: 2.5分
  テスト数: 18個

【観察】
- 最もカバレッジが高かったのは: 設定2 (95%)
- 最もバグ検出が高かったのは: 設定1と設定3 (1.00)
- 最も速かったのは: 設定1 (2.0分)

【結論】
自分のプロジェクトに最適なのは: 設定1 (デフォルト)
理由:
  - バグ検出が完璧 (1.00)
  - カバレッジも十分高い (92%)
  - 実行時間が最短 (2.0分)
  - バランスが取れている
```

### 実行手順

```bash
# 1. 設定1で実行
cp quality_config_default.yaml quality_config.yaml
shinka-qa evolve --config quality_config.yaml
# 結果を記録

# 2. 設定2で実行
cp quality_config_coverage.yaml quality_config.yaml
shinka-qa evolve --config quality_config.yaml
# 結果を記録

# 3. 設定3で実行
cp quality_config_bug.yaml quality_config.yaml
shinka-qa evolve --config quality_config.yaml
# 結果を記録

# 4. 結果を比較
shinka-qa compare \
  results/default/ \
  results/coverage/ \
  results/bug/
```

---

## 問題4: evolutionパラメータの調整（理解度確認）

### 質問

以下のシナリオに対して、最適な`num_generations`を答えてください。

#### シナリオA
```
プロジェクト: 150行のユーティリティライブラリ
初期カバレッジ: 40%
目標: 90%以上
時間制約: 1分以内
```

#### シナリオB
```
プロジェクト: 4000行のWebアプリ
初期カバレッジ: 35%
目標: 80%以上
時間制約: 5分以内
```

#### シナリオC
```
プロジェクト: 12000行の基幹システム
初期カバレッジ: 20%
目標: できるだけ高く
時間制約: 夜間バッチ（30分OK）
```

### 解答

#### シナリオA: num_generations = 3

**理由**:
- 小規模（150行）なので早く収束する
- 3世代で十分90%以上に到達可能
- 実行時間: 約45秒（1分以内に収まる）

**設定例**:
```yaml
evolution:
  num_generations: 3
  population_per_island: 4
  num_islands: 2
```

**期待される進化**:
```
Generation 0: 40%
Generation 1: 65% (+25pt)
Generation 2: 82% (+17pt)
Generation 3: 93% (+11pt) ✓ 目標達成
```

#### シナリオB: num_generations = 5

**理由**:
- 中規模（4000行）なので標準的な世代数
- 5世代で80%は確実に到達
- 実行時間: 約4分（5分以内に収まる）

**設定例**:
```yaml
evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4
```

**期待される進化**:
```
Generation 0: 35%
Generation 1: 52% (+17pt)
Generation 2: 67% (+15pt)
Generation 3: 77% (+10pt)
Generation 4: 84% (+7pt) ✓ 目標達成
Generation 5: 88% (+4pt)
```

#### シナリオC: num_generations = 10

**理由**:
- 大規模（12000行）なので多めの世代数が必要
- 時間制約が緩い（30分OK）ので徹底的に改善
- 10世代で最大限のカバレッジを目指す

**設定例**:
```yaml
evolution:
  num_generations: 10
  population_per_island: 8
  num_islands: 8
```

**期待される進化**:
```
Generation 0: 20%
Generation 1: 32% (+12pt)
Generation 2: 45% (+13pt)
Generation 3: 56% (+11pt)
Generation 4: 65% (+9pt)
Generation 5: 72% (+7pt)
Generation 6: 77% (+5pt)
Generation 7: 81% (+4pt)
Generation 8: 84% (+3pt)
Generation 9: 86% (+2pt)
Generation 10: 87% (+1pt) → 収束
```

**観察**: 世代8以降、改善が逓減している

---

## 問題5: トラブルシューティング（実践）

### 質問

以下のエラーメッセージが表示されました。原因と解決策を答えてください。

#### エラーA
```
Error: Fitness weights must sum to 1.0 (current sum: 1.2)
```

#### エラーB
```
Error: 'coverage' weight must be in range [0.0, 1.0], got 1.5
```

#### エラーC
```
Error: Missing required field 'bug_detection' in fitness weights
```

#### エラーD
```
Evolution took 45 minutes but only improved coverage by 2%
Warning: Consider reducing num_generations or population_size
```

### 解答

#### エラーA: 重みの合計が1.0でない

**原因**:
```yaml
fitness:
  weights:
    coverage: 0.5
    bug_detection: 0.4
    execution_time: 0.2
    code_quality: 0.1
  # 合計 = 1.2 ❌
```

**解決策**:
```yaml
fitness:
  weights:
    coverage: 0.42        # 0.5 × (1.0/1.2) = 0.42
    bug_detection: 0.33   # 0.4 × (1.0/1.2) = 0.33
    execution_time: 0.17  # 0.2 × (1.0/1.2) = 0.17
    code_quality: 0.08    # 0.1 × (1.0/1.2) = 0.08
  # 合計 = 1.0 ✓
```

**自動計算スクリプト**:
```python
# normalize_weights.py
weights = {
    'coverage': 0.5,
    'bug_detection': 0.4,
    'execution_time': 0.2,
    'code_quality': 0.1
}

total = sum(weights.values())
print(f"Current sum: {total}")

normalized = {k: v/total for k, v in weights.items()}
print("\nNormalized weights:")
for k, v in normalized.items():
    print(f"  {k}: {v:.2f}")

print(f"\nNew sum: {sum(normalized.values()):.2f}")
```

#### エラーB: 重みが範囲外

**原因**:
```yaml
fitness:
  weights:
    coverage: 1.5  # 1.0を超えている
```

**解決策**:
```yaml
fitness:
  weights:
    coverage: 0.7   # 最大1.0まで
    bug_detection: 0.15
    execution_time: 0.1
    code_quality: 0.05
  # 合計 = 1.0 ✓
```

**理解**:
- 重みは相対的な重要度
- 1.5 = 「1.5倍重要」という意味ではない
- 0.7 = 「全体の70%の重要度」という意味

#### エラーC: 必須項目が欠けている

**原因**:
```yaml
fitness:
  weights:
    coverage: 0.5
    bug_detection: 0.3
    execution_time: 0.2
    # code_quality がない
```

**解決策**:
```yaml
fitness:
  weights:
    coverage: 0.5
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.0  # 重視しない場合は0でもOK
  # 合計 = 1.0 ✓
```

#### エラーD: 実行時間に対して改善が小さい

**原因**:
```yaml
evolution:
  num_generations: 20   # 多すぎる
  population_per_island: 10  # 大きすぎる
```

初期カバレッジが既に高い（例: 85%）場合、
改善余地が小さく、世代数を増やしても効果がない。

**解決策1**: 世代数を減らす
```yaml
evolution:
  num_generations: 5    # 20 → 5
  population_per_island: 6  # 10 → 6
```

**解決策2**: 早期停止を有効化
```yaml
evolution:
  num_generations: 20
  early_stopping:
    enabled: true
    patience: 3  # 3世代改善なしで停止
    min_improvement: 0.01  # 最小改善率 1%
```

**解決策3**: 目標が達成されていないか確認
```bash
# 目標カバレッジを確認
# 85% → 87% (+2%) でも、目標が90%なら継続すべき
```

---

## 問題6: 設定の最適化（応用）

### 質問

以下のプロジェクトに対して、段階的な改善計画を立ててください。

#### プロジェクト情報
```
名称: オンライン決済システム
サイズ: 8,000行
現在のカバレッジ: 15%
現在のバグ検出: 0.20
目標: カバレッジ 90%、バグ検出 1.00
期間: 3ヶ月
チーム: 3人
```

### 解答例

#### 段階的改善計画（3ヶ月）

**Week 1-2: Phase 1 - 基礎固め**

目標: カバレッジ 15% → 40%

```yaml
# quality_config_phase1.yaml

target:
  module: src/core/  # まずはコアモジュールから
  exclude:
    - __pycache__
    - tests/
    - legacy/  # レガシー部分は後回し

fitness:
  weights:
    coverage: 0.6      # カバレッジ重視
    bug_detection: 0.25
    execution_time: 0.1
    code_quality: 0.05

evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4
```

**期待される結果**:
```
Coverage: 15% → 42%
Bug Detection: 0.20 → 0.45
Time: 5分
```

**Week 3-4: Phase 2 - バグ検出強化**

目標: バグ検出 0.45 → 0.75

```yaml
# quality_config_phase2.yaml

target:
  module: src/core/
  exclude:
    - __pycache__
    - tests/
    - legacy/

fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.5  # バグ検出重視に変更
    execution_time: 0.1
    code_quality: 0.1

evolution:
  num_generations: 7  # 増やす
  population_per_island: 6
  num_islands: 4
  mutation_strategies:
    - add_edge_case
    - add_error_handling  # エラー処理を追加
    - add_assertion
```

**期待される結果**:
```
Coverage: 42% → 55%
Bug Detection: 0.45 → 0.78
Time: 7分
```

**Week 5-8: Phase 3 - カバレッジ拡大**

目標: カバレッジ 55% → 75%

```yaml
# quality_config_phase3.yaml

target:
  module: src/  # 全モジュールに拡大
  exclude:
    - __pycache__
    - tests/
    - legacy/  # まだレガシーは除外

fitness:
  weights:
    coverage: 0.5      # カバレッジ重視に戻す
    bug_detection: 0.3
    execution_time: 0.15
    code_quality: 0.05

evolution:
  num_generations: 8
  population_per_island: 8
  num_islands: 6  # 並列化
```

**期待される結果**:
```
Coverage: 55% → 77%
Bug Detection: 0.78 → 0.90
Time: 15分
```

**Week 9-12: Phase 4 - レガシー対応**

目標: カバレッジ 77% → 90%、バグ検出 1.00

```yaml
# quality_config_phase4.yaml

target:
  module: src/  # 全モジュール（レガシー含む）
  exclude:
    - __pycache__
    - tests/

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.4  # バランス型
    execution_time: 0.1
    code_quality: 0.1

evolution:
  num_generations: 10  # 徹底的に
  population_per_island: 8
  num_islands: 8
```

**期待される結果**:
```
Coverage: 77% → 91%
Bug Detection: 0.90 → 1.00
Time: 25分
```

#### マイルストーン

| Phase | 期間 | カバレッジ目標 | バグ検出目標 | 実施内容 |
|-------|------|--------------|------------|---------|
| 1 | Week 1-2 | 15% → 40% | 0.20 → 0.45 | コアモジュール |
| 2 | Week 3-4 | 40% → 55% | 0.45 → 0.78 | バグ検出強化 |
| 3 | Week 5-8 | 55% → 77% | 0.78 → 0.90 | 全モジュール拡大 |
| 4 | Week 9-12 | 77% → 91% | 0.90 → 1.00 | レガシー対応 |

#### リソース配分

**Week 1-2**:
- エンジニアA: 設定作成と実行
- エンジニアB: 生成されたテストのレビュー
- エンジニアC: CI/CD統合

**Week 3-4**:
- 全員: バグ検出テストのレビューと修正
- 本番バグの再現テスト追加

**Week 5-8**:
- 全員: モジュールごとに分担してテスト改善

**Week 9-12**:
- 全員: レガシーコードのテスト追加
- リファクタリングも並行実施

---

## 📊 演習の総括

### 採点基準

| 問題 | 配点 | あなたの得点 |
|------|------|--------------:|
| 問題1 | 15点 | ___ |
| 問題2 | 20点 | ___ |
| 問題3 | 20点 | ___ |
| 問題4 | 15点 | ___ |
| 問題5 | 15点 | ___ |
| 問題6 | 15点 | ___ |
| **合計** | **100点** | ___ |

### 評価

- **90点以上**: 優秀！設定を自在に操れます。Part 3へ
- **70-89点**: 良好。実践で経験を積みながらPart 3へ
- **50-69点**: 基本は理解。もう一度実験を
- **49点以下**: ガイドを再読し、講師に質問を

---

## 🎯 実践チェックリスト

### 基本操作
- [ ] 設定ファイルの5セクションを理解した
- [ ] 重みの合計を1.0にできる
- [ ] 重みの調整で結果が変わることを確認した
- [ ] バリデーションコマンドを実行した

### 実践演習
- [ ] カバレッジ重視設定を作成して実行した
- [ ] バグ検出重視設定を作成して実行した
- [ ] 複数設定で結果を比較した
- [ ] 自分のプロジェクトに合った設定を作成した

### トラブルシューティング
- [ ] 重みの合計エラーを解決できる
- [ ] 範囲外エラーを解決できる
- [ ] 欠落項目エラーを解決できる
- [ ] 実行時間vs改善のバランスを理解した

**全てチェックできたら、Part 3に進みましょう！**

---

## 💡 発展課題（オプション）

### 課題1: A/Bテスト

2つの異なる設定で実験し、どちらが優れているか統計的に検証してください。

```bash
# 設定Aで10回実行
for i in {1..10}; do
  shinka-qa evolve --config config_A.yaml
done

# 設定Bで10回実行
for i in {1..10}; do
  shinka-qa evolve --config config_B.yaml
done

# 結果を比較
shinka-qa analyze-variance results/
```

### 課題2: 最適化アルゴリズム

グリッドサーチで最適な重みを見つけてください。

```python
# optimize_weights.py
import itertools
import subprocess
import json

coverage_weights = [0.3, 0.4, 0.5, 0.6, 0.7]
bug_weights = [0.1, 0.2, 0.3, 0.4]

results = []

for cov_w in coverage_weights:
    for bug_w in bug_weights:
        exec_w = 0.2
        qual_w = 1.0 - cov_w - bug_w - exec_w

        if qual_w < 0:
            continue

        # 設定を更新
        config = {
            'fitness': {
                'weights': {
                    'coverage': cov_w,
                    'bug_detection': bug_w,
                    'execution_time': exec_w,
                    'code_quality': qual_w
                }
            }
        }

        # 実行
        result = run_evolution(config)
        results.append({
            'config': config,
            'coverage': result['coverage'],
            'bug_detection': result['bug_detection']
        })

# 最良の設定を表示
best = max(results, key=lambda x: x['coverage'] + x['bug_detection'])
print(f"Best config: {best['config']}")
```

### 課題3: CI/CD統合

最適化した設定をCI/CDに統合してください。

```yaml
# .github/workflows/test.yml
name: Test with Shinka QA

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install shinka-qa

      - name: Run evolution
        run: |
          shinka-qa evolve --config quality_config.yaml

      - name: Check coverage
        run: |
          # カバレッジが80%未満ならfail
          python check_coverage.py --min 80
```

---

## 🔗 次のステップ

### Part 3で学ぶこと

**変異戦略の詳細**:

1. **add_edge_case**: 境界値テストの生成
2. **parameterize_test**: パラメータ化の実践
3. **add_error_handling**: エラーハンドリングのパターン
4. **add_assertion**: アサーション改善の技法

### 準備

```bash
# Part 3のサンプルを確認
cd examples/mutation_strategies/
ls -la

# 各戦略のREADMEを読む
cat add_edge_case/README.md
```

準備ができたら、Part 3に進みましょう！

---

**作成日**: 2025-11-07
**更新日**: 2025-11-07
**バージョン**: 1.0
