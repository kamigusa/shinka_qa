# Shinka QA (Quality Assurance) チュートリアル

**バージョン**: 1.0
**最終更新**: 2025-11-07
**所要時間**: 3時間（全10パート）

---

## 🎯 チュートリアルの目的

このチュートリアルは、**Shinka QA (Quality Assurance)**を使ってテスト品質を劇的に向上させる方法を、実践を通じて学ぶためのものです。

### 学習目標

このチュートリアルを完了すると、以下ができるようになります：

- ✅ Shinka QAをインストールして実行できる
- ✅ 設定ファイルをカスタマイズして最適化できる
- ✅ 8つの変異戦略を使い分けられる
- ✅ 実際のプロジェクトに適用できる
- ✅ CI/CDパイプラインに統合できる
- ✅ 高度な最適化技法を実践できる
- ✅ トラブルシューティングができる
- ✅ エンタープライズ環境で展開できる

---

## 📚 チュートリアル構成

### Phase 1: 基礎（必須）

実際にShinka QAを動かし、基本的な使い方をマスターします。

| Part | タイトル | 時間 | 内容 | 前提知識 |
|------|----------|------|------|---------|
| **[Part 0](part00_introduction/)** | イントロダクション | 10分 | なぜテスト品質が重要か、Shinka QAとは何か | なし |
| **[Part 1](part01_first_evolution/)** | はじめての進化 | 15分 | インストールから最初の進化実行まで | Part 0 |
| **[Part 2](part02_config_customization/)** | 設定のカスタマイズ | 20分 | 設定ファイルの詳細と重みの調整 | Part 1 |

**Phase 1完了後の状態**:
- Shinka QAを自由に実行できる
- 自分のプロジェクトに合わせた設定ができる
- カバレッジを2倍以上に改善できる

---

### Phase 2: 実践（推奨）

変異戦略を理解し、実際のプロジェクトに適用します。

| Part | タイトル | 時間 | 内容 | 前提知識 |
|------|----------|------|------|---------|
| **Part 3** | 変異戦略の理解 | 25分 | 8つの変異戦略の詳細と使い分け | Part 2 |
| **Part 4** | 実プロジェクト適用 | 30分 | 実際のコードベースでの適用例 | Part 3 |

**Phase 2完了後の状態**:
- 変異戦略を戦略的に選択できる
- 実プロジェクトで成果を出せる
- チームに展開できる

---

### Phase 3: 統合と自動化（推奨）

CI/CDに統合し、継続的にテスト品質を向上させます。

| Part | タイトル | 時間 | 内容 | 前提知識 |
|------|----------|------|------|---------|
| **Part 5** | CI/CD統合 | 25分 | GitHub Actions、GitLab CI等への統合 | Part 4 |
| **Part 6** | 高度な使い方 | 30分 | カスタム戦略、プラグイン、API | Part 5 |
| **Part 7** | トラブルシューティング | 20分 | よくある問題と解決法 | Part 6 |

**Phase 3完了後の状態**:
- CI/CDで自動テスト改善が実行される
- 高度なカスタマイズができる
- 問題を自己解決できる

---

### Phase 4: エンタープライズ（オプション）

大規模組織での導入とケーススタディを学びます。

| Part | タイトル | 時間 | 内容 | 前提知識 |
|------|----------|------|------|---------|
| **Part 8** | エンタープライズ導入 | 25分 | 大規模組織での展開戦略 | Part 7 |
| **Part 9** | ケーススタディ | 15分 | 銀行システムでの実例 | Part 8 |
| **Part 10** | まとめ | 15分 | 振り返りと次のステップ | Part 9 |

**Phase 4完了後の状態**:
- エンタープライズ環境で導入できる
- 組織全体に展開できる
- ベストプラクティスを理解している

---

## 🗂️ ファイル構成

各パートには以下の4つのファイルが含まれています：

```
partXX_<topic_name>/
├── talk_script.md          # 講師用のプレゼンテーション台本
├── slides.html             # インタラクティブなHTMLスライド
├── guide.md                # 受講者用の詳細ガイド
└── exercises.md            # 演習問題と解答
```

### ファイルの使い方

#### 講師の方
1. **talk_script.md**: プレゼンテーション時に参照
   - タイミング配分
   - デモの手順
   - トラブルシューティング
   - エンゲージメントのヒント

2. **slides.html**: ブラウザで開いてプレゼン
   - キーボードで操作（← → スペース）
   - アニメーション付き
   - レスポンシブデザイン

#### 受講者の方
1. **guide.md**: 自習用の詳細ガイド
   - ステップバイステップの手順
   - コマンドと期待される出力
   - トラブルシューティング
   - よくある質問

2. **exercises.md**: 演習で理解を深める
   - 実践的な問題
   - 詳しい解答と解説
   - 評価基準

---

## 🚀 クイックスタート

### 1. 環境要件

**必須**:
- Python 3.11以上
- pip 23以上
- Git 2.x

**推奨**:
- VSCode または PyCharm
- ターミナル（bash, zsh, PowerShell）

### 2. インストール

```bash
# リポジトリをクローン
git clone https://github.com/Kamigusa/shinka-qa.git
cd shinka-qa

# インストール
pip install -e .

# 確認
shinka-qa --version
```

### 3. 最初のチュートリアルを開始

```bash
# Part 0のガイドを開く
cd tutorials/part00_introduction/
cat guide.md

# または、ブラウザでスライドを開く
open slides.html  # Mac
start slides.html  # Windows
xdg-open slides.html  # Linux
```

---

## 📖 学習パス

### 初心者向け（2時間）

まずは基礎を固めます。

```
Part 0 → Part 1 → Part 2 → Part 4
(10分)  (15分)  (20分)  (30分)
```

**到達目標**:
- 自分のプロジェクトでShinka QAを実行できる
- カバレッジを大幅に改善できる

---

### 中級者向け（3時間）

基礎から実践まで網羅します。

```
Part 0 → Part 1 → Part 2 → Part 3 → Part 4 → Part 5
(10分)  (15分)  (20分)  (25分)  (30分)  (25分)
```

**到達目標**:
- 変異戦略を使い分けられる
- CI/CDに統合できる

---

### 上級者向け（5時間）

全てのパートを完了し、エキスパートを目指します。

```
Part 0-10を全て完了
```

**到達目標**:
- エンタープライズ環境で導入できる
- カスタム戦略を開発できる
- 組織全体に展開できる

---

## 🎓 受講形式

### 1. ワークショップ形式

**推奨**: 講師が進行し、受講者が実際に手を動かす

**進め方**:
1. 講師が`talk_script.md`に従ってプレゼン
2. `slides.html`を画面共有
3. 受講者は`guide.md`を見ながら実践
4. 演習時間に`exercises.md`に取り組む
5. 質疑応答

**タイムテーブル例**（Part 1の場合）:
```
00:00-00:03  オープニング
00:03-00:07  インストール（全員で実施）
00:07-00:10  ベンチマーク実行
00:10-00:15  進化実行と結果確認
00:15-00:18  質疑応答
```

---

### 2. 自習形式

**推奨**: 自分のペースで進めたい場合

**進め方**:
1. `guide.md`を読む
2. コマンドを実際に実行
3. `exercises.md`に取り組む
4. わからないことは`slides.html`で復習

**コツ**:
- 必ず手を動かす
- エラーを恐れない
- 演習を飛ばさない

---

### 3. チーム学習形式

**推奨**: チーム全体でスキルアップしたい場合

**進め方**:
1. 週1回、1パートずつ進める
2. 持ち回りで講師役を担当
3. 演習結果を共有
4. 自プロジェクトでの適用例を発表

**スケジュール例**（10週間）:
```
Week 1: Part 0-1
Week 2: Part 2
Week 3: Part 3
Week 4: Part 4
Week 5: Part 5
Week 6: Part 6
Week 7: Part 7
Week 8: Part 8
Week 9: Part 9
Week 10: Part 10 + 総括
```

---

## 📊 進捗管理

### チェックリスト

各パートを完了したらチェックしましょう：

- [ ] Part 0: イントロダクション
- [ ] Part 1: はじめての進化
- [ ] Part 2: 設定のカスタマイズ
- [ ] Part 3: 変異戦略の理解
- [ ] Part 4: 実プロジェクト適用
- [ ] Part 5: CI/CD統合
- [ ] Part 6: 高度な使い方
- [ ] Part 7: トラブルシューティング
- [ ] Part 8: エンタープライズ導入
- [ ] Part 9: ケーススタディ
- [ ] Part 10: まとめ

### 達成バッジ

**🥉 Bronze**: Part 0-2完了
→ 基本的な使い方をマスター

**🥈 Silver**: Part 0-5完了
→ CI/CD統合までマスター

**🥇 Gold**: Part 0-10完了
→ Shinka QA エキスパート

---

## 💡 学習のヒント

### 成功するためのコツ

1. **手を動かす**
   - 読むだけでは身につかない
   - 必ずコマンドを実行する

2. **エラーを恐れない**
   - エラーは学習の機会
   - トラブルシューティングで成長する

3. **演習を飛ばさない**
   - 理解度を確認する重要な機会
   - 実践力が身につく

4. **自分のプロジェクトに適用する**
   - サンプルだけでは不十分
   - 実際のコードで試す

5. **チームで共有する**
   - 学びを共有すると定着する
   - 他の人の質問から学べる

---

## 🔧 トラブルシューティング

### よくある問題

#### インストールエラー

**症状**: `pip install -e .` が失敗する

**解決策**:
```bash
# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 再インストール
pip install -e .
```

#### コマンドが見つからない

**症状**: `shinka-qa: command not found`

**解決策**:
```bash
# PATHを確認
echo $PATH

# または、フルパスで実行
python -m shinka_qa.cli.main --version
```

#### 実行が遅い

**症状**: 10分以上かかる

**解決策**:
```yaml
# quality_config.yaml
evolution:
  num_generations: 3  # 5から3に減らす
```

### サポート

- **GitHub Issues**: https://github.com/kamigusa/shinka-qa/issues

---

## 📚 追加リソース

### ドキュメント

### ビデオ

- [YouTube チュートリアル](https://youtube.com/shinka-qa)

---

## 🤝 コントリビューション

このチュートリアルの改善にご協力ください！

### フィードバック

- **良かった点**: 何が役立ちましたか？
- **改善点**: どこがわかりにくかったですか？
- **要望**: 追加してほしい内容は？

### プルリクエスト

```bash
# 1. フォーク
git clone https://github.com/Kamigusa/shinka-qa.git

# 2. ブランチ作成
git checkout -b improve-tutorial-part1

# 3. 編集
vim tutorials/part01_first_evolution/guide.md

# 4. コミット
git commit -m "Improve Part 1 guide"

# 5. プッシュ
git push origin improve-tutorial-part1

# 6. プルリクエスト作成
```

---

## 📝 クイックリファレンス

### よく使うコマンド

```bash
# バージョン確認
shinka-qa --version

# ベンチマーク実行
shinka-qa benchmark --config quality_config.yaml

# 進化実行
shinka-qa evolve --config quality_config.yaml --verbose

# 結果の可視化
shinka-qa visualize --results-dir results/run_*/

# 設定のバリデーション
shinka-qa validate --config quality_config.yaml

# ヘルプ表示
shinka-qa --help
```

### デフォルト設定

```yaml
# quality_config.yaml (最小構成)

target:
  module: src/

test:
  initial_file: tests/test_main.py
  framework: pytest
  coverage_tool: pytest-cov

fitness:
  weights:
    coverage: 0.4
    bug_detection: 0.3
    execution_time: 0.2
    code_quality: 0.1

evolution:
  num_generations: 5
  population_per_island: 6
  num_islands: 4

output:
  results_dir: results/
```

---

## 🎯 次のステップ

### 基礎を学んだ後（Part 0-2完了）

1. **Part 4に進む**: 実プロジェクトに適用
2. **チームに共有**: 成果を報告
3. **CI/CDに統合**: 継続的改善

### 実践を完了した後（Part 0-5完了）

1. **高度な機能を学ぶ**: Part 6-7
2. **カスタマイズを試す**: 独自の戦略を開発
3. **コミュニティに貢献**: ノウハウを共有

### 全パート完了後

1. **エキスパート認定**: 証明書を取得
2. **講師として活動**: 社内でワークショップ開催
3. **コントリビューター**: プロジェクトに貢献

---

## 📄 ライセンス

このチュートリアルは、Shinka QAと同じライセンス（MIT License）で提供されています。

---

**さあ、始めましょう！Part 0から開始してください。**

[Part 0: イントロダクション](../tutorials/part00_introduction/guide.md) →

---

**作成日**: 2025-11-07
**更新日**: 2025-11-07
**バージョン**: 1.0
