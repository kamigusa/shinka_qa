"""
レポート生成器
進化の結果をHTML/PDFレポートとして出力
"""

from pathlib import Path
from typing import Dict, List, Any
import json
from datetime import datetime


class ReportGenerator:
    """レポート生成クラス"""

    def __init__(self, results_dir: Path):
        """
        Args:
            results_dir: 結果ディレクトリのパス
        """
        self.results_dir = Path(results_dir)
        self.metrics_file = self.results_dir / 'metrics.json'

    def generate_html_report(self) -> Path:
        """
        HTMLレポートを生成

        Returns:
            生成されたHTMLファイルのパス
        """
        if not self.metrics_file.exists():
            raise FileNotFoundError(f"Metrics file not found: {self.metrics_file}")

        # メトリクスを読み込み
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            metrics = json.load(f)

        # HTMLを生成
        html_content = self._generate_html_content(metrics)

        # ファイルに保存
        html_file = self.results_dir / 'evolution_report.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return html_file

    def _generate_html_content(self, metrics: Dict[str, Any]) -> str:
        """
        HTMLコンテンツを生成

        Args:
            metrics: メトリクスデータ

        Returns:
            HTML文字列
        """
        # 基本情報
        baseline = metrics.get('baseline', {})
        initial_metrics = metrics.get('initial_metrics', {})
        timestamp = metrics.get('timestamp', 'Unknown')

        # カバレッジ情報
        baseline_coverage = baseline.get('coverage', 0)
        current_coverage = initial_metrics.get('coverage', 0)
        coverage_improvement = current_coverage - baseline_coverage

        # バグ検出情報
        bugs_detected = initial_metrics.get('bugs_detected', 0)

        # 実行時間
        execution_time = initial_metrics.get('execution_time', 0)

        # コード品質
        maintainability = initial_metrics.get('maintainability', 0)

        # フィットネス
        fitness = metrics.get('initial_fitness', 0)

        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shinka Quality - Evolution Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}

        .metric-card:hover {{
            transform: translateY(-5px);
        }}

        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}

        .metric-subtitle {{
            font-size: 0.9em;
            color: #888;
            margin-top: 5px;
        }}

        .improvement {{
            color: #10b981;
            font-weight: bold;
        }}

        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
        }}

        .status-excellent {{
            background: #10b981;
            color: white;
        }}

        .status-good {{
            background: #3b82f6;
            color: white;
        }}

        .status-fair {{
            background: #f59e0b;
            color: white;
        }}

        .status-poor {{
            background: #ef4444;
            color: white;
        }}

        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        .info-table th,
        .info-table td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}

        .info-table th {{
            background: #f9fafb;
            font-weight: bold;
            color: #667eea;
        }}

        .footer {{
            background: #f9fafb;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e5e7eb;
            border-radius: 15px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 1s ease-in-out;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Shinka Quality Evolution Report</h1>
            <p>Generated on {timestamp}</p>
        </div>

        <div class="content">
            <div class="section">
                <h2>Overview</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Test Coverage</div>
                        <div class="metric-value">{current_coverage:.1f}%</div>
                        <div class="metric-subtitle">
                            <span class="improvement">+{coverage_improvement:.1f}%</span> from baseline
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {current_coverage}%">
                                {current_coverage:.1f}%
                            </div>
                        </div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">Bug Detection</div>
                        <div class="metric-value">{bugs_detected:.1%}</div>
                        <div class="metric-subtitle">
                            of seeded bugs detected
                        </div>
                        {self._get_status_badge(bugs_detected, 'bug_detection')}
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">Execution Time</div>
                        <div class="metric-value">{execution_time:.2f}s</div>
                        <div class="metric-subtitle">
                            test suite runtime
                        </div>
                        {self._get_status_badge(execution_time, 'execution_time')}
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">Code Quality</div>
                        <div class="metric-value">{maintainability:.2f}</div>
                        <div class="metric-subtitle">
                            maintainability score
                        </div>
                        {self._get_status_badge(maintainability, 'quality')}
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>Overall Fitness Score</h2>
                <div class="metric-card">
                    <div class="metric-value" style="text-align: center; font-size: 3em;">
                        {fitness:.3f}
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {fitness * 100}%">
                            {fitness:.1%}
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>Detailed Metrics</h2>
                <table class="info-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                            <th>Weight</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Coverage Improvement</td>
                            <td>{initial_metrics.get('coverage_improvement', 0):.3f}</td>
                            <td>40%</td>
                        </tr>
                        <tr>
                            <td>Bug Detection Rate</td>
                            <td>{bugs_detected:.3f}</td>
                            <td>35%</td>
                        </tr>
                        <tr>
                            <td>Efficiency</td>
                            <td>{initial_metrics.get('efficiency', 0):.3f}</td>
                            <td>15%</td>
                        </tr>
                        <tr>
                            <td>Maintainability</td>
                            <td>{maintainability:.3f}</td>
                            <td>10%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>Generated by Shinka Quality v1.0</p>
            <p>A quality improvement framework powered by evolutionary algorithms</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def _get_status_badge(self, value: float, metric_type: str) -> str:
        """
        ステータスバッジのHTMLを生成

        Args:
            value: メトリクス値
            metric_type: メトリクスの種類

        Returns:
            バッジのHTML
        """
        if metric_type == 'bug_detection':
            if value >= 0.8:
                return '<span class="status-badge status-excellent">Excellent</span>'
            elif value >= 0.6:
                return '<span class="status-badge status-good">Good</span>'
            elif value >= 0.4:
                return '<span class="status-badge status-fair">Fair</span>'
            else:
                return '<span class="status-badge status-poor">Needs Improvement</span>'

        elif metric_type == 'execution_time':
            if value <= 2.0:
                return '<span class="status-badge status-excellent">Excellent</span>'
            elif value <= 5.0:
                return '<span class="status-badge status-good">Good</span>'
            elif value <= 10.0:
                return '<span class="status-badge status-fair">Fair</span>'
            else:
                return '<span class="status-badge status-poor">Slow</span>'

        elif metric_type == 'quality':
            if value >= 0.8:
                return '<span class="status-badge status-excellent">Excellent</span>'
            elif value >= 0.6:
                return '<span class="status-badge status-good">Good</span>'
            elif value >= 0.4:
                return '<span class="status-badge status-fair">Fair</span>'
            else:
                return '<span class="status-badge status-poor">Needs Improvement</span>'

        return ''

    def generate_summary_text(self) -> str:
        """
        サマリーテキストを生成

        Returns:
            サマリー文字列
        """
        if not self.metrics_file.exists():
            return "No metrics data available."

        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            metrics = json.load(f)

        baseline = metrics.get('baseline', {})
        initial_metrics = metrics.get('initial_metrics', {})

        baseline_coverage = baseline.get('coverage', 0)
        current_coverage = initial_metrics.get('coverage', 0)

        summary = f"""
Shinka Quality - Evolution Summary
{'=' * 50}

Baseline Coverage: {baseline_coverage:.1f}%
Current Coverage:  {current_coverage:.1f}%
Improvement:       +{current_coverage - baseline_coverage:.1f}%

Bug Detection:     {initial_metrics.get('bugs_detected', 0):.1%}
Execution Time:    {initial_metrics.get('execution_time', 0):.2f}s
Code Quality:      {initial_metrics.get('maintainability', 0):.2f}

Overall Fitness:   {metrics.get('initial_fitness', 0):.3f}
"""

        return summary
