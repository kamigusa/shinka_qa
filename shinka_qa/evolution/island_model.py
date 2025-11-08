"""
島モデル（Island Model）の実装
複数の独立した進化集団を並行して進化させ、定期的に個体を交換する
"""

import random
from typing import List, Dict, Tuple, Callable
from dataclasses import dataclass
from pathlib import Path
import copy


@dataclass
class Individual:
    """個体を表すクラス"""
    test_code: str
    fitness: float
    metrics: Dict[str, float]
    generation: int
    island_id: int


class Island:
    """単一の島（進化集団）"""

    def __init__(
        self,
        island_id: int,
        population_size: int,
        elite_ratio: float = 0.3
    ):
        """
        Args:
            island_id: 島のID
            population_size: 集団サイズ
            elite_ratio: エリート選択比率
        """
        self.island_id = island_id
        self.population_size = population_size
        self.elite_ratio = elite_ratio
        self.population: List[Individual] = []
        self.generation = 0
        self.best_individual: Individual = None

    def initialize_population(self, initial_code: str, fitness_func: Callable):
        """
        初期集団を生成

        Args:
            initial_code: 初期テストコード
            fitness_func: 適応度評価関数
        """
        # 初期コードを評価
        fitness, metrics = fitness_func(initial_code)

        # 初期個体を作成
        initial_individual = Individual(
            test_code=initial_code,
            fitness=fitness,
            metrics=metrics,
            generation=0,
            island_id=self.island_id
        )

        # 集団を初期化（初期は同じ個体のコピー）
        self.population = [copy.deepcopy(initial_individual) for _ in range(self.population_size)]
        self.best_individual = initial_individual

    def evolve_generation(
        self,
        mutate_func: Callable,
        fitness_func: Callable,
        target_code: str = ""
    ) -> Individual:
        """
        1世代分進化させる

        Args:
            mutate_func: 変異関数
            fitness_func: 適応度評価関数
            target_code: テスト対象コード

        Returns:
            この世代の最良個体
        """
        # エリート選択
        elite_count = max(1, int(self.population_size * self.elite_ratio))
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        elites = sorted_population[:elite_count]

        # 新しい集団を生成
        new_population = []

        # エリートをそのまま残す
        new_population.extend(copy.deepcopy(elites))

        # 残りを変異で生成
        while len(new_population) < self.population_size:
            # 親を選択（トーナメント選択）
            parent = self._tournament_selection()

            # 変異を適用
            mutated_code = mutate_func(parent.test_code, target_code)

            # 適応度を評価
            fitness, metrics = fitness_func(mutated_code)

            # 新しい個体を作成
            new_individual = Individual(
                test_code=mutated_code,
                fitness=fitness,
                metrics=metrics,
                generation=self.generation + 1,
                island_id=self.island_id
            )

            new_population.append(new_individual)

        # 集団を更新
        self.population = new_population
        self.generation += 1

        # 最良個体を更新
        current_best = max(self.population, key=lambda x: x.fitness)
        if current_best.fitness > self.best_individual.fitness:
            self.best_individual = current_best

        return current_best

    def _tournament_selection(self, tournament_size: int = 3) -> Individual:
        """
        トーナメント選択

        Args:
            tournament_size: トーナメントサイズ

        Returns:
            選択された個体
        """
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda x: x.fitness)

    def get_migrants(self, migration_rate: float) -> List[Individual]:
        """
        移住する個体を取得

        Args:
            migration_rate: 移住率

        Returns:
            移住する個体のリスト
        """
        num_migrants = max(1, int(self.population_size * migration_rate))
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        return sorted_population[:num_migrants]

    def accept_migrants(self, migrants: List[Individual]):
        """
        他の島からの移住者を受け入れる

        Args:
            migrants: 移住者のリスト
        """
        # 最悪の個体を移住者で置き換え
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=False)

        for i, migrant in enumerate(migrants):
            if i < len(sorted_population):
                # 移住者の島IDを更新
                migrant_copy = copy.deepcopy(migrant)
                migrant_copy.island_id = self.island_id
                sorted_population[i] = migrant_copy

        self.population = sorted_population


class IslandModel:
    """島モデル全体を管理するクラス"""

    def __init__(
        self,
        num_islands: int = 4,
        population_size: int = 20,
        migration_interval: int = 10,
        migration_rate: float = 0.1,
        elite_ratio: float = 0.3
    ):
        """
        Args:
            num_islands: 島の数
            population_size: 各島の個体数
            migration_interval: 移住間隔（世代）
            migration_rate: 移住率
            elite_ratio: エリート選択比率
        """
        self.num_islands = num_islands
        self.population_size = population_size
        self.migration_interval = migration_interval
        self.migration_rate = migration_rate

        # 島を初期化
        self.islands = [
            Island(i, population_size, elite_ratio)
            for i in range(num_islands)
        ]

        self.global_best: Individual = None
        self.generation = 0

    def initialize(self, initial_code: str, fitness_func: Callable):
        """
        全ての島を初期化

        Args:
            initial_code: 初期テストコード
            fitness_func: 適応度評価関数
        """
        for island in self.islands:
            island.initialize_population(initial_code, fitness_func)

        # グローバル最良個体を設定
        self.global_best = max(
            [island.best_individual for island in self.islands],
            key=lambda x: x.fitness
        )

    def evolve(
        self,
        generations: int,
        mutate_func: Callable,
        fitness_func: Callable,
        target_code: str = "",
        callback: Callable = None
    ) -> Individual:
        """
        指定世代数だけ進化させる

        Args:
            generations: 世代数
            mutate_func: 変異関数
            fitness_func: 適応度評価関数
            target_code: テスト対象コード
            callback: 各世代後に呼ばれるコールバック関数

        Returns:
            最終的な最良個体
        """
        for gen in range(generations):
            # 各島で1世代進化
            generation_bests = []
            for island in self.islands:
                best = island.evolve_generation(mutate_func, fitness_func, target_code)
                generation_bests.append(best)

            # グローバル最良個体を更新
            current_gen_best = max(generation_bests, key=lambda x: x.fitness)
            if current_gen_best.fitness > self.global_best.fitness:
                self.global_best = current_gen_best

            # 移住処理
            if (gen + 1) % self.migration_interval == 0:
                self._migrate()

            # コールバック実行
            if callback:
                callback(gen + 1, generation_bests, self.global_best)

            self.generation = gen + 1

            # アーリーストッピング: 完璧なテストが生成されたら終了
            if self._check_perfect_solution():
                try:
                    print(f"\n🎯 Perfect solution achieved at generation {gen + 1}!")
                except UnicodeEncodeError:
                    print(f"\n[*] Perfect solution achieved at generation {gen + 1}!")
                print(f"   Coverage: 100%, Bug Detection: 100%, Fitness: {self.global_best.fitness:.3f}")
                print(f"   Early stopping - skipping remaining {generations - gen - 1} generations\n")
                break

        return self.global_best

    def _check_perfect_solution(self) -> bool:
        """
        完璧な解が見つかったかチェック

        Returns:
            完璧な解が見つかった場合True
        """
        if not self.global_best or not self.global_best.metrics:
            return False

        metrics = self.global_best.metrics

        # カバレッジ、バグ検出、適応度すべてが完璧（またはほぼ完璧）
        coverage = metrics.get('coverage', 0) / 100.0  # パーセンテージを0-1に変換
        bug_detection = metrics.get('bugs_detected', 0)
        fitness = self.global_best.fitness

        # すべてが1.0（100%）または0.999以上
        is_perfect = (
            coverage >= 0.999 and
            bug_detection >= 0.999 and
            fitness >= 0.999
        )

        return is_perfect

    def _migrate(self):
        """島間で個体を移住させる"""
        # 各島から移住者を取得
        all_migrants = []
        for island in self.islands:
            migrants = island.get_migrants(self.migration_rate)
            all_migrants.append(migrants)

        # リング型の移住（島iの移住者は島i+1に移動）
        for i, island in enumerate(self.islands):
            next_island_idx = (i + 1) % self.num_islands
            island.accept_migrants(all_migrants[next_island_idx])

    def get_statistics(self) -> Dict[str, any]:
        """
        現在の統計情報を取得

        Returns:
            統計情報の辞書
        """
        island_stats = []
        for island in self.islands:
            avg_fitness = sum(ind.fitness for ind in island.population) / len(island.population)
            island_stats.append({
                'island_id': island.island_id,
                'best_fitness': island.best_individual.fitness,
                'avg_fitness': avg_fitness,
                'generation': island.generation
            })

        return {
            'generation': self.generation,
            'global_best_fitness': self.global_best.fitness,
            'island_stats': island_stats
        }
