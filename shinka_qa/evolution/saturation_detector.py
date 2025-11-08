"""
カバレッジサチュレーション検出器
カバレッジの向上が飽和したかを判定する
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class CoverageRecord:
    """カバレッジ記録"""
    generation: int
    coverage: float


class CoverageSaturationDetector:
    """カバレッジのサチュレーション（飽和）を検出するクラス"""

    def __init__(
        self,
        window_size: int = 5,
        improvement_threshold: float = 0.5,
        min_generations: int = 10
    ):
        """
        Args:
            window_size: 評価するウィンドウサイズ（世代数）
            improvement_threshold: サチュレーションとみなす改善閾値（%）
            min_generations: サチュレーション判定を開始する最小世代数
        """
        self.window_size = window_size
        self.improvement_threshold = improvement_threshold
        self.min_generations = min_generations
        self.coverage_history: List[CoverageRecord] = []
        self.saturated = False
        self.saturation_generation: Optional[int] = None

    def add_coverage(self, generation: int, coverage: float):
        """
        カバレッジ記録を追加

        Args:
            generation: 世代番号
            coverage: カバレッジ（%）
        """
        record = CoverageRecord(generation=generation, coverage=coverage)
        self.coverage_history.append(record)

    def is_saturated(self) -> bool:
        """
        カバレッジがサチュレーション（飽和）しているかを判定

        Returns:
            サチュレーションしている場合True
        """
        # すでにサチュレーション検出済みの場合
        if self.saturated:
            return True

        # 最低世代数に達していない場合
        if len(self.coverage_history) < self.min_generations:
            return False

        # ウィンドウサイズ分のデータがない場合
        if len(self.coverage_history) < self.window_size:
            return False

        # 最近のwindow_size世代のカバレッジを取得
        recent_records = self.coverage_history[-self.window_size:]

        # 最初と最後のカバレッジを比較
        first_coverage = recent_records[0].coverage
        last_coverage = recent_records[-1].coverage

        improvement = last_coverage - first_coverage

        # 改善が閾値以下の場合、サチュレーションとみなす
        if improvement <= self.improvement_threshold:
            if not self.saturated:
                self.saturated = True
                self.saturation_generation = self.coverage_history[-1].generation
            return True

        return False

    def get_current_coverage(self) -> Optional[float]:
        """
        現在のカバレッジを取得

        Returns:
            最新のカバレッジ、記録がない場合None
        """
        if not self.coverage_history:
            return None
        return self.coverage_history[-1].coverage

    def get_coverage_improvement(self) -> float:
        """
        初期カバレッジからの改善量を取得

        Returns:
            改善量（%）
        """
        if len(self.coverage_history) < 2:
            return 0.0

        initial = self.coverage_history[0].coverage
        current = self.coverage_history[-1].coverage
        return current - initial

    def get_recent_improvement(self, window: Optional[int] = None) -> float:
        """
        最近のカバレッジ改善量を取得

        Args:
            window: ウィンドウサイズ（Noneの場合はself.window_sizeを使用）

        Returns:
            最近の改善量（%）
        """
        if window is None:
            window = self.window_size

        if len(self.coverage_history) < 2:
            return 0.0

        window = min(window, len(self.coverage_history))
        recent = self.coverage_history[-window:]

        return recent[-1].coverage - recent[0].coverage

    def get_statistics(self) -> dict:
        """
        統計情報を取得

        Returns:
            統計情報の辞書
        """
        if not self.coverage_history:
            return {
                'total_generations': 0,
                'current_coverage': 0.0,
                'initial_coverage': 0.0,
                'total_improvement': 0.0,
                'recent_improvement': 0.0,
                'is_saturated': False,
                'saturation_generation': None
            }

        return {
            'total_generations': len(self.coverage_history),
            'current_coverage': self.get_current_coverage(),
            'initial_coverage': self.coverage_history[0].coverage,
            'total_improvement': self.get_coverage_improvement(),
            'recent_improvement': self.get_recent_improvement(),
            'is_saturated': self.saturated,
            'saturation_generation': self.saturation_generation
        }

    def reset_saturation(self):
        """サチュレーション状態をリセット"""
        self.saturated = False
        self.saturation_generation = None
