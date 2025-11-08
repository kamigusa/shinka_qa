# Part 9: ケーススタディ - チュートリアルガイド

**所要時間**: 15分
**難易度**: 全レベル

---

## 🎯 学ぶこと

実際の成功事例から学ぶベストプラクティス

---

## 💼 ケース1: 銀行システム

**企業**: 大手金融機関
**プロジェクト**: オンラインバンキングシステム
**規模**: 50,000行

### 課題
- レガシーコード（15年以上）
- カバレッジ 18%
- 月に10-15件の本番バグ

### 適用戦略

**Phase 1 (Month 1-2)**: コアモジュール
```yaml
target:
  module: core/transaction/
  exclude:
    - legacy/deprecated/

fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.5    # バグ検出最優先
    execution_time: 0.1
    code_quality: 0.1

evolution:
  num_generations: 10
```

**結果**:
- カバレッジ: 18% → 45% (+27pt)
- バグ検出: 0.3 → 0.85
- 本番バグ: 15件/月 → 8件/月

**Phase 2 (Month 3-6)**: 全モジュール
```yaml
target:
  module: src/
  exclude:
    - legacy/deprecated/
```

**最終結果**:
- カバレッジ: 45% → 78% (+60pt total)
- バグ検出: 0.85 → 1.0
- 本番バグ: 8件/月 → 2件/月（87%削減）

### ROI
- **投資**: ¥5,000,000（ライセンス、研修、工数）
- **効果**: ¥30,000,000/年（バグ対応コスト削減）
- **ROI**: 6倍

---

## 🛒 ケース2: Eコマース企業

**企業**: 中規模EC事業者
**プロジェクト**: カート・決済システム
**規模**: 8,000行

### 課題
- カバレッジ 35%
- 決済処理のバグ頻発
- テストが遅い（15分）

### 適用戦略

```yaml
target:
  module: cart/
  module: payment/

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.4
    execution_time: 0.1    # テスト高速化
    code_quality: 0.1

mutation_strategies:
  - add_edge_case
  - add_error_handling
  - add_mock              # 外部API高速化
```

### 結果
- カバレッジ: 35% → 88%
- テスト実行時間: 15分 → 3分（80%削減）
- 決済バグ: ゼロ（6ヶ月間）

### 学び
- モックの活用でテスト高速化
- 決済処理のエッジケース網羅
- CI/CD統合で継続的改善

---

## 🚀 ケース3: スタートアップ

**企業**: SaaS系スタートアップ
**プロジェクト**: REST API
**規模**: 3,000行

### 課題
- 急成長でテスト追いつかない
- カバレッジ要件（80%）未達
- リソース不足（2名）

### 適用戦略

```yaml
# 自動化重視
target:
  module: api/

fitness:
  weights:
    coverage: 0.6    # カバレッジ最優先
    bug_detection: 0.2
    execution_time: 0.1
    code_quality: 0.1

evolution:
  num_generations: 5
```

### CI/CD統合

```yaml
# .github/workflows/test.yml
- name: Shinka QA
  run: shinka-qa evolve --config quality_config.yaml

- name: Check 80% coverage
  run: python check_coverage.py --min 80
```

### 結果
- カバレッジ: 42% → 85%（要件達成）
- 開発速度: 維持（自動化のおかげ）
- テスト工数: 50%削減

### 学び
- CI/CD統合で自動化
- 少人数でも高品質維持
- 早期導入が効果的

---

## 📊 共通の成功要因

### 1. 段階的適用
すべてのケースで段階的に適用

### 2. バグ検出重視
重要システムでは`bug_detection`の重みを高く

### 3. CI/CD統合
継続的改善のためCI/CD統合が必須

### 4. チーム教育
ツールだけでなくプロセスも改善

### 5. 測定と改善
定期的にメトリクスを測定し改善

---

## 💡 適用のヒント

### プロジェクトタイプ別

**金融・決済系**:
```yaml
fitness:
  weights:
    bug_detection: 0.5    # 最優先
    coverage: 0.3
```

**API・Web系**:
```yaml
mutation_strategies:
  - add_mock           # 外部依存
  - add_error_handling # HTTPエラー
```

**データ処理系**:
```yaml
mutation_strategies:
  - add_edge_case      # データ境界
  - parameterize_test  # 多様なデータ
```

---

## 📝 チェックリスト

- [ ] ケーススタディを読んだ
- [ ] 自プロジェクトとの類似点を特定
- [ ] 適用戦略のアイデアを得た
- [ ] ROI測定方法を理解

---

**作成日**: 2025-11-07
**バージョン**: 1.0
