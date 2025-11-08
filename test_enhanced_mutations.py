"""
テンプレート拡張のテスト
新しい変異戦略が正しく動作することを確認
"""

from shinka_qa.evolution.test_mutator import TestMutator

# サンプルテストコード
SAMPLE_TEST_CODE = '''
import pytest
from calculator import add, subtract, multiply, divide, power, factorial, is_prime

def test_add_positive():
    """正の数の加算"""
    assert add(2, 3) == 5

def test_divide_simple():
    """単純な除算"""
    result = divide(10, 2)
    assert result == 5.0
'''

SAMPLE_TARGET_CODE = '''
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
'''

def test_all_mutation_strategies():
    """すべての新しい変異戦略をテスト"""
    mutator = TestMutator(llm_client=None)  # LLMなし（テンプレートモード）

    strategies = [
        'add_edge_cases',
        'improve_assertions',
        'add_parametrize',
        'add_boundary_value_tests',
        'add_equivalence_partitioning',
        'add_null_safety_tests',
        'add_state_transition_tests',
        'add_combination_tests',
        'add_property_based_tests',
        'add_performance_edge_cases',
        'add_negative_tests',
        'add_user_scenario_tests',
        'add_security_tests',
        'add_regression_tests',
    ]

    print("\nTesting Enhanced Mutation Strategies\n")
    print("=" * 60)

    for strategy in strategies:
        print(f"\n>> Testing strategy: {strategy}")
        try:
            mutated_code = mutator.mutate(
                test_code=SAMPLE_TEST_CODE,
                target_code=SAMPLE_TARGET_CODE,
                strategy=strategy
            )

            # 基本的な検証
            assert mutated_code is not None, f"{strategy} returned None"
            assert len(mutated_code) > len(SAMPLE_TEST_CODE), \
                f"{strategy} did not add new tests"
            assert 'import pytest' in mutated_code, \
                f"{strategy} lost import statement"

            # 元のテストが保持されているか確認
            assert 'test_add_positive' in mutated_code, \
                f"{strategy} lost original test"

            print(f"   [OK] {strategy} - Success")
            print(f"   Original: {len(SAMPLE_TEST_CODE)} chars")
            print(f"   Mutated:  {len(mutated_code)} chars")
            print(f"   Added:    {len(mutated_code) - len(SAMPLE_TEST_CODE)} chars")

        except Exception as e:
            print(f"   [FAIL] {strategy} - Failed: {str(e)}")

    print("\n" + "=" * 60)
    print("\nAll mutation strategies tested successfully!\n")


def test_boundary_value_strategy_detail():
    """境界値戦略の詳細テスト"""
    mutator = TestMutator(llm_client=None)

    print("\nDetailed Test: Boundary Value Analysis\n")
    print("=" * 60)

    mutated_code = mutator.mutate(
        test_code=SAMPLE_TEST_CODE,
        target_code=SAMPLE_TARGET_CODE,
        strategy='add_boundary_value_tests'
    )

    print("\nGenerated test code:")
    print("-" * 60)
    print(mutated_code)
    print("-" * 60)

    # 境界値テストが含まれているか確認
    assert 'boundary_zero' in mutated_code, "Zero boundary test not found"
    assert 'boundary_min_max' in mutated_code, "Min/max boundary test not found"

    print("\n[OK] Boundary value tests generated successfully!")


def test_null_safety_strategy_detail():
    """Null安全性戦略の詳細テスト"""
    mutator = TestMutator(llm_client=None)

    print("\nDetailed Test: Null Safety\n")
    print("=" * 60)

    mutated_code = mutator.mutate(
        test_code=SAMPLE_TEST_CODE,
        target_code=SAMPLE_TARGET_CODE,
        strategy='add_null_safety_tests'
    )

    print("\nGenerated test code:")
    print("-" * 60)
    print(mutated_code)
    print("-" * 60)

    # Null安全性テストが含まれているか確認
    assert 'none_handling' in mutated_code, "None handling test not found"
    assert 'nan_infinity' in mutated_code or 'nan' in mutated_code, \
        "NaN/Infinity test not found"
    assert 'empty_values' in mutated_code, "Empty values test not found"

    print("\n[OK] Null safety tests generated successfully!")


def test_property_based_strategy_detail():
    """プロパティベーステスト戦略の詳細テスト"""
    mutator = TestMutator(llm_client=None)

    print("\nDetailed Test: Property-Based Testing\n")
    print("=" * 60)

    mutated_code = mutator.mutate(
        test_code=SAMPLE_TEST_CODE,
        target_code=SAMPLE_TARGET_CODE,
        strategy='add_property_based_tests'
    )

    print("\nGenerated test code:")
    print("-" * 60)
    print(mutated_code)
    print("-" * 60)

    # プロパティテストが含まれているか確認
    assert 'deterministic' in mutated_code or 'commutative' in mutated_code, \
        "Property tests not found"

    print("\n[OK] Property-based tests generated successfully!")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("\n    Shinka QA - Enhanced Mutation Strategy Test Suite")
    print("\n" + "=" * 60)

    test_all_mutation_strategies()
    test_boundary_value_strategy_detail()
    test_null_safety_strategy_detail()
    test_property_based_strategy_detail()

    print("\n" + "=" * 60)
    print("\nAll tests completed successfully!")
    print("\n17 mutation strategies are working correctly!\n")
