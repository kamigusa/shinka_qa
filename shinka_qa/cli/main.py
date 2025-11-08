"""
CLIエントリーポイント
Shinka Quality のコマンドラインインターフェース
"""

import click
import yaml
from pathlib import Path
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

from ..core.evaluator import QualityEvaluator
from ..evolution.test_mutator import TestMutator
from ..evolution.island_model import IslandModel
from ..evolution.saturation_detector import CoverageSaturationDetector
from ..utils.test_runner import TestRunner
from ..visualization.report_generator import ReportGenerator
from ..visualization.lineage_tree import LineageTreeVisualizer
from ..llm.llm_client import create_llm_client, create_multi_provider_client


def safe_echo(message: str, **kwargs):
    """
    Windowsコンソールでも安全にメッセージを表示するヘルパー関数
    絵文字が表示できない場合は代替文字を使用
    """
    try:
        click.echo(message, **kwargs)
    except UnicodeEncodeError:
        # 絵文字を代替テキストに置換
        replacements = {
            '🔍': '[i]',
            '✅': '[+]',
            '💰': '[$]',
            '📊': '[=]',
            '⚠️': '[!]',
            '❌': '[x]'
        }
        safe_message = message
        for emoji, replacement in replacements.items():
            safe_message = safe_message.replace(emoji, replacement)
        click.echo(safe_message, **kwargs)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Shinka Quality - ソフトウェア品質改善のための進化的フレームワーク

    テストコードとテスト戦略を進化させ、テストカバレッジとバグ検出率を自動的に向上させます。
    """
    pass


@cli.command()
@click.option('--config', type=click.Path(exists=True), required=True,
              help='設定ファイルのパス（YAML）')
@click.option('--output-dir', type=click.Path(), default='results/',
              help='出力ディレクトリ（デフォルト: results/）')
@click.option('--verbose', is_flag=True, help='詳細ログを表示')
@click.option('--llm/--no-llm', default=False,
              help='LLMを使用するかどうか（デフォルト: 無効）')
def evolve(config, output_dir, verbose, llm):
    """
    テストスイートを進化させる

    指定された設定ファイルに基づいて、テストコードを自動的に改善します。
    """
    click.echo("Shinka Quality v1.0")
    click.echo("=" * 40)

    # 設定ファイルを読み込み
    config_path = Path(config)
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    if verbose:
        click.echo(f"\nConfiguration loaded from: {config_path}")

    # 設定を取得
    target_config = config_data.get('target', {})
    target_module = Path(target_config.get('module_path'))
    initial_test = Path(target_config.get('test_initial_path'))
    seeded_bugs = target_config.get('seeded_bugs_path')

    if not target_module.exists():
        click.echo(f"Error: Target module not found: {target_module}", err=True)
        return

    if not initial_test.exists():
        click.echo(f"Error: Initial test file not found: {initial_test}", err=True)
        return

    click.echo(f"\nConfiguration:")
    click.echo(f"  Target: {target_module.name}")

    # 評価器を初期化
    weights = config_data.get('fitness_weights', {})
    evaluator = QualityEvaluator(
        target_module_path=target_module,
        seeded_bugs_path=seeded_bugs if seeded_bugs else None,
        weights=weights
    )

    # ベースラインを設定
    click.echo("\nMeasuring baseline...")
    evaluator.set_baseline(initial_test)

    click.echo(f"  Initial Coverage: {evaluator.baseline_coverage:.1f}%")

    # 初期評価
    click.echo("\nEvaluating initial test suite...")
    fitness, metrics = evaluator.evaluate(initial_test)

    click.echo(f"  Coverage: {metrics['coverage']:.1f}%")
    click.echo(f"  Bug Detection: {metrics['bugs_detected']:.2f}")
    click.echo(f"  Execution Time: {metrics['execution_time']:.2f}s")
    click.echo(f"  Code Quality: {metrics['maintainability']:.2f}")
    click.echo(f"  Overall Fitness: {fitness:.2f}")

    # 出力ディレクトリを作成
    output_path = Path(output_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_path / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # 進化パラメータを取得
    evolution_config = config_data.get('evolution', {})
    num_generations = evolution_config.get('num_generations', 10)
    population_size = evolution_config.get('population_size', 20)
    num_islands = evolution_config.get('num_islands', 4)

    # LLMクライアントを初期化
    llm_client = None

    # コマンドライン引数が優先（--llm/--no-llm）
    if not llm:
        click.echo("LLM disabled: Using template-based mutations only (--no-llm)")
    else:
        # LLM有効の場合、設定ファイルから読み込み
        llm_config = config_data.get('llm', {})
        llm_model = llm_config.get('model', 'gpt-5-nano')
        llm_provider = llm_config.get('provider', 'openai')

        # providerが"none"の場合はLLMを無効化
        if llm_provider == "none" or llm_model == "none":
            click.echo("LLM disabled: Using fallback mutations only")
        elif llm_provider == "auto":
            # 複数プロバイダーの自動検出（コストの安い順に使用）
            safe_echo("🔍 Auto-detecting available LLM providers...")
            llm_client = create_multi_provider_client(auto_detect=True)

            if llm_client:
                safe_echo(f"✅ LLM enabled with multi-provider fallback")
                if hasattr(llm_client, 'get_available_providers'):
                    safe_echo("📊 Available providers (cheapest first):")
                    for provider in llm_client.get_available_providers():
                        safe_echo(f"   - {provider}")
            else:
                safe_echo("⚠️  No LLM providers detected: Using template-based mutations only")
        else:
            # 単一プロバイダーを使用
            llm_client = create_llm_client(
                provider=llm_provider,
                model=llm_model
            )

            if llm_client:
                cost = llm_client.get_cost_per_1m_tokens()
                click.echo(f"LLM enabled: Using {llm_client.get_provider_name()} {llm_client.get_model_name()}")
                safe_echo(f"💰 Cost: ${cost[0]:.3f}/${cost[1]:.3f} per 1M tokens (input/output)")
            else:
                click.echo("LLM not configured: Using simple fallback mutations")

    # テストミューテーターを初期化
    # ハイブリッドアプローチ: 最初は常にテンプレートベースから開始
    # カバレッジサチュレーション検出後、LLMが利用可能ならLLMモードに切り替え
    mutation_strategies = config_data.get('mutation_strategies', ['add_edge_cases'])
    mutator = TestMutator(llm_client=llm_client, force_template=True)

    # カバレッジサチュレーション検出器を初期化
    saturation_config = config_data.get('saturation_detection', {})
    saturation_detector = CoverageSaturationDetector(
        window_size=saturation_config.get('window_size', 5),
        improvement_threshold=saturation_config.get('improvement_threshold', 0.5),
        min_generations=saturation_config.get('min_generations', 10)
    )

    # 進化を実行
    click.echo(f"\nStarting evolution...")
    click.echo(f"  Generations: {num_generations}")
    click.echo(f"  Population per island: {population_size}")
    click.echo(f"  Islands: {num_islands}")

    island_model = IslandModel(
        num_islands=num_islands,
        population_size=population_size,
        migration_interval=max(2, num_generations // 3),
        migration_rate=0.1,
        elite_ratio=0.3
    )

    # 初期個体として現在のテストファイルを読み込み
    with open(initial_test, 'r', encoding='utf-8') as f:
        initial_code = f.read()

    # 適応度評価関数を定義
    def fitness_func(code_str):
        """テストコードの適応度を評価"""
        # テストファイルをtarget_moduleと同じディレクトリに保存
        # （インポートが正しく動作するように）
        temp_test_file = target_module.parent / 'temp_test_evolved.py'
        with open(temp_test_file, 'w', encoding='utf-8') as f:
            f.write(code_str)
        try:
            fitness, metrics = evaluator.evaluate(temp_test_file)
            return fitness, metrics
        finally:
            # 評価後にクリーンアップ
            if temp_test_file.exists():
                temp_test_file.unlink()

    # 変異関数を定義
    def mutate_func(code_str, target_code=""):
        """テストコードを変異させる"""
        # ランダムに戦略を選択
        import random
        strategy = random.choice(mutation_strategies)
        return mutator.mutate(code_str, str(target_module), strategy)

    # 島を初期化
    island_model.initialize(initial_code, fitness_func)

    # 各世代の進化を記録
    all_generations = []

    def generation_callback(gen, generation_bests, global_best):
        """各世代後に呼ばれるコールバック"""
        # カバレッジを記録
        current_coverage = global_best.metrics.get('coverage', 0) if global_best.metrics else 0
        saturation_detector.add_coverage(gen, current_coverage)

        # サチュレーション検出とLLM切り替え
        if saturation_detector.is_saturated() and mutator.force_template:
            click.echo(f"\n{'='*60}")
            safe_echo("📊 Coverage saturation detected!")
            stats = saturation_detector.get_statistics()
            click.echo(f"  Current coverage: {stats['current_coverage']:.1f}%")
            click.echo(f"  Recent improvement: {stats['recent_improvement']:.2f}%")
            click.echo(f"  Switching to LLM exploration mode...")
            click.echo(f"{'='*60}\n")

            # LLMモードに切り替え
            if llm_client:
                mutator.set_use_llm(True)
                safe_echo("✅ LLM exploration mode activated")
            else:
                safe_echo("⚠️  LLM client not available, continuing with template-based mutations")

        if verbose:
            click.echo(f"\nGeneration {gen}/{num_generations}")
            click.echo(f"  Best Fitness: {global_best.fitness:.3f}")
            if global_best.metrics:
                click.echo(f"  Coverage: {global_best.metrics.get('coverage', 0):.1f}%")
                click.echo(f"  Bug Detection: {global_best.metrics.get('bugs_detected', 0):.2f}")

            # テンプレートモードかLLMモードかを表示
            mode = "LLM Exploration" if not mutator.force_template else "Template-based"
            click.echo(f"  Mode: {mode}")

        # 世代情報を記録
        gen_data = {
            'generation': gen,
            'best_fitness': global_best.fitness,
            'best_metrics': global_best.metrics,
            'num_islands': len(generation_bests),
            'mode': 'llm' if not mutator.force_template else 'template',
            'saturation_stats': saturation_detector.get_statistics()
        }
        all_generations.append(gen_data)

        # この世代の最良個体を保存
        best_test_file = run_dir / f'best_test_gen{gen}.py'
        with open(best_test_file, 'w', encoding='utf-8') as f:
            f.write(global_best.test_code)

    # 進化を実行
    best_individual = island_model.evolve(
        generations=num_generations,
        mutate_func=mutate_func,
        fitness_func=fitness_func,
        target_code=str(target_module),
        callback=generation_callback
    )

    # 最終結果を保存
    results = {
        'config': config_data,
        'baseline': {
            'coverage': evaluator.baseline_coverage,
            'execution_time': evaluator.baseline_time
        },
        'initial_metrics': metrics,
        'initial_fitness': fitness,
        'final_metrics': best_individual.metrics,
        'final_fitness': best_individual.fitness,
        'improvement': {
            'coverage': best_individual.metrics.get('coverage', 0) - metrics.get('coverage', 0),
            'fitness': best_individual.fitness - fitness
        },
        'generations': all_generations,
        'timestamp': timestamp
    }

    results_file = run_dir / 'metrics.json'
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # 最終最良個体を保存
    final_test_file = run_dir / 'evolved_test.py'
    with open(final_test_file, 'w', encoding='utf-8') as f:
        f.write(best_individual.test_code)

    click.echo(f"\nEvolution Complete!")
    click.echo("=" * 40)
    click.echo(f"\nFinal Results:")
    click.echo(f"  Best Fitness: {best_individual.fitness:.3f} (improved by {best_individual.fitness - fitness:+.3f})")
    if best_individual.metrics:
        m = best_individual.metrics
        click.echo(f"  Final Coverage: {m.get('coverage', 0):.1f}% (improved by {m.get('coverage', 0) - metrics.get('coverage', 0):+.1f}%)")
        click.echo(f"  Final Bug Detection: {m.get('bugs_detected', 0):.2f}")

    click.echo(f"\nResults saved to: {run_dir}/")
    click.echo(f"  - evolved_test.py (best test suite)")
    click.echo(f"  - metrics.json (detailed metrics)")
    click.echo(f"  - best_test_gen*.py (best from each generation)")

    if verbose:
        click.echo(f"\nDetailed final metrics:")
        click.echo(json.dumps(best_individual.metrics, indent=2))


@cli.command()
@click.option('--results-dir', type=click.Path(exists=True), required=True,
              help='結果ディレクトリのパス')
@click.option('--generate-report', is_flag=True, help='HTMLレポートを生成')
def visualize(results_dir, generate_report):
    """
    進化の結果を可視化する

    指定されたディレクトリの結果を表示し、オプションでHTMLレポートを生成します。
    """
    click.echo(f"Loading results from: {results_dir}")

    results_path = Path(results_dir)
    metrics_file = results_path / 'metrics.json'

    if not metrics_file.exists():
        click.echo(f"Error: metrics.json not found in {results_dir}", err=True)
        return

    # メトリクスを読み込み
    with open(metrics_file, 'r', encoding='utf-8') as f:
        metrics = json.load(f)

    click.echo("\nMetrics Summary:")
    click.echo(f"  Baseline Coverage: {metrics['baseline']['coverage']:.1f}%")

    if 'initial_metrics' in metrics:
        im = metrics['initial_metrics']
        click.echo(f"  Current Coverage: {im.get('coverage', 0):.1f}%")
        click.echo(f"  Bug Detection: {im.get('bugs_detected', 0):.2f}")
        click.echo(f"  Fitness Score: {metrics.get('initial_fitness', 0):.2f}")

    # HTMLレポートを生成
    if generate_report:
        click.echo("\nGenerating HTML report...")
        try:
            report_gen = ReportGenerator(results_path)
            html_file = report_gen.generate_html_report()
            click.echo(f"HTML report generated: {html_file}")

            # サマリーテキストも生成
            summary = report_gen.generate_summary_text()
            click.echo("\n" + summary)

            # 系譜ツリーを生成
            lineage_viz = LineageTreeVisualizer(results_path)
            # サンプルの系譜データを追加（実際の進化データがある場合はそれを使用）
            lineage_viz.add_node("gen0_0", 0, metrics.get('initial_fitness', 0))

            tree_file = lineage_viz.save_tree()
            click.echo(f"Lineage tree saved: {tree_file}")

        except Exception as e:
            click.echo(f"Error generating report: {e}", err=True)

    click.echo(f"\nTip: Use --generate-report to create an HTML report")
    click.echo(f"     Or open {results_dir}/metrics.json to see detailed results")


@cli.command()
@click.option('--config', type=click.Path(exists=True), required=True,
              help='設定ファイルのパス')
def benchmark(config):
    """
    初期テストとの性能比較を実行

    ベースラインテストの性能を測定してレポートします。
    """
    click.echo("Running benchmark...")
    click.echo("=" * 40)

    # 設定ファイルを読み込み
    config_path = Path(config)
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    target_config = config_data.get('target', {})
    target_module = Path(target_config.get('module_path'))
    initial_test = Path(target_config.get('test_initial_path'))

    if not target_module.exists() or not initial_test.exists():
        click.echo("Error: Target files not found", err=True)
        return

    # テストランナーで実行
    runner = TestRunner()
    result = runner.run_with_coverage(
        initial_test,
        target_module,
        target_module.parent
    )

    click.echo("\nBenchmark Results:")
    click.echo(f"  Tests Passed: {result.get('passed', 0)}")
    click.echo(f"  Tests Failed: {result.get('failed', 0)}")
    click.echo(f"  Coverage: {result.get('coverage', 0):.1f}%")
    click.echo(f"  Success: {'YES' if result.get('success') else 'NO'}")

    if not result.get('success'):
        click.echo("\nWARNING: Some tests failed. Check the output above for details.")


@cli.command()
@click.argument('test_file', type=click.Path(exists=True))
@click.argument('target_module', type=click.Path(exists=True))
def validate(test_file, target_module):
    """
    テストファイルを検証する

    指定されたテストファイルの妥当性をチェックします。
    """
    click.echo(f"Validating test file: {test_file}")

    runner = TestRunner()
    is_valid, error_msg = runner.validate_test_file(Path(test_file))

    if is_valid:
        click.echo("Test file is valid")

        # 実行テストも行う
        result = runner.run_tests(Path(test_file), Path(target_module).parent)
        click.echo(f"\nTest Execution:")
        click.echo(f"  Passed: {result.get('passed', 0)}")
        click.echo(f"  Failed: {result.get('failed', 0)}")
        click.echo(f"  Success: {'YES' if result.get('success') else 'NO'}")
    else:
        click.echo(f"Validation failed: {error_msg}", err=True)


if __name__ == '__main__':
    cli()
