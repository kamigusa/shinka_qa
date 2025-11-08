# Part 6: 高度な使い方 - チュートリアルガイド

**所要時間**: 30分
**難易度**: 上級

---

## 🎯 学ぶこと

1. カスタム変異戦略の作成
2. プラグインAPI の使用
3. 高度な設定オプション
4. パフォーマンスチューニング

---

## 🔌 カスタム変異戦略

### 独自戦略の作成

```python
# custom_strategies/add_performance_test.py
from shinka_quality.mutation import MutationStrategy

class AddPerformanceTest(MutationStrategy):
    """パフォーマンステストを追加する戦略"""

    def mutate(self, test_suite):
        """テストスイートに変異を適用"""
        new_tests = []

        for test in test_suite.tests:
            # 元のテストを保持
            new_tests.append(test)

            # パフォーマンステストを追加
            perf_test = self._create_performance_test(test)
            new_tests.append(perf_test)

        return TestSuite(new_tests)

    def _create_performance_test(self, test):
        """パフォーマンステストを生成"""
        code = f"""
import time

def test_{test.name}_performance():
    start = time.time()
    {test.name}()
    duration = time.time() - start
    assert duration < 0.1, f"Too slow: {{duration}}s"
"""
        return Test(code)
```

### カスタム戦略の登録

```yaml
# quality_config.yaml
mutation_strategies:
  - add_edge_case
  - custom_strategies.add_performance_test.AddPerformanceTest
```

---

## 🎛️ 高度な設定オプション

### 早期停止

```yaml
evolution:
  early_stopping:
    enabled: true
    patience: 3              # 3世代改善なしで停止
    min_improvement: 0.01    # 最小改善率 1%
    metric: coverage         # 監視指標
```

### 並列化設定

```yaml
evolution:
  parallel:
    enabled: true
    num_workers: 8           # ワーカー数
    batch_size: 4            # バッチサイズ
```

### キャッシング

```yaml
cache:
  enabled: true
  directory: .shinka_cache/
  ttl: 86400                 # 24時間
```

---

## ⚡ パフォーマンスチューニング

### メモリ使用量の削減

```yaml
optimization:
  memory_limit: 4GB          # メモリ上限
  gc_interval: 10            # GC頻度
  store_intermediate: false  # 中間結果を保存しない
```

### 実行時間の最適化

```yaml
evolution:
  timeout_per_test: 5        # テストタイムアウト（秒）
  max_test_size: 100         # 最大テストサイズ（行）
```

---

## 📊 カスタムメトリクス

```python
# custom_metrics/security_score.py
from shinka_quality.metrics import Metric

class SecurityScore(Metric):
    """セキュリティスコアを計算"""

    def calculate(self, test_suite):
        score = 0

        # SQL injection テスト
        if self._has_sql_injection_tests(test_suite):
            score += 0.3

        # XSS テスト
        if self._has_xss_tests(test_suite):
            score += 0.3

        # CSRF テスト
        if self._has_csrf_tests(test_suite):
            score += 0.2

        # 認証テスト
        if self._has_auth_tests(test_suite):
            score += 0.2

        return score
```

### メトリクスの登録

```yaml
fitness:
  custom_metrics:
    - custom_metrics.security_score.SecurityScore

  weights:
    coverage: 0.3
    bug_detection: 0.3
    security_score: 0.3      # カスタムメトリクス
    execution_time: 0.1
```

---

## 📝 チェックリスト

- [ ] カスタム戦略を作成
- [ ] 高度な設定を理解
- [ ] パフォーマンスチューニングを実施
- [ ] カスタムメトリクスを検討

---

**作成日**: 2025-11-07
**バージョン**: 1.0
