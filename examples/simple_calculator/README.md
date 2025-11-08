# Simple Calculator Example - Shinka Quality クイックスタート

このサンプルは、Shinka Qualityを使った自動テスト生成の基本的な使い方を示します。シンプルな電卓プログラムに対して、進化的アルゴリズムでテストコードを自動生成し、カバレッジを劇的に向上させます。

## 概要

**モジュール**: `calculator.py` - 四則演算を行うシンプルな電卓
**初期状態**: 基本テスト3個（カバレッジ41%）
**最終結果**: 自動生成テスト35個（カバレッジ100%）

## ファイル構成

```
simple_calculator/
├── calculator.py                    # 電卓の実装
├── calculator_buggy.py              # バグ混入版（テスト用）
├── test_calculator_initial.py       # 初期テストスイート
├── quality_config_local.yaml        # Shinka Quality設定ファイル
└── README.md                        # このファイル
```

## クイックスタート

### 1. 初期テストの実行（ベースライン測定）

まず、初期状態のテストがどのくらいカバレッジがあるか確認します：

```bash
cd examples/simple_calculator

# 初期テストを実行してカバレッジを測定
pytest test_calculator_initial.py -v --cov=calculator --cov-report=term-missing

# 期待結果: 3件成功、カバレッジ約41%
```

### 2. テストコードの自動生成（進化的アルゴリズム）

Shinka Qualityを使って、テストコードを自動的に進化させます：

```bash
# テンプレートベース（無料）で進化
python -m shinka_qa.cli.main evolve --config quality_config_local.yaml

# LLM使用（より高品質だがAPI費用がかかる）で進化
python -m shinka_qa.cli.main evolve --config quality_config_local.yaml --llm

# 詳細ログ付きで実行
python -m shinka_qa.cli.main evolve --config quality_config_local.yaml --verbose
```

**実行時間**: 約2-5分（10世代、4島、各20個体の進化）

**期待される進化の様子**:
```
Generation 1/10
  Best Fitness: 0.568
  Coverage: 68.0%
  Mode: Template-based

Generation 5/10
  Best Fitness: 0.857
  Coverage: 92.0%
  Mode: Template-based

Generation 8/10
  Best Fitness: 0.998
  Coverage: 100.0%
  Mode: Template-based

[*] Perfect solution achieved at generation 8!
   Coverage: 100%, Bug Detection: 100%, Fitness: 0.998
   Early stopping - skipping remaining 2 generations
```

### 3. 生成されたテストの実行

進化が完了すると、`results/`ディレクトリに最適なテストコードが保存されます：

```bash
# 生成されたテストを実行
pytest results/best_test.py -v --cov=calculator --cov-report=term-missing

# 期待結果: 35件前後成功、カバレッジ100%
```

### 4. バグ検出能力の確認（オプション）

初期テストと進化後テストのバグ検出能力を比較します：

```bash
# 元のファイルをバックアップ
cp calculator.py calculator_backup.py

# バグ混入版に置き換え
cp calculator_buggy.py calculator.py

# 初期テストでバグ検出（一部のバグのみ検出）
pytest test_calculator_initial.py -v

# 進化後テストでバグ検出（すべてのバグを検出）
pytest results/best_test.py -v

# 元に戻す
mv calculator_backup.py calculator.py
```

## 進化パラメータの調整

`quality_config_local.yaml`を編集することで、進化の動作をカスタマイズできます：

```yaml
evolution:
  generations: 30              # 世代数（多いほど時間がかかるが品質向上）
  population_size: 20          # 各島の個体数
  num_islands: 4               # 島の数（並列探索）
  migration_interval: 10       # 移住間隔（世代）
```

**推奨設定**:
- **クイック試行**: `generations: 5`, `population_size: 10`, `num_islands: 2`
- **標準**: `generations: 10`, `population_size: 20`, `num_islands: 4`（デフォルト）
- **高品質**: `generations: 30`, `population_size: 30`, `num_islands: 8`

## LLM使用について

### テンプレートベース（デフォルト、無料）

```bash
python -m shinka_qa.cli.main evolve --config quality_config_local.yaml
```

- ✅ **無料**: API費用なし
- ✅ **高速**: 数分で完了
- ✅ **十分高品質**: ほとんどのケースで100%カバレッジ達成
- ⚠️ **制限**: 複雑なロジックでは限界がある場合も

### ハイブリッドモード（LLM併用、推奨）

```bash
python -m shinka_qa.cli.main evolve --config quality_config_local.yaml --llm
```

- 🧬 **最初はテンプレート**: 無料でカバレッジを上げる
- 🚀 **サチュレーション検出**: カバレッジが伸び悩んだらLLMに切り替え
- 💰 **コスト最適**: 必要な時だけLLMを使用（約$0.01-0.10）
- ✨ **最高品質**: 複雑なエッジケースも網羅

**必要な設定**:
1. `.env`ファイルにAPIキーを設定（プロジェクトルートに配置）
   ```bash
   # いずれか1つ以上を設定（複数可）
   GEMINI_API_KEY=your-key           # 最安 ($0.075/1M tokens)
   ANTHROPIC_API_KEY=your-key        # コスパ ($0.25/1M tokens)
   OPENAI_API_KEY=your-key           # 従来 ($0.50/1M tokens)
   ```

2. `quality_config_local.yaml`でプロバイダーを設定
   ```yaml
   llm:
     provider: "gemini"              # gemini, anthropic, openai, auto
     model: "gemini-2.5-flash"       # 使用モデル
   ```

## 進化的アルゴリズムの仕組み

### 世代（Generations）
テストコードを繰り返し改良していきます：
```
世代1: カバレッジ68% → 世代5: 92% → 世代8: 100% ✨
```

### 島モデル（Islands）
複数の独立した進化グループが並列に探索し、良い個体を交換します：
```
🏝️ 島1: エッジケース重視
🏝️ 島2: 境界値テスト重視
🏝️ 島3: 例外ハンドリング重視
🏝️ 島4: パラメータ化テスト重視
```

### アーリーストッピング
カバレッジ100%、バグ検出100%、適応度≈100%を達成すると自動的に終了します。

## よくある質問

### Q: 生成されたテストはそのまま使えますか？

**A**: 基本的には使えますが、以下のレビューを推奨します：
- テストの意図が明確か確認
- ドメイン固有のアサーションを追加
- テスト名をわかりやすく変更

### Q: 既存のテストは削除されますか？

**A**: いいえ。Shinka Qualityは**常に追加のみ**で、既存のテストは保持されます。

### Q: どのくらいの時間がかかりますか？

**A**: このシンプルな電卓の場合：
- テンプレートベース: 2-5分
- LLMハイブリッド: 5-10分

より大規模なモジュールでは、10-30分程度かかる場合があります。

## 次のステップ

1. **より複雑な例を試す**: `examples/banking_system/`を確認
2. **自分のコードで試す**: 自分のプロジェクトに適用
3. **CI/CDに組み込む**: GitHubActionsなどで定期的に実行

## 関連ドキュメント

- [Shinka Quality完全ガイド](../../docs/COMPLETE_TUTORIAL_GUIDE.md)
- [API リファレンス](../../docs/api_reference.md)
- [マルチプロバイダー設定](../../docs/multi_provider_setup.md)
- [変異戦略の詳細](../../docs/mutation_strategies.md)

---

**生成ツール**: Shinka Quality v1.0
**ライセンス**: MIT
