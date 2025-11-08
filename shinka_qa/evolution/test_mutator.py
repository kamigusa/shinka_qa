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
- 例外が期待される場合は pytest.raises を使用

重要な指示:
1. 既存のテストコードをすべて含めてください
2. 新しいテスト関数を追加してください（既存を削除しないでください）
3. 各テストは独立して実行可能でなければなりません
4. import文を忘れずに含めてください
5. 完全な実行可能なPythonコードのみを返してください

例:
```python
import pytest
from calculator import divide

def test_divide_by_zero():
    \"\"\"ゼロ除算のテスト\"\"\"
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_none_input():
    \"\"\"None入力のテスト\"\"\"
    with pytest.raises(TypeError):
        divide(None, 5)
```

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

改善されたテストコード（元のテスト + 新しいエッジケーステスト）を出力してください。
""",

        'improve_assertions': """
以下のテストコードのアサーションを改善してください。

改善ポイント:
- 単純な assert True/False を具体的な比較に置き換える
- 値のチェックを追加（assert result is not None）
- 型のチェックを追加（assert isinstance(result, expected_type)）
- エラーメッセージを追加

重要: 元のテストコードをすべて含め、アサーションのみを改善してください。

例:
```python
# 改善前
def test_add():
    result = add(2, 3)
    assert result == 5

# 改善後
def test_add():
    result = add(2, 3)
    assert result is not None, "Result should not be None"
    assert isinstance(result, (int, float)), "Result should be numeric"
    assert result == 5, f"Expected 5 but got {{result}}"
```

現在のテストコード:
```python
{current_test_code}
```

改善されたテストコードを出力してください。
""",

        'add_parametrize': """
以下のテストコードに pytest.mark.parametrize を使用して、
複数のテストケースを効率的に実行できるようにしてください。

重要: 元のテストコードもすべて含めてください。

例:
```python
import pytest
from calculator import add

# 既存のテスト（保持）
def test_add_positive():
    assert add(2, 3) == 5

# 新しいパラメータ化テスト（追加）
@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (1, 1, 2),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -3, -8),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

現在のテストコード:
```python
{current_test_code}
```

テスト対象の関数:
```python
{target_function}
```

改善されたテストコード（元のテスト + パラメータ化されたテスト）を出力してください。
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

    def __init__(self, llm_client=None, model="gpt-4"):
        """
        Args:
            llm_client: LLMクライアント（OpenAI, Anthropic等）
            model: 使用するLLMモデル名
        """
        self.llm = llm_client
        self.model = model

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
        mutated_code = None
        if self.llm:
            mutated_code = self._call_llm(prompt)

        # LLMが失敗した場合、またはLLMが利用できない場合はフォールバックを使用
        if mutated_code is None:
            mutated_code = self._simple_mutation(test_code, strategy)
        else:
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
            # temperatureはgpt-5-nanoではサポートされていないため、モデルに応じて設定
            params = {
                "model": self.model,
                "messages": [
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
                "max_completion_tokens": 2000
            }

            # gpt-5-nano以外のモデルではtemperatureを設定
            if not ("gpt-5" in self.model.lower() and "nano" in self.model.lower()):
                params["temperature"] = 0.7

            response = self.llm.chat.completions.create(**params)

            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM call error: {e}")
            return None  # エラー時はNoneを返してフォールバックを使う
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
        import random

        if strategy == 'add_edge_cases':
            # テスト対象の関数を抽出
            imports = re.findall(r'from \w+ import (.+)', test_code)
            if imports:
                functions = [f.strip() for f in imports[0].split(',')]
                # ランダムに関数を選択してエッジケーステストを追加
                func = random.choice(functions)

                # 関数ごとに特化したテストを生成
                if func == 'divide':
                    edge_case_tests = f"""

def test_divide_by_zero():
    \"\"\"Test division by zero\"\"\"
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_negative():
    \"\"\"Test division with negative numbers\"\"\"
    assert divide(10, -2) == -5.0
    assert divide(-10, 2) == -5.0
"""
                elif func == 'power':
                    edge_case_tests = f"""

def test_power_type_error():
    \"\"\"Test power with invalid types\"\"\"
    with pytest.raises(TypeError, match="Both arguments must be numbers"):
        power("string", 2)
    with pytest.raises(TypeError, match="Both arguments must be numbers"):
        power(2, "string")

def test_power_various():
    \"\"\"Test power with various inputs\"\"\"
    assert power(2, 0) == 1
    assert power(5, 2) == 25
    assert power(10, 3) == 1000
"""
                elif func == 'factorial':
                    edge_case_tests = f"""

def test_factorial_positive():
    \"\"\"Test factorial with positive numbers\"\"\"
    assert factorial(5) == 120
    assert factorial(3) == 6
    assert factorial(4) == 24

def test_factorial_edge_zero():
    \"\"\"Zero input test\"\"\"
    try:
        result = factorial(0)
        assert result is not None
    except (ValueError, TypeError):
        pass

def test_factorial_edge_negative():
    \"\"\"Negative input test\"\"\"
    with pytest.raises(ValueError):
        factorial(-1)

def test_factorial_type_error():
    \"\"\"None input test\"\"\"
    with pytest.raises(TypeError):
        factorial(None)
"""
                elif func == 'is_prime':
                    edge_case_tests = f"""

def test_is_prime_primes():
    \"\"\"Test with actual prime numbers\"\"\"
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(5) == True
    assert is_prime(7) == True
    assert is_prime(11) == True
    assert is_prime(13) == True

def test_is_prime_non_primes():
    \"\"\"Test with composite numbers\"\"\"
    assert is_prime(4) == False
    assert is_prime(6) == False
    assert is_prime(8) == False
    assert is_prime(9) == False
    assert is_prime(10) == False

def test_is_prime_edge():
    \"\"\"Edge cases for is_prime\"\"\"
    assert is_prime(0) == False
    assert is_prime(1) == False
    assert is_prime(-5) == False

def test_is_prime_type_error():
    \"\"\"Type error test\"\"\"
    with pytest.raises(TypeError):
        is_prime(None)
"""
                else:
                    # デフォルトのエッジケーステスト
                    edge_case_tests = f"""

def test_{func}_edge_case_zero():
    \"\"\"Zero input test\"\"\"
    try:
        result = {func}(0)
        assert result is not None
    except (ValueError, TypeError):
        pass  # Expected for invalid input

def test_{func}_edge_case_negative():
    \"\"\"Negative input test\"\"\"
    try:
        result = {func}(-1)
        assert result is not None
    except (ValueError, TypeError):
        pass  # Expected for invalid input

def test_{func}_edge_case_none():
    \"\"\"None input test\"\"\"
    with pytest.raises((ValueError, TypeError)):
        {func}(None)
"""
                return test_code + edge_case_tests
            return test_code

        elif strategy == 'improve_assertions':
            # assertをより具体的に変更
            if 'is not None' not in test_code:
                improved_code = re.sub(
                    r'assert\s+(\w+)\s*==',
                    r'assert \1 is not None and \1 ==',
                    test_code
                )
                return improved_code
            return test_code

        elif strategy == 'add_parametrize':
            # 既存のテストにparametrizeを追加
            # test_add_positiveのような関数を見つけて拡張
            test_match = re.search(r'def (test_\w+)\(\):\s+.*?assert (\w+)\(([^)]+)\)', test_code, re.DOTALL)
            if test_match:
                func_name = test_match.group(2)

                # 元のテストコードを完全に保持し、新しいテストのみを追加
                parametrized_test = f"""

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (5, -3, 2),
])
def test_{func_name}_parametrized(a, b, expected):
    \"\"\"Parametrized test for {func_name}\"\"\"
    result = {func_name}(a, b)
    assert result == expected
"""
                # 元のコードをそのまま保持して、最後に新しいテストを追加
                return test_code + parametrized_test
            return test_code
        else:
            return test_code
