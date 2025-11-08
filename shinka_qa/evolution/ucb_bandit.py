"""
UCB1（Upper Confidence Bound）バンディットアルゴリズムの実装
複数のLLMモデルや変異戦略から最適なものを選択する
"""

import math
from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Arm:
    """バンディットアルゴリズムの腕（選択肢）"""
    name: str
    total_reward: float = 0.0
    num_plays: int = 0
    average_reward: float = 0.0


class UCB1Bandit:
    """UCB1バンディットアルゴリズム"""

    def __init__(
        self,
        arms: List[str],
        exploration_coefficient: float = 1.0
    ):
        """
        Args:
            arms: 選択肢のリスト（モデル名、戦略名など）
            exploration_coefficient: 探索係数（デフォルト: 1.0）
        """
        self.exploration_coefficient = exploration_coefficient
        self.arms = {name: Arm(name=name) for name in arms}
        self.total_plays = 0

    def select_arm(self) -> str:
        """
        UCB1アルゴリズムで腕を選択

        Returns:
            選択された腕の名前
        """
        # 各腕を少なくとも1回は選択
        for arm_name, arm in self.arms.items():
            if arm.num_plays == 0:
                return arm_name

        # UCB1スコアを計算して最大の腕を選択
        ucb_scores = {}
        for arm_name, arm in self.arms.items():
            # UCB1スコア = 平均報酬 + c * sqrt(ln(総プレイ数) / プレイ数)
            exploration_bonus = self.exploration_coefficient * math.sqrt(
                math.log(self.total_plays) / arm.num_plays
            )
            ucb_scores[arm_name] = arm.average_reward + exploration_bonus

        # 最大スコアの腕を返す
        return max(ucb_scores, key=ucb_scores.get)

    def update(self, arm_name: str, reward: float):
        """
        選択した腕の報酬を更新

        Args:
            arm_name: 選択した腕の名前
            reward: 得られた報酬（0.0〜1.0）
        """
        if arm_name not in self.arms:
            raise ValueError(f"Unknown arm: {arm_name}")

        arm = self.arms[arm_name]
        arm.num_plays += 1
        arm.total_reward += reward
        arm.average_reward = arm.total_reward / arm.num_plays

        self.total_plays += 1

    def get_statistics(self) -> Dict[str, Any]:
        """
        各腕の統計情報を取得

        Returns:
            統計情報の辞書
        """
        stats = {}
        for arm_name, arm in self.arms.items():
            stats[arm_name] = {
                'num_plays': arm.num_plays,
                'total_reward': arm.total_reward,
                'average_reward': arm.average_reward,
                'play_rate': arm.num_plays / self.total_plays if self.total_plays > 0 else 0.0
            }
        return stats

    def get_best_arm(self) -> str:
        """
        最も平均報酬が高い腕を返す

        Returns:
            最良の腕の名前
        """
        return max(self.arms, key=lambda name: self.arms[name].average_reward)


class StrategyBandit:
    """変異戦略を選択するためのバンディット"""

    def __init__(
        self,
        strategies: List[str],
        exploration_coefficient: float = 1.0
    ):
        """
        Args:
            strategies: 変異戦略のリスト
            exploration_coefficient: 探索係数
        """
        self.bandit = UCB1Bandit(strategies, exploration_coefficient)
        self.strategies = strategies

    def select_strategy(self) -> str:
        """
        次に使用する変異戦略を選択

        Returns:
            選択された戦略名
        """
        return self.bandit.select_arm()

    def update_strategy(self, strategy: str, fitness_improvement: float):
        """
        戦略の報酬を更新

        Args:
            strategy: 使用した戦略
            fitness_improvement: 適応度の改善度（0.0〜1.0）
        """
        # 適応度改善度を報酬として使用
        reward = max(0.0, min(1.0, fitness_improvement))
        self.bandit.update(strategy, reward)

    def get_statistics(self) -> Dict[str, Any]:
        """戦略の統計情報を取得"""
        return self.bandit.get_statistics()


class ModelBandit:
    """LLMモデルを選択するためのバンディット"""

    def __init__(
        self,
        models: List[str],
        exploration_coefficient: float = 1.0
    ):
        """
        Args:
            models: LLMモデルのリスト
            exploration_coefficient: 探索係数
        """
        self.bandit = UCB1Bandit(models, exploration_coefficient)
        self.models = models

    def select_model(self) -> str:
        """
        次に使用するLLMモデルを選択

        Returns:
            選択されたモデル名
        """
        return self.bandit.select_arm()

    def update_model(self, model: str, fitness_improvement: float):
        """
        モデルの報酬を更新

        Args:
            model: 使用したモデル
            fitness_improvement: 適応度の改善度（0.0〜1.0）
        """
        reward = max(0.0, min(1.0, fitness_improvement))
        self.bandit.update(model, reward)

    def get_statistics(self) -> Dict[str, Any]:
        """モデルの統計情報を取得"""
        return self.bandit.get_statistics()


class AdaptiveBanditSelector:
    """戦略とモデルの両方を選択する統合バンディット"""

    def __init__(
        self,
        strategies: List[str],
        models: List[str] = None,
        exploration_coefficient: float = 1.0
    ):
        """
        Args:
            strategies: 変異戦略のリスト
            models: LLMモデルのリスト（Noneの場合は単一モデル）
            exploration_coefficient: 探索係数
        """
        self.strategy_bandit = StrategyBandit(strategies, exploration_coefficient)
        self.model_bandit = ModelBandit(models, exploration_coefficient) if models else None

    def select(self) -> Dict[str, str]:
        """
        戦略とモデルを選択

        Returns:
            {'strategy': 戦略名, 'model': モデル名}
        """
        result = {'strategy': self.strategy_bandit.select_strategy()}

        if self.model_bandit:
            result['model'] = self.model_bandit.select_model()

        return result

    def update(
        self,
        strategy: str,
        fitness_improvement: float,
        model: str = None
    ):
        """
        選択の報酬を更新

        Args:
            strategy: 使用した戦略
            fitness_improvement: 適応度の改善度
            model: 使用したモデル（オプション）
        """
        self.strategy_bandit.update_strategy(strategy, fitness_improvement)

        if self.model_bandit and model:
            self.model_bandit.update_model(model, fitness_improvement)

    def get_statistics(self) -> Dict[str, Any]:
        """全体の統計情報を取得"""
        stats = {
            'strategies': self.strategy_bandit.get_statistics()
        }

        if self.model_bandit:
            stats['models'] = self.model_bandit.get_statistics()

        return stats
