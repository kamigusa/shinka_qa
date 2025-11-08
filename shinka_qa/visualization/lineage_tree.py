"""
系譜ツリー可視化
進化の系譜を視覚的に表現
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json


class LineageNode:
    """系譜ツリーのノード"""

    def __init__(
        self,
        node_id: str,
        generation: int,
        fitness: float,
        parent_id: Optional[str] = None,
        strategy: str = ""
    ):
        self.node_id = node_id
        self.generation = generation
        self.fitness = fitness
        self.parent_id = parent_id
        self.strategy = strategy
        self.children: List['LineageNode'] = []


class LineageTreeVisualizer:
    """系譜ツリー可視化クラス"""

    def __init__(self, results_dir: Path):
        """
        Args:
            results_dir: 結果ディレクトリのパス
        """
        self.results_dir = Path(results_dir)
        self.nodes: Dict[str, LineageNode] = {}

    def add_node(
        self,
        node_id: str,
        generation: int,
        fitness: float,
        parent_id: Optional[str] = None,
        strategy: str = ""
    ):
        """
        ノードを追加

        Args:
            node_id: ノードID
            generation: 世代番号
            fitness: 適応度
            parent_id: 親ノードのID
            strategy: 使用した戦略
        """
        node = LineageNode(node_id, generation, fitness, parent_id, strategy)
        self.nodes[node_id] = node

        # 親ノードに子として追加
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].children.append(node)

    def generate_ascii_tree(self) -> str:
        """
        ASCIIアートで系譜ツリーを生成

        Returns:
            ASCIIツリーの文字列
        """
        if not self.nodes:
            return "No lineage data available."

        # ルートノード（親がないノード）を見つける
        root_nodes = [node for node in self.nodes.values() if node.parent_id is None]

        if not root_nodes:
            return "No root nodes found."

        lines = []
        lines.append("Evolution Lineage Tree")
        lines.append("=" * 50)
        lines.append("")

        for root in root_nodes:
            self._render_node(root, lines, prefix="", is_last=True)

        return "\n".join(lines)

    def _render_node(
        self,
        node: LineageNode,
        lines: List[str],
        prefix: str = "",
        is_last: bool = True
    ):
        """
        ノードを再帰的にレンダリング

        Args:
            node: レンダリングするノード
            lines: 出力行のリスト
            prefix: 行のプレフィックス
            is_last: 最後の子かどうか
        """
        # 現在のノードを描画
        connector = "+-- " if is_last else "|-- "
        node_info = f"Gen{node.generation} (fitness: {node.fitness:.3f})"
        if node.strategy:
            node_info += f" [{node.strategy}]"

        lines.append(f"{prefix}{connector}{node_info}")

        # 子ノードを描画
        if node.children:
            extension = "    " if is_last else "|   "
            for i, child in enumerate(node.children):
                self._render_node(
                    child,
                    lines,
                    prefix=prefix + extension,
                    is_last=(i == len(node.children) - 1)
                )

    def generate_html_tree(self) -> str:
        """
        HTMLで系譜ツリーを生成

        Returns:
            HTML文字列
        """
        if not self.nodes:
            return "<p>No lineage data available.</p>"

        # 世代ごとにノードをグループ化
        generations: Dict[int, List[LineageNode]] = {}
        for node in self.nodes.values():
            if node.generation not in generations:
                generations[node.generation] = []
            generations[node.generation].append(node)

        html = """
<div class="lineage-tree">
    <style>
        .lineage-tree {
            font-family: 'Courier New', monospace;
            background: #f9fafb;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
        }
        .generation {
            margin-bottom: 20px;
        }
        .generation-title {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        .node {
            display: inline-block;
            background: white;
            border: 2px solid #667eea;
            border-radius: 5px;
            padding: 10px;
            margin: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .node-fitness {
            font-weight: bold;
            color: #10b981;
        }
        .node-strategy {
            font-size: 0.9em;
            color: #666;
            font-style: italic;
        }
    </style>
"""

        # 世代ごとに表示
        for gen in sorted(generations.keys()):
            nodes = generations[gen]
            html += f'    <div class="generation">\n'
            html += f'        <div class="generation-title">Generation {gen}</div>\n'

            for node in sorted(nodes, key=lambda x: x.fitness, reverse=True):
                html += f'        <div class="node">\n'
                html += f'            <div>ID: {node.node_id}</div>\n'
                html += f'            <div class="node-fitness">Fitness: {node.fitness:.3f}</div>\n'
                if node.strategy:
                    html += f'            <div class="node-strategy">Strategy: {node.strategy}</div>\n'
                html += f'        </div>\n'

            html += '    </div>\n'

        html += '</div>'

        return html

    def export_to_json(self) -> str:
        """
        系譜データをJSONにエクスポート

        Returns:
            JSON文字列
        """
        data = {
            'nodes': [
                {
                    'id': node.node_id,
                    'generation': node.generation,
                    'fitness': node.fitness,
                    'parent_id': node.parent_id,
                    'strategy': node.strategy,
                    'num_children': len(node.children)
                }
                for node in self.nodes.values()
            ]
        }

        return json.dumps(data, indent=2)

    def save_tree(self, output_file: Optional[Path] = None):
        """
        系譜ツリーをファイルに保存

        Args:
            output_file: 出力ファイルのパス（Noneの場合はresults_dir/lineage_tree.txt）
        """
        if output_file is None:
            output_file = self.results_dir / 'lineage_tree.txt'

        tree_text = self.generate_ascii_tree()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tree_text)

        return output_file

    def get_statistics(self) -> Dict[str, Any]:
        """
        系譜ツリーの統計情報を取得

        Returns:
            統計情報の辞書
        """
        if not self.nodes:
            return {}

        fitnesses = [node.fitness for node in self.nodes.values()]
        generations = [node.generation for node in self.nodes.values()]

        return {
            'total_nodes': len(self.nodes),
            'max_generation': max(generations) if generations else 0,
            'best_fitness': max(fitnesses) if fitnesses else 0.0,
            'avg_fitness': sum(fitnesses) / len(fitnesses) if fitnesses else 0.0
        }
