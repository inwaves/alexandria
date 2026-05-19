# Goodhart's Law in Automated Weak-to-Strong Research: Held-out Leakage Audit

## Summary

This study demonstrates how repeated submission to held-out validation inflates apparent progress in automated weak-to-strong (W2S) generalization research. Through synthetic experiments, we quantify the **optimism bias** that emerges when automated researchers iteratively query held-out sets, and propose concrete protocols to bound this leakage.

## Core Finding: The Goodhart Caveat

When an automated W2S researcher repeatedly submits method variants to a held-out validation set, **apparent progress diverges from true generalization**. In our main experiment:

- **Apparent improvement**: +1.2% (held-out score: 0.776 → 0.788)
- **Actual improvement**: -0.8% (test score: 0.728 → 0.720)
- **Optimism bias**: +2.0 percentage points
- **Bias ratio**: 167% (bias exceeds apparent improvement)

The automated researcher appeared to make meaningful progress while actually degrading true performance—a textbook example of Goodhart's law where "a measure ceases to be a good measure when it becomes a target."

## Mechanism: Selection Pressure on Finite Data

The bias emerges from **selection pressure** applied to a finite held-out set. Each submission round:

1. Generates multiple method variants (hyperparameter perturbations)
2. Evaluates all variants on the same held-out split
3. Selects the highest-scoring variant
4. Iterates, using the selected method as a new baseline

Over 50 iterations with 15 methods per iteration (750 total held-out evaluations), random fluctuations in held-out scores get systematically selected, inflating apparent performance while test performance stagnates or degrades.

## Quantifying Bias vs. Submission Budget

Testing different submission budgets reveals how bias scales:

| Budget | Optimism Bias | Bias Ratio |
|--------|---------------|------------|
| 5      | +0.0%         | 0%         |
| 10     | +0.0%         | 0%         |
| 20     | +0.0%         | 0%         |
| 50     | +1.0%         | 300%       |
| 100    | +0.3%         | 100%       |

Bias emerges sharply around 50 submissions and plateaus, suggesting a critical threshold where selection pressure overwhelms true signal.

## How This Looks From Inside Fab

From an automated researcher's perspective:
- Held-out scores show consistent upward trend
- Method variants appear to be learning from weak supervision
- Progress metrics suggest successful W2S elicitation
- **But test performance reveals the truth: no genuine improvement**

This creates a dangerous feedback loop where apparent success drives continued optimization on a corrupted signal.

## Proposed Mitigation Protocols

### 1. Submission Budget Limits
- **Recommended limit**: 50 submissions per held-out set
- **Rationale**: Bias threshold observed at this level
- **Implementation**: Hard cap on held-out evaluations

### 2. Held-out Rotation
- **Recommended**: 3 fresh held-out splits, ~17 submissions each
- **Rationale**: Prevents prolonged exposure to any single split
- **Implementation**: Cycle through disjoint validation sets

### 3. Early Stopping with Patience
- **Recommended patience**: 5 rounds without improvement
- **Minimum improvement**: 0.1% to continue
- **Rationale**: Stops optimization when diminishing returns suggest overfitting

### 4. Bias-Corrected Confidence Intervals
- **Method**: Bootstrap resampling of held-out set
- **Purpose**: Estimate and subtract expected optimism bias
- **Implementation**: Report bias-corrected performance bounds

## Limitations and Shortcuts

1. **Synthetic task**: Real W2S tasks may show different bias patterns
2. **Simple methods**: More complex methods might exhibit different leakage
3. **Fixed data splits**: Dynamic splitting could change bias characteristics
4. **Noise model**: Gaussian noise may not reflect real method uncertainty
5. **Single metric**: Multi-objective optimization could compound bias

## Key Implications

This study reveals a fundamental tension in automated AI safety research: the same held-out validation that prevents overfitting becomes a source of bias under selection pressure. **Automated researchers need explicit protocols to prevent held-out leakage**, especially when iterating many method variants.

The results suggest that automated W2S research—while promising for scalable safety—requires careful experimental design to avoid spurious progress signals that could mislead safety evaluations.

## Next Steps

1. **Scale validation**: Test on real W2S benchmarks and larger models
2. **Method diversity**: Evaluate bias across different W2S approaches
3. **Dynamic protocols**: Develop adaptive submission budgets based on bias estimation
4. **Meta-learning**: Train automated researchers to detect their own overfitting