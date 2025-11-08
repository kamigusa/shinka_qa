# Part 5: CI/CD統合 - チュートリアルガイド

**所要時間**: 25分
**難易度**: 中級〜上級

---

## 🎯 学ぶこと

1. GitHub ActionsとGitLab CIへの統合
2. 自動テスト品質チェック
3. PR/MRごとの進化実行
4. カバレッジ要件の自動チェック

---

## 🔧 GitHub Actions 統合

### 基本設定

```.github/workflows/shinka_quality.yml
name: Shinka QA

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-quality:
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
          pip install -r requirements.txt

      - name: Run Shinka QA
        run: |
          shinka-qa evolve --config quality_config.yaml

      - name: Check coverage threshold
        run: |
          python scripts/check_coverage.py --min 80
```

### カバレッジチェックスクリプト

```python
# scripts/check_coverage.py
import json
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--min', type=int, required=True)
args = parser.parse_args()

with open('results/latest/metrics.json') as f:
    metrics = json.load(f)

coverage = metrics['final_metrics']['coverage']

if coverage < args.min:
    print(f"Coverage {coverage}% is below minimum {args.min}%")
    sys.exit(1)

print(f"Coverage {coverage}% meets requirement")
```

---

## 🦊 GitLab CI 統合

```.gitlab-ci.yml
stages:
  - test
  - quality

test_quality:
  stage: quality
  image: python:3.11
  script:
    - pip install shinka-qa
    - shinka-qa evolve --config quality_config.yaml
    - python scripts/check_coverage.py --min 80
  artifacts:
    paths:
      - results/
    expire_in: 1 week
  only:
    - merge_requests
    - main
```

---

## 📊 PRごとの品質レポート

### GitHub Actions - コメント投稿

```yaml
- name: Comment PR
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const metrics = JSON.parse(fs.readFileSync('results/latest/metrics.json'));

      const coverage = metrics.final_metrics.coverage;
      const improvement = coverage - metrics.baseline.coverage;

      const body = `
      ## Shinka QA Report

      **Coverage**: ${coverage}% (${improvement > 0 ? '+' : ''}${improvement.toFixed(1)}%)
      **Bug Detection**: ${metrics.final_metrics.bugs_detected}

      ${coverage >= 80 ? '✅' : '⚠️'} ${coverage >= 80 ? 'Meets' : 'Below'} minimum requirement (80%)
      `;

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.name,
        body: body
      });
```

---

## ⚙️ 設定のベストプラクティス

### CI用の軽量設定

```yaml
# quality_config_ci.yaml
evolution:
  num_generations: 3      # CIでは少なめ
  population_per_island: 4
  num_islands: 2

  early_stopping:
    enabled: true
    patience: 2
```

### 差分のみ対象

```bash
# 変更されたファイルのみテスト
git diff --name-only origin/main...HEAD | grep '.py$' > changed_files.txt
shinka-qa evolve --target-files changed_files.txt
```

---

## 📝 チェックリスト

- [ ] GitHub Actions または GitLab CI を設定
- [ ] カバレッジチェックを追加
- [ ] PR/MRコメント機能を実装
- [ ] 軽量設定を作成
- [ ] テスト実行を確認

---

**作成日**: 2025-11-07
**バージョン**: 1.0
