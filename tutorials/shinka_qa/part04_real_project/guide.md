# Part 4: 実プロジェクト適用 - チュートリアルガイド

**所要時間**: 30分
**難易度**: 中級
**前提知識**: Part 3完了

---

## 🎯 このパートで学ぶこと

1. 実際のプロジェクトへの適用方法
2. プロジェクトタイプ別のベストプラクティス
3. 段階的な適用戦略
4. トラブルシューティング

---

## 📚 プロジェクトタイプ別ガイド

### タイプ1: REST API

**プロジェクト構造**:
```
project/
├── api/
│   ├── routes.py
│   ├── models.py
│   └── validators.py
├── tests/
│   └── test_api.py
└── quality_config.yaml
```

**推奨設定**:
```yaml
target:
  module: api/
  exclude:
    - __pycache__
    - tests/

fitness:
  weights:
    coverage: 0.3
    bug_detection: 0.4    # APIはバグ検出重視
    execution_time: 0.2
    code_quality: 0.1

evolution:
  num_generations: 7
  mutation_strategies:
    - add_edge_case
    - add_error_handling  # HTTPエラー
    - add_mock           # 外部API
    - add_assertion
```

**実行**:
```bash
shinka-qa evolve --config quality_config.yaml --verbose
```

**期待される結果**:
- HTTPステータスコードのテスト（200, 400, 404, 500）
- リクエストバリデーションのテスト
- エラーレスポンスのテスト
- モックを使った外部API呼び出しのテスト

---

### タイプ2: データ処理パイプライン

**推奨設定**:
```yaml
target:
  module: pipeline/

fitness:
  weights:
    coverage: 0.5        # データ処理はカバレッジ重視
    bug_detection: 0.3
    execution_time: 0.1
    code_quality: 0.1

mutation_strategies:
  - add_edge_case        # データ境界値
  - parameterize_test    # 多様なデータ
  - add_error_handling   # データエラー
```

**期待される結果**:
- 空データのテスト
- 大量データのテスト
- 不正データのテスト
- データ型エラーのテスト

---

### タイプ3: Webアプリケーション

**推奨設定**:
```yaml
target:
  module: app/
  exclude:
    - static/
    - templates/
    - migrations/

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2  # フロントエンドテストは速度重視
    code_quality: 0.1

mutation_strategies:
  - add_fixture         # DB、セッション
  - add_mock           # 外部サービス
  - add_error_handling
  - add_assertion
```

---

## 🔄 段階的適用戦略

### フェーズ1: パイロット実施（Week 1-2）

**目標**: 小規模モジュールで成功体験

**手順**:
1. 最も重要な1モジュールを選択
2. 現状を測定
3. 進化実行
4. 結果をレビュー
5. チームに報告

**設定例**:
```yaml
target:
  module: core/user_service.py  # 単一モジュール

evolution:
  num_generations: 5
```

**判断基準**:
- カバレッジ +30%以上 → 成功
- カバレッジ +10%未満 → 設定見直し

---

### フェーズ2: 段階的拡大（Week 3-6）

**目標**: 複数モジュールに拡大

**手順**:
1. 成功モジュールと同じ設定を使用
2. 3-5モジュールに適用
3. 結果を比較
4. 設定を微調整

**設定例**:
```yaml
target:
  module: core/  # ディレクトリ単位
```

---

### フェーズ3: 全体適用（Week 7-12）

**目標**: プロジェクト全体にカバレッジ

**手順**:
1. レガシーコードを除外
2. 全モジュールに適用
3. CI/CDに統合（Part 5）
4. 定期実行設定

**設定例**:
```yaml
target:
  module: src/
  exclude:
    - legacy/
    - deprecated/
```

---

## 💡 ベストプラクティス

### 1. 既存テストの活用

```yaml
test:
  initial_file: tests/test_comprehensive.py  # 最良のテストから開始
```

### 2. モジュール単位で実行

```bash
# ディレクトリごとに設定ファイルを作成
core/quality_config.yaml
api/quality_config.yaml
utils/quality_config.yaml

# それぞれ実行
cd core && shinka-qa evolve --config quality_config.yaml
cd api && shinka-qa evolve --config quality_config.yaml
```

### 3. 結果の記録

```bash
# 実行結果を保存
mkdir -p results/archive/
cp -r results/run_* results/archive/$(date +%Y%m%d)/
```

---

## ❓ よくある質問

### Q1: レガシーコードはどうすべき？

**A**: 段階的に対応

```yaml
# Phase 1: レガシー除外
target:
  exclude:
    - legacy/

# Phase 2: レガシーの一部
target:
  module: legacy/core/

# Phase 3: レガシー全体
target:
  module: legacy/
```

### Q2: 実行時間が長すぎる

**A**: 並列化またはモジュール分割

```bash
# モジュールごとに並列実行
parallel shinka-qa evolve --config {}/quality_config.yaml ::: api core utils
```

---

## 📝 チェックリスト

- [ ] プロジェクトタイプを特定した
- [ ] 適切な設定を作成した
- [ ] パイロット実施を完了した
- [ ] 結果をチームに報告した
- [ ] 段階的拡大計画を立てた

**全てチェックできたら、Part 5 (CI/CD統合) に進みましょう！**

---

**作成日**: 2025-11-07
**バージョン**: 1.0
