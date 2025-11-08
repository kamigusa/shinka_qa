"""
新規性フィルタリング（Novelty Filtering）の実装
生成されたテストコードの多様性を維持し、局所最適化を防ぐ
"""

import hashlib
from typing import List, Set, Dict, Tuple
from difflib import SequenceMatcher
import re


class NoveltyFilter:
    """新規性フィルタリングクラス"""

    def __init__(
        self,
        similarity_threshold: float = 0.9,
        archive_size: int = 100
    ):
        """
        Args:
            similarity_threshold: 類似度の閾値（これ以上似ている場合は除外）
            archive_size: アーカイブの最大サイズ
        """
        self.similarity_threshold = similarity_threshold
        self.archive_size = archive_size

        # コードのハッシュを保存するアーカイブ
        self.code_hashes: Set[str] = set()

        # コードの特徴ベクトルを保存するアーカイブ
        self.code_archive: List[Dict[str, any]] = []

    def is_novel(self, code: str) -> bool:
        """
        コードが新規性を持つかチェック

        Args:
            code: チェックするコード

        Returns:
            新規性があればTrue
        """
        # 完全一致チェック（高速）
        code_hash = self._compute_hash(code)
        if code_hash in self.code_hashes:
            return False

        # 特徴ベクトルによる類似度チェック
        features = self._extract_features(code)

        for archived_item in self.code_archive:
            similarity = self._compute_similarity(features, archived_item['features'])
            if similarity >= self.similarity_threshold:
                return False

        return True

    def add_to_archive(self, code: str, fitness: float = 0.0):
        """
        コードをアーカイブに追加

        Args:
            code: 追加するコード
            fitness: コードの適応度
        """
        code_hash = self._compute_hash(code)
        self.code_hashes.add(code_hash)

        features = self._extract_features(code)
        self.code_archive.append({
            'code': code,
            'hash': code_hash,
            'features': features,
            'fitness': fitness
        })

        # アーカイブサイズを制限
        if len(self.code_archive) > self.archive_size:
            # 適応度の低いものから削除
            self.code_archive.sort(key=lambda x: x['fitness'], reverse=True)
            removed = self.code_archive.pop()
            self.code_hashes.discard(removed['hash'])

    def _compute_hash(self, code: str) -> str:
        """
        コードのハッシュを計算

        Args:
            code: コード文字列

        Returns:
            ハッシュ値
        """
        # 空白を正規化してからハッシュ化
        normalized = re.sub(r'\s+', ' ', code.strip())
        return hashlib.md5(normalized.encode()).hexdigest()

    def _extract_features(self, code: str) -> Dict[str, any]:
        """
        コードから特徴を抽出

        Args:
            code: コード文字列

        Returns:
            特徴の辞書
        """
        features = {}

        # 行数
        features['num_lines'] = len(code.split('\n'))

        # テスト関数の数
        features['num_test_functions'] = code.count('def test_')

        # アサーションの数
        features['num_assertions'] = code.count('assert')

        # インポート文の数
        features['num_imports'] = code.count('import')

        # pytest固有の機能
        features['has_parametrize'] = '@pytest.mark.parametrize' in code
        features['has_fixture'] = '@pytest.fixture' in code
        features['has_mock'] = 'mock' in code.lower()

        # エッジケース関連のキーワード
        edge_case_keywords = ['None', 'empty', 'zero', 'negative', 'boundary', 'edge']
        features['edge_case_coverage'] = sum(
            1 for keyword in edge_case_keywords if keyword in code
        )

        # 例外処理
        features['has_raises'] = 'pytest.raises' in code or 'assertRaises' in code

        # コードの長さ
        features['code_length'] = len(code)

        # ユニークな識別子の数（簡易版）
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        features['unique_identifiers'] = len(set(identifiers))

        return features

    def _compute_similarity(
        self,
        features1: Dict[str, any],
        features2: Dict[str, any]
    ) -> float:
        """
        2つの特徴ベクトル間の類似度を計算

        Args:
            features1: 特徴ベクトル1
            features2: 特徴ベクトル2

        Returns:
            類似度（0.0〜1.0）
        """
        # 数値特徴の正規化類似度
        numeric_features = [
            'num_lines', 'num_test_functions', 'num_assertions',
            'num_imports', 'edge_case_coverage', 'code_length',
            'unique_identifiers'
        ]

        similarities = []

        for feature in numeric_features:
            val1 = features1.get(feature, 0)
            val2 = features2.get(feature, 0)

            # 正規化された差分を計算
            max_val = max(val1, val2, 1)  # ゼロ除算を防ぐ
            similarity = 1.0 - abs(val1 - val2) / max_val
            similarities.append(similarity)

        # ブール特徴の一致度
        boolean_features = [
            'has_parametrize', 'has_fixture', 'has_mock', 'has_raises'
        ]

        for feature in boolean_features:
            val1 = features1.get(feature, False)
            val2 = features2.get(feature, False)
            similarities.append(1.0 if val1 == val2 else 0.0)

        # 平均類似度を返す
        return sum(similarities) / len(similarities) if similarities else 0.0

    def get_diversity_score(self) -> float:
        """
        現在のアーカイブの多様性スコアを計算

        Returns:
            多様性スコア（0.0〜1.0、高いほど多様）
        """
        if len(self.code_archive) < 2:
            return 1.0

        # ペアワイズ類似度の平均を計算
        total_similarity = 0.0
        num_pairs = 0

        for i in range(len(self.code_archive)):
            for j in range(i + 1, len(self.code_archive)):
                similarity = self._compute_similarity(
                    self.code_archive[i]['features'],
                    self.code_archive[j]['features']
                )
                total_similarity += similarity
                num_pairs += 1

        avg_similarity = total_similarity / num_pairs if num_pairs > 0 else 0.0

        # 多様性は平均類似度の逆
        diversity = 1.0 - avg_similarity
        return max(0.0, min(1.0, diversity))

    def get_statistics(self) -> Dict[str, any]:
        """
        統計情報を取得

        Returns:
            統計情報の辞書
        """
        return {
            'archive_size': len(self.code_archive),
            'diversity_score': self.get_diversity_score(),
            'avg_fitness': (
                sum(item['fitness'] for item in self.code_archive) / len(self.code_archive)
                if self.code_archive else 0.0
            )
        }

    def clear(self):
        """アーカイブをクリア"""
        self.code_hashes.clear()
        self.code_archive.clear()
