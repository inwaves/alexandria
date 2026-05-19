# Bootstrapping Through Intermediate Capacities in Weak-to-Strong Generalization

## Summary

This research tests the key bootstrapping claim from weak-to-strong generalization: whether staged supervision (weak→medium→strong) outperforms direct supervision (weak→strong) across different capability gaps. Using a synthetic classification task with controllable model capabilities and systematic error patterns, we find **bootstrapping consistently wins across all tested configurations**, with accuracy advantages ranging from 2.4% to 10.8% (average 6.4%).

## Research Question

When does staged weak→medium→strong supervision beat direct weak→strong supervision? What are the failure modes and early warning signals?

## Methodology

**Synthetic Setup**: 10-class classification task with three "models" (weak, medium, strong) having different base accuracies and systematic error patterns. Models make controlled mistakes: weak models have high systematic error rates on specific class pairs (0→1, 2→3, 4→5), medium models fewer, strong models minimal.

**Experimental Design**:
- 7 capability gap configurations tested
- 5 trials per configuration for robustness
- Direct supervision: weak model labels → strong model training
- Bootstrap supervision: weak labels → medium training → medium labels → strong training
- Measured: accuracy improvement, error pattern overlap, supervision quality

**Key Innovation**: Models can either ELICIT latent capability or IMITATE supervisor errors based on supervision strength and error pattern adoption rates.

## Key Findings

### 1. Bootstrapping Always Wins
- **7/7 configurations show positive bootstrap advantage**
- Range: +2.4% to +10.8% accuracy improvement
- Average advantage: +6.4%
- No failure cases observed in tested parameter range

### 2. Error Pattern Breaking is the Core Mechanism
- Direct supervision: 29.9% error overlap with weak supervisor
- Bootstrap supervision: 21.9% error overlap
- **8.0% average reduction in error overlap**
- Staged supervision dilutes rather than compounds systematic errors

### 3. Intermediate Supervisor Quality Drives Success
- Weak supervisor accuracy: 29.6%
- Medium supervisor accuracy: 42.1% (+12.5% improvement)
- Even weak→medium supervision improves supervisor quality significantly

### 4. Predictable from Early Signals
- **Strongest predictor**: Lower weak accuracy → higher bootstrap advantage (r=-0.789)
- Also predictive: weak supervisor accuracy (r=-0.769), capability gap size (r=0.705)
- **Practical insight**: Bootstrapping most valuable when weak supervisor is very poor

## Gap Regime Analysis

| Weak→Medium→Strong | Bootstrap Advantage | Pattern |
|-------------------|--------------------|---------|
| 0.3→0.5→0.7       | 4.6%               | Small uniform gaps |
| 0.3→0.6→0.9       | 7.3%               | Medium gaps |
| 0.2→0.5→0.9       | 8.3%               | Large weak-strong gap |
| 0.2→0.7→0.8       | 10.8%              | Large first jump, small second |
| 0.5→0.6→0.9       | 2.4%               | Small first jump, large second |

**Pattern**: Bootstrapping advantage increases when (1) weak model is very poor, (2) total capability gap is large, (3) first jump (weak→medium) is substantial.

## Limitations and Caveats

- **Synthetic only**: May not generalize to real LLM training dynamics
- **No failure cases**: Parameter range may be too narrow to find bootstrap failure modes
- **Simplified error model**: Real systematic errors likely more complex
- **Small scale**: Only 7 configurations, 5 trials each
- **Goodhart risk**: Optimizing for accuracy may miss other important failure modes

## Implications for Superalignment

**Positive**: Staged supervision shows promise as a more robust approach than direct weak-to-strong supervision. The error pattern dilution mechanism suggests bootstrapping could reduce harmful imitation behaviors.

**Critical gaps**: Need to identify failure modes and test on realistic tasks. Real superalignment may face different tradeoffs (e.g., deception, goal misgeneralization) not captured in synthetic accuracy metrics.

**Next steps**: Test bootstrapping on larger models, identify failure regimes, investigate whether results hold for safety-relevant capabilities vs. just accuracy.

## Evidence Summary

All claims supported by controlled experiments with measurable outcomes:
- Experiment design: `code/w2s_bootstrap_experiment.py`
- Raw results: `results/experiment_results.json` (7 configurations × 5 trials)
- Statistical analysis: `results/detailed_analysis.json`
- Pattern identification: `results/early_signals.json`# Bootstrapping Through Intermediate Capacities in Weak-to-Strong Generalization

## Summary

This research tests the key bootstrapping claim from weak-to-strong generalization: whether staged supervision (weak→medium→strong) outperforms direct supervision (weak→strong) across different capability gaps. Using a synthetic classification task with controllable model capabilities and systematic error patterns, we find **bootstrapping consistently wins across all tested configurations**, with accuracy advantages ranging from 2.4% to 10.8% (average 6.4%).

## Research Question

When does staged weak→medium→strong supervision beat direct weak→strong supervision? What are the failure modes and early warning signals?

## Methodology

**Synthetic Setup**: 10-class classification task with three "models" (weak, medium, strong) having different base accuracies and systematic error patterns. Models make controlled mistakes: weak models have high systematic error rates on specific class pairs (0→1, 2→3, 4→5), medium models fewer, strong models minimal.

**Experimental Design**:
- 7 capability gap configurations tested
- 5 trials per configuration for robustness
- Direct supervision: weak model labels → strong model training
- Bootstrap supervision: weak labels → medium training → medium labels → strong training
- Measured: accuracy improvement, error pattern overlap, supervision quality

**Key Innovation**: Models can either ELICIT latent capability or IMITATE supervisor errors based on supervision strength and error pattern adoption rates.

## Key Findings

### 1. Bootstrapping Always Wins
- **7/7 configurations show positive bootstrap advantage**
- Range: +2.4% to +10.8% accuracy improvement
- Average advantage: +6.4%
- No failure cases observed in tested parameter range

### 2. Error Pattern Breaking is the Core Mechanism
- Direct supervision: 29.9% error overlap with weak supervisor
- Bootstrap supervision: 21.9% error overlap
- **8.0% average reduction in error overlap**
- Staged supervision dilutes rather than compounds systematic errors

### 3. Intermediate Supervisor Quality Drives Success
- Weak supervisor accuracy: 29.6%
- Medium supervisor accuracy: 42.1% (+12.5% improvement)
- Even weak→medium supervision improves supervisor quality significantly

### 4. Predictable from Early Signals
- **Strongest predictor**: Lower weak accuracy → higher bootstrap advantage (r=-0.789)
- Also predictive: weak supervisor accuracy (r=-0.769), capability gap size (r=0.705)
- **Practical insight**: Bootstrapping most valuable when weak supervisor is very poor

## Gap Regime Analysis

| Weak→Medium→Strong | Bootstrap Advantage | Pattern |
|-------------------|--------------------|---------|
| 0.3→0.5→0.7       | 4.6%               | Small uniform gaps |
| 0.3→0.6→0.9       | 7.3%               | Medium gaps |
| 0.2→0.5→0.9       | 8.3%               | Large weak-strong gap |
| 0.2→0.7→0.8       | 10.8%              | Large first jump, small second |
| 0.5→0.6→0.9       | 2.4%               | Small first jump, large second |

**Pattern**: Bootstrapping advantage increases when (1) weak model is very poor, (2) total capability gap is large, (3) first jump (weak→medium) is substantial.

## Limitations and Caveats

- **Synthetic only**: May not generalize to real LLM training dynamics
- **No failure cases**: Parameter range may be too narrow to find bootstrap failure modes
- **Simplified error model**: Real systematic errors likely more complex
- **Small scale**: Only 7 configurations, 5 trials each
- **Goodhart risk**: Optimizing for accuracy may miss other important failure modes

## Implications for Superalignment

**Positive**: Staged supervision shows promise as a more robust approach than direct weak-to-strong supervision. The error pattern dilution mechanism suggests bootstrapping could reduce harmful imitation behaviors.

**Critical gaps**: Need to identify failure modes and test on realistic tasks. Real superalignment may face different tradeoffs (e.g., deception, goal misgeneralization) not captured in synthetic accuracy metrics.

**Next steps**: Test bootstrapping on larger models, identify failure regimes, investigate whether results hold for safety-relevant capabilities vs. just accuracy.

## Evidence Summary

All claims supported by controlled experiments with measurable outcomes:
- Experiment design: `code/w2s_bootstrap_experiment.py`
- Raw results: `results/experiment_results.json` (7 configurations × 5 trials)
- Statistical analysis: `results/detailed_analysis.json`
- Pattern identification: `results/early_signals.json`