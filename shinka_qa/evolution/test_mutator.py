"""
テストコードの変異オペレータ
LLMを使用してテストコードを進化させる
"""

import re
from typing import List, Dict, Optional
from pathlib import Path


class TestMutator:
    """テストコード変異クラス"""

    # LLMへのプロンプトテンプレート
    MUTATION_PROMPTS = {
        'add_edge_cases': """
以下のテストコードに、エッジケースのテストを追加してください。

考慮すべきエッジケース:
- 空の入力（空文字列、空リスト、None）
- 境界値（0, -1, 最大値、最小値）
- 無効な型（期待される型と異なる入力）
- 特殊文字（Unicode, エスケープシーケンス）

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

改善されたテストコードを出力してください。
""",

        'improve_assertions': """
以下のテストコードのアサーションを改善してください。

改善ポイント:
- 単純な assert True/False を具体的な比較に置き換える
- assertEqual, assertIn, assertRaises などの専用メソッドを使用
- エラーメッセージを追加して、失敗時の原因を明確にする

現在のテストコード:
```python
{current_test_code}
```

改善されたテストコードを出力してください。
""",

        'add_parametrize': """
以下のテストコードに pytest.mark.parametrize を使用して、
複数のテストケースを効率的に実行できるようにしてください。

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

パラメータ化されたテストコードを出力してください。
""",

        'add_fixtures': """
以下のテストコードに pytest fixtures を追加して、
テストのセットアップとクリーンアップを改善してください。

現在のテストコード:
```python
{current_test_code}
```

改善されたテストコード（fixtureを含む）を出力してください。
""",

        'add_mocks': """
以下のテストコードに unittest.mock または pytest-mock を使用して、
外部依存をモック化し、テストの独立性を向上させてください。

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

モックを使用した改善されたテストコードを出力してください。
"""
    }

    def __init__(self, llm_client=None):
        """
        Args:
            llm_client: LLMクライアント（OpenAI, Anthropic等）
        """
        self.llm = llm_client

    def mutate(
        self,
        test_code: str,
        target_code: str,
        strategy: str,
        context: Dict = None
    ) -> str:
        """
        テストコードを変異させる

        Args:
            test_code: 現在のテストコード
            target_code: テスト対象のコード
            strategy: 変異戦略（'add_edge_cases', 'improve_assertions'等）
            context: 追加コンテキスト（カバレッジ情報等）

        Returns:
            変異後のテストコード
        """
        # プロンプトを構築
        prompt = self._build_prompt(test_code, target_code, strategy, context)

        # LLMで変異を生成
        if self.llm:
            mutated_code = self._call_llm(prompt)
        else:
            # LLMが利用できない場合は簡単な変異を適用
            mutated_code = self._simple_mutation(test_code, strategy)

        # コードブロックを抽出（```python ... ``` を除去）
        mutated_code = self._extract_code_block(mutated_code)

        return mutated_code

    def _build_prompt(
        self,
        test_code: str,
        target_code: str,
        strategy: str,
        context: Optional[Dict]
    ) -> str:
        """変異プロンプトを構築"""
        base_prompt = self.MUTATION_PROMPTS.get(
            strategy,
            self.MUTATION_PROMPTS['add_edge_cases']
        )

        prompt = base_prompt.format(
            current_test_code=test_code,
            target_function=target_code
        )

        # コンテキスト情報を追加
        if context and 'uncovered_lines' in context:
            prompt += f"\n\n未カバーの行: {context['uncovered_lines']}"

        if context and 'previous_failures' in context:
            prompt += f"\n\n以前の失敗: {context['previous_failures']}"

        return prompt

    def _call_llm(self, prompt: str) -> str:
        """LLMを呼び出してコードを生成"""
        # EVOLVE-BLOCK-START: llm_call
        try:
            response = self.llm.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは優秀なソフトウェアテストエンジニアです。"
                                   "高品質なpytestテストコードを生成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM call error: {e}")
            return prompt  # エラー時は元のコードを返す
        # EVOLVE-BLOCK-END

    def _extract_code_block(self, llm_response: str) -> str:
        """LLMの応答からコードブロックを抽出"""
        # ```python ... ``` を検出
        if '```python' in llm_response:
            start = llm_response.find('```python') + 9
            end = llm_response.find('```', start)
            if end != -1:
                return llm_response[start:end].strip()

        # ``` ... ``` を検出（言語指定なし）
        if '```' in llm_response:
            start = llm_response.find('```') + 3
            end = llm_response.find('```', start)
            if end != -1:
                return llm_response[start:end].strip()

        # コードブロックがない場合はそのまま返す
        return llm_response.strip()

    def _simple_mutation(self, test_code: str, strategy: str) -> str:
        """LLMなしで簡単な変異を適用（フォールバック）"""
        if strategy == 'add_edge_cases':
            # 簡単なエッジケーステストを追加
            return test_code + "\n\n# TODO: Add more edge case tests"
        elif strategy == 'improve_assertions':
            # assertをより具体的に変更（簡易版）
            # すでに is not None が含まれている場合は置換しない
            if 'is not None' not in test_code:
                # 正規表現を使って、assert result == value のパターンを改善
                improved_code = re.sub(
                    r'assert\s+(\w+)\s*==',
                    r'assert \1 is not None and \1 ==',
                    test_code
                )
                return improved_code
            return test_code
        else:
            return test_code
