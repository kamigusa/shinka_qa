"""
メタスクラッチパッド（Meta Scratchpad）の実装
進化過程で得られた知見や成功した戦略を記録・共有する
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Insight:
    """得られた洞察を表すクラス"""
    generation: int
    strategy: str
    fitness_improvement: float
    description: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SuccessPattern:
    """成功パターンを表すクラス"""
    strategy: str
    context: str  # どのような状況で成功したか
    frequency: int = 0
    avg_improvement: float = 0.0
    examples: List[str] = field(default_factory=list)


class MetaScratchpad:
    """メタスクラッチパッドクラス"""

    def __init__(self, max_insights: int = 100):
        """
        Args:
            max_insights: 保存する洞察の最大数
        """
        self.max_insights = max_insights

        # 洞察のリスト
        self.insights: List[Insight] = []

        # 成功パターンの辞書
        self.success_patterns: Dict[str, SuccessPattern] = {}

        # カバレッジ改善の履歴
        self.coverage_history: List[Dict[str, float]] = []

        # バグ検出の履歴
        self.bug_detection_history: List[Dict[str, float]] = []

    def add_insight(
        self,
        generation: int,
        strategy: str,
        fitness_improvement: float,
        description: str,
        metadata: Dict[str, Any] = None
    ):
        """
        洞察を追加

        Args:
            generation: 世代番号
            strategy: 使用した戦略
            fitness_improvement: 適応度の改善
            description: 洞察の説明
            metadata: 追加のメタデータ
        """
        insight = Insight(
            generation=generation,
            strategy=strategy,
            fitness_improvement=fitness_improvement,
            description=description,
            metadata=metadata or {}
        )

        self.insights.append(insight)

        # 最大数を超えたら古いものを削除
        if len(self.insights) > self.max_insights:
            self.insights.pop(0)

        # 成功パターンを更新
        self._update_success_pattern(strategy, fitness_improvement, description)

    def _update_success_pattern(
        self,
        strategy: str,
        improvement: float,
        example: str
    ):
        """
        成功パターンを更新

        Args:
            strategy: 戦略名
            improvement: 改善度
            example: 成功例
        """
        # 有意な改善があった場合のみ記録
        if improvement > 0.05:  # 5%以上の改善
            if strategy not in self.success_patterns:
                self.success_patterns[strategy] = SuccessPattern(
                    strategy=strategy,
                    context="",
                    frequency=0,
                    avg_improvement=0.0,
                    examples=[]
                )

            pattern = self.success_patterns[strategy]
            pattern.frequency += 1
            pattern.avg_improvement = (
                (pattern.avg_improvement * (pattern.frequency - 1) + improvement) /
                pattern.frequency
            )

            # 例を最大5個まで保存
            if len(pattern.examples) < 5:
                pattern.examples.append(example)

    def get_best_strategies(self, top_k: int = 3) -> List[str]:
        """
        最も効果的な戦略を取得

        Args:
            top_k: 上位何個の戦略を返すか

        Returns:
            戦略名のリスト
        """
        sorted_patterns = sorted(
            self.success_patterns.items(),
            key=lambda x: x[1].avg_improvement * x[1].frequency,
            reverse=True
        )

        return [pattern[0] for pattern in sorted_patterns[:top_k]]

    def get_strategy_recommendation(self, current_coverage: float) -> str:
        """
        現在のカバレッジに基づいて戦略を推奨

        Args:
            current_coverage: 現在のカバレッジ

        Returns:
            推奨される戦略名
        """
        # カバレッジが低い場合はエッジケースの追加を推奨
        if current_coverage < 50:
            return "add_edge_cases"

        # カバレッジが中程度の場合はパラメータ化を推奨
        elif current_coverage < 70:
            return "add_parametrize"

        # カバレッジが高い場合はアサーションの改善を推奨
        elif current_coverage < 85:
            return "improve_assertions"

        # カバレッジが非常に高い場合はモックやフィクスチャを追加
        else:
            return "add_fixtures"

    def record_coverage(self, generation: int, coverage: float, strategy: str = ""):
        """
        カバレッジの履歴を記録

        Args:
            generation: 世代番号
            coverage: カバレッジ
            strategy: 使用した戦略
        """
        self.coverage_history.append({
            'generation': generation,
            'coverage': coverage,
            'strategy': strategy
        })

    def record_bug_detection(
        self,
        generation: int,
        bugs_detected: float,
        strategy: str = ""
    ):
        """
        バグ検出の履歴を記録

        Args:
            generation: 世代番号
            bugs_detected: 検出されたバグの割合
            strategy: 使用した戦略
        """
        self.bug_detection_history.append({
            'generation': generation,
            'bugs_detected': bugs_detected,
            'strategy': strategy
        })

    def get_progress_summary(self) -> str:
        """
        進化の進捗をまとめたサマリーを取得

        Returns:
            サマリー文字列
        """
        if not self.coverage_history and not self.insights:
            return "No progress data available."

        summary_parts = []

        # カバレッジの進捗
        if self.coverage_history:
            initial_coverage = self.coverage_history[0]['coverage']
            latest_coverage = self.coverage_history[-1]['coverage']
            improvement = latest_coverage - initial_coverage

            summary_parts.append(
                f"Coverage improved from {initial_coverage:.1f}% to {latest_coverage:.1f}% "
                f"(+{improvement:.1f}%)"
            )

        # 最も効果的だった戦略
        best_strategies = self.get_best_strategies(top_k=3)
        if best_strategies:
            summary_parts.append(
                f"Most effective strategies: {', '.join(best_strategies)}"
            )

        # 重要な洞察
        significant_insights = [
            insight for insight in self.insights
            if insight.fitness_improvement > 0.1
        ]

        if significant_insights:
            summary_parts.append(
                f"Found {len(significant_insights)} significant improvements"
            )

        return "\n".join(summary_parts)

    def generate_prompt_context(self, current_coverage: float) -> str:
        """
        LLMプロンプトに追加するコンテキストを生成

        Args:
            current_coverage: 現在のカバレッジ

        Returns:
            プロンプトに追加するコンテキスト文字列
        """
        context_parts = []

        # 成功パターンの情報
        best_strategies = self.get_best_strategies(top_k=2)
        if best_strategies:
            context_parts.append(
                f"Previously successful strategies: {', '.join(best_strategies)}"
            )

        # 最近の洞察
        recent_insights = self.insights[-3:] if self.insights else []
        if recent_insights:
            insights_text = "\n".join([
                f"- {insight.description} (improvement: {insight.fitness_improvement:.2f})"
                for insight in recent_insights
            ])
            context_parts.append(f"Recent insights:\n{insights_text}")

        # 推奨事項
        recommendation = self.get_strategy_recommendation(current_coverage)
        context_parts.append(
            f"Based on current coverage ({current_coverage:.1f}%), "
            f"consider focusing on: {recommendation}"
        )

        return "\n\n".join(context_parts)

    def export_to_json(self) -> str:
        """
        スクラッチパッドの内容をJSONにエクスポート

        Returns:
            JSON文字列
        """
        data = {
            'insights': [
                {
                    'generation': i.generation,
                    'strategy': i.strategy,
                    'fitness_improvement': i.fitness_improvement,
                    'description': i.description,
                    'timestamp': i.timestamp,
                    'metadata': i.metadata
                }
                for i in self.insights
            ],
            'success_patterns': {
                name: {
                    'strategy': p.strategy,
                    'frequency': p.frequency,
                    'avg_improvement': p.avg_improvement,
                    'examples': p.examples
                }
                for name, p in self.success_patterns.items()
            },
            'coverage_history': self.coverage_history,
            'bug_detection_history': self.bug_detection_history
        }

        return json.dumps(data, indent=2, ensure_ascii=False)

    def get_statistics(self) -> Dict[str, Any]:
        """
        統計情報を取得

        Returns:
            統計情報の辞書
        """
        return {
            'total_insights': len(self.insights),
            'num_success_patterns': len(self.success_patterns),
            'best_strategies': self.get_best_strategies(top_k=3),
            'coverage_improvement': (
                self.coverage_history[-1]['coverage'] - self.coverage_history[0]['coverage']
                if len(self.coverage_history) > 1 else 0.0
            ),
            'avg_fitness_improvement': (
                sum(i.fitness_improvement for i in self.insights) / len(self.insights)
                if self.insights else 0.0
            )
        }
