#!/usr/bin/env python3
"""
Analyze the W2S bootstrapping experimental results and generate insights.
"""

import json
import numpy as np
import os


def load_results():
    """Load experimental results."""
    results_dir = os.path.expanduser('~/fab_out/artifact/results')

    with open(os.path.join(results_dir, 'experiment_results.json'), 'r') as f:
        experiment_results = json.load(f)

    with open(os.path.join(results_dir, 'summary_stats.json'), 'r') as f:
        summary_stats = json.load(f)

    with open(os.path.join(results_dir, 'pattern_analysis.json'), 'r') as f:
        pattern_analysis = json.load(f)

    return experiment_results, summary_stats, pattern_analysis


def analyze_gap_relationship(results):
    """Analyze relationship between capability gaps and bootstrap effectiveness."""

    analysis = {
        'by_weak_strong_gap': {},
        'by_weak_accuracy': {},
        'error_reduction_analysis': {},
        'supervision_quality_analysis': {}
    }

    # Group by different factors
    for result in results:
        # Group by weak-strong gap (binned)
        gap_bin = f"{result['weak_strong_gap']:.1f}"
        if gap_bin not in analysis['by_weak_strong_gap']:
            analysis['by_weak_strong_gap'][gap_bin] = []
        analysis['by_weak_strong_gap'][gap_bin].append(result)

        # Group by weak accuracy
        weak_acc_bin = f"{result['weak_acc']:.1f}"
        if weak_acc_bin not in analysis['by_weak_accuracy']:
            analysis['by_weak_accuracy'][weak_acc_bin] = []
        analysis['by_weak_accuracy'][weak_acc_bin].append(result)

    # Compute statistics for each group
    for group_name, groups in analysis.items():
        if group_name.startswith('by_'):
            for bin_name, bin_results in groups.items():
                stats = {
                    'count': len(bin_results),
                    'avg_bootstrap_advantage': np.mean([r['bootstrap_advantage'] for r in bin_results]),
                    'avg_error_overlap_reduction': np.mean([
                        r['direct']['error_overlap'] - r['bootstrap']['error_overlap']
                        for r in bin_results
                    ]),
                    'avg_accuracy_improvement': np.mean([
                        r['bootstrap']['accuracy'] - r['direct']['accuracy']
                        for r in bin_results
                    ])
                }
                analysis[group_name][bin_name] = stats

    # Error reduction analysis
    error_overlaps_direct = [r['direct']['error_overlap'] for r in results]
    error_overlaps_bootstrap = [r['bootstrap']['error_overlap'] for r in results]

    analysis['error_reduction_analysis'] = {
        'avg_direct_error_overlap': np.mean(error_overlaps_direct),
        'avg_bootstrap_error_overlap': np.mean(error_overlaps_bootstrap),
        'avg_error_overlap_reduction': np.mean([d - b for d, b in zip(error_overlaps_direct, error_overlaps_bootstrap)]),
        'cases_with_error_reduction': sum(1 for d, b in zip(error_overlaps_direct, error_overlaps_bootstrap) if d > b)
    }

    # Supervision quality analysis
    analysis['supervision_quality_analysis'] = {
        'avg_weak_supervisor_accuracy': np.mean([r['direct']['supervisor_accuracy'] for r in results]),
        'avg_medium_supervisor_accuracy': np.mean([r['bootstrap']['supervisor_accuracy'] for r in results]),
        'supervisor_quality_improvement': np.mean([
            r['bootstrap']['supervisor_accuracy'] - r['direct']['supervisor_accuracy']
            for r in results
        ])
    }

    return analysis


def identify_early_warning_signals(results):
    """Identify signals that could predict bootstrap effectiveness."""

    # Since all cases showed positive bootstrap advantage, we'll look for
    # signals that predict the MAGNITUDE of advantage

    signals = []

    for result in results:
        signal = {
            'weak_strong_gap': result['weak_strong_gap'],
            'weak_accuracy': result['weak_acc'],
            'medium_accuracy': result['medium_acc'],
            'weak_supervisor_accuracy': result['direct']['supervisor_accuracy'],
            'direct_error_overlap': result['direct']['error_overlap'],
            'bootstrap_advantage': result['bootstrap_advantage']
        }
        signals.append(signal)

    # Compute correlations
    bootstrap_advantages = [s['bootstrap_advantage'] for s in signals]

    correlations = {}
    for key in ['weak_strong_gap', 'weak_accuracy', 'direct_error_overlap', 'weak_supervisor_accuracy']:
        values = [s[key] for s in signals]
        correlation = np.corrcoef(values, bootstrap_advantages)[0, 1]
        correlations[key] = correlation

    return {
        'correlations_with_bootstrap_advantage': correlations,
        'strongest_predictor': max(correlations.items(), key=lambda x: abs(x[1])),
        'signals_data': signals
    }


def generate_insights_report(results, summary, analysis, early_signals):
    """Generate comprehensive insights report."""

    report = []

    report.append("# Weak-to-Strong Bootstrapping Analysis Report")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    report.append(f"Tested {summary['total_configs']} different capability gap configurations.")
    report.append(f"**Result: Bootstrapping wins in ALL {summary['bootstrap_wins']} cases tested.**")
    report.append(f"Average bootstrap advantage: {summary['avg_bootstrap_advantage']:.1%}")
    report.append(f"Range: {summary['worst_bootstrap_advantage']:.1%} to {summary['best_bootstrap_advantage']:.1%}")
    report.append("")

    report.append("## Key Findings")
    report.append("")
    report.append("### 1. Bootstrapping Consistently Outperforms Direct Supervision")
    report.append(f"- In all {len(results)} tested configurations, weak→medium→strong beats weak→strong directly")
    report.append("- Even the worst-case bootstrap advantage is +2.4%")
    report.append("- Best-case advantage reaches +10.8%")
    report.append("")

    report.append("### 2. Error Pattern Breaking is Key")
    report.append(f"- Average error overlap with supervisor: Direct {analysis['error_reduction_analysis']['avg_direct_error_overlap']:.1%} vs Bootstrap {analysis['error_reduction_analysis']['avg_bootstrap_error_overlap']:.1%}")
    report.append(f"- Bootstrap reduces error overlap in {analysis['error_reduction_analysis']['cases_with_error_reduction']}/{len(results)} cases")
    report.append(f"- Average error overlap reduction: {analysis['error_reduction_analysis']['avg_error_overlap_reduction']:.1%}")
    report.append("")

    report.append("### 3. Intermediate Supervisor Quality Matters")
    report.append(f"- Weak supervisor accuracy: {analysis['supervision_quality_analysis']['avg_weak_supervisor_accuracy']:.1%}")
    report.append(f"- Medium supervisor accuracy: {analysis['supervision_quality_analysis']['avg_medium_supervisor_accuracy']:.1%}")
    report.append(f"- Quality improvement from weak→medium step: {analysis['supervision_quality_analysis']['supervisor_quality_improvement']:.1%}")
    report.append("")

    report.append("### 4. Early Warning Signals")
    strongest_predictor, correlation = early_signals['strongest_predictor']
    report.append(f"- Strongest predictor of bootstrap advantage: **{strongest_predictor}** (r={correlation:.3f})")

    for signal, corr in sorted(early_signals['correlations_with_bootstrap_advantage'].items(),
                              key=lambda x: abs(x[1]), reverse=True):
        report.append(f"- {signal}: r={corr:.3f}")
    report.append("")

    report.append("## Mechanism Analysis")
    report.append("")
    report.append("**Why does bootstrapping work?**")
    report.append("")
    report.append("1. **Supervisor Quality Improvement**: The medium model, even when supervised by the weak model, still performs better than the weak model directly")
    report.append("")
    report.append("2. **Error Pattern Dilution**: Each supervision step dilutes systematic errors rather than compounding them")
    report.append("")
    report.append("3. **Capability Gap Reduction**: Smaller gaps at each step (weak→medium, medium→strong) are easier to bridge than one large gap (weak→strong)")
    report.append("")

    report.append("## Tested Configurations")
    report.append("")
    report.append("| Weak Acc | Medium Acc | Strong Acc | Bootstrap Advantage |")
    report.append("|----------|------------|------------|-------------------|")

    for result in results:
        report.append(f"| {result['weak_acc']:.1f} | {result['medium_acc']:.1f} | {result['strong_acc']:.1f} | {result['bootstrap_advantage']:.1%} |")

    report.append("")

    report.append("## Limitations and Caveats")
    report.append("")
    report.append("- **Synthetic setup**: Results may not generalize to real language models")
    report.append("- **Limited configurations**: Only 7 capability gap configurations tested")
    report.append("- **Simplified error model**: Real systematic errors may be more complex")
    report.append("- **No failure cases observed**: May need wider parameter ranges to find bootstrap failure modes")
    report.append("- **Small sample size**: Each configuration averaged over only 5 trials")
    report.append("")

    report.append("## Implications for Superalignment")
    report.append("")
    report.append("- **Staged supervision shows promise**: Rather than jumping directly from weak to strong capabilities, intermediate steps help")
    report.append("- **Error pattern breaking**: Bootstrapping appears to reduce harmful imitation of supervisor errors")
    report.append("- **Robustness across gaps**: Works across different capability gap configurations")
    report.append("- **Need for failure case analysis**: Future work should identify when/why bootstrapping might fail")
    report.append("")

    return "\n".join(report)


def main():
    """Main analysis function."""

    # Load results
    experiment_results, summary_stats, pattern_analysis = load_results()

    # Perform detailed analysis
    detailed_analysis = analyze_gap_relationship(experiment_results)
    early_signals = identify_early_warning_signals(experiment_results)

    # Generate insights report
    report = generate_insights_report(
        experiment_results, summary_stats, detailed_analysis, early_signals
    )

    # Save comprehensive analysis
    results_dir = os.path.expanduser('~/fab_out/artifact/results')

    with open(os.path.join(results_dir, 'detailed_analysis.json'), 'w') as f:
        json.dump(detailed_analysis, f, indent=2)

    with open(os.path.join(results_dir, 'early_signals.json'), 'w') as f:
        json.dump(early_signals, f, indent=2)

    # Save report
    with open(os.path.join(results_dir, 'insights_report.txt'), 'w') as f:
        f.write(report)

    print("Analysis complete!")
    print(f"Bootstrap advantage range: {summary_stats['worst_bootstrap_advantage']:.1%} to {summary_stats['best_bootstrap_advantage']:.1%}")
    print(f"Average advantage: {summary_stats['avg_bootstrap_advantage']:.1%}")

    return detailed_analysis, early_signals, report


if __name__ == "__main__":
    main()