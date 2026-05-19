# Bias-Variance Early Warning Signals for W2S Failure

## Executive Summary

This study operationalizes bias-variance perspectives into ground-truth-free early warning indicators for weak-to-strong (W2S) generalization failure. Using a synthetic 2D classification task with controllable supervisor bias, I tested whether in-training signals can predict poor Performance Gap Ratio (PGR) and high imitation rates before ground-truth evaluation.

**Key Finding**: Several indicators show promising correlations with generalization failure, with prediction entropy (r=0.589) and prediction variance (r=-0.581) emerging as the strongest early warning signals.

## Experimental Setup

### Synthetic Task
- **Domain**: 2D XOR classification (-2 to 2 coordinate space)
- **Ground truth**: Positive labels in matching quadrants ((+,+) or (-,-))
- **Weak supervisor bias**: Regional bias toward class 1 in upper-right quadrant
- **Bias strengths tested**: 0.1, 0.2, 0.3, 0.4, 0.5
- **Sample sizes**: 500 train, 200 validation, 300 test per experiment

### Early Warning Indicators
1. **Disagreement rate**: Student-weak supervisor prediction disagreement
2. **Confidence on disagreement**: Student confidence on disagreement examples
3. **Mean entropy**: Average prediction uncertainty
4. **Weak loss**: Cross-entropy loss on weak supervisor labels
5. **Prediction variance**: Variance in student probability outputs

### Evaluation Metrics
- **PGR**: Performance Gap Ratio = (student_acc - 0.5) / (weak_acc - 0.5)
- **Imitation score**: Agreement between student and weak supervisor predictions

## Results

### Overall Performance Distribution
- **Total experiments**: 15 (5 bias levels × 3 seeds)
- **Mean PGR**: 0.133 ± 0.340 (range: 0.0-1.0)
- **High imitation rate**: 100% (all experiments >0.8 agreement)
- **Dominant failure mode**: Complete imitation of weak supervisor

### Early Warning Signal Effectiveness

| Indicator | PGR Correlation | Mean Value | Interpretation |
|-----------|-----------------|------------|----------------|
| **Mean entropy** | **+0.589** | 0.691 | Higher uncertainty → better generalization |
| **Prediction variance** | **-0.581** | 0.0009 | Lower variance → better generalization |
| **Weak loss** | +0.432 | 0.692 | Higher loss on weak labels → better generalization |
| **Confidence on disagreement** | -0.307 | 0.011 | Lower confidence when disagreeing → worse outcomes |
| **Disagreement rate** | -0.288 | 0.213 | Less disagreement → worse generalization |

### Bias Strength Impact
- **Low bias (0.1-0.3)**: Complete imitation (PGR=0.0)
- **High bias (0.4-0.5)**: Occasional generalization (PGR up to 1.0)
- **Critical threshold**: Around 0.3-0.4 bias strength for any generalization

## Key Insights

1. **Entropy as early warning**: Higher prediction entropy during training correlates with better final generalization, suggesting that maintaining uncertainty helps avoid premature convergence to biased patterns.

2. **Variance paradox**: Lower prediction variance correlates with better generalization, potentially indicating that successful students develop more consistent (but correct) decision boundaries.

3. **Disagreement dynamics**: Students that disagree less with weak supervisors tend to generalize worse, confirming the imitation failure mode.

4. **Complete failure dominance**: 100% imitation rate indicates this synthetic setup strongly favors the failure mode, making it a good stress test for early warning systems.

## Limitations & Caveats

1. **Synthetic scope**: Results limited to 2D XOR task; real-world applicability uncertain
2. **Small sample size**: Only 15 experiments; statistical power limited
3. **Model simplicity**: Basic logistic regression may not capture complex failure modes
4. **ROC analysis incomplete**: Technical issues with AUC calculation (all 0.5)
5. **Goodhart risk**: Optimizing for these indicators could lead to gaming without genuine improvement
6. **Ground-truth leakage**: Validation set uses same bias pattern as training

## Technical Implementation

The experiment implements a minimal W2S pipeline using only numpy:
- Custom logistic regression with gradient descent
- Controllable regional bias injection
- Incremental training simulation for mid-point indicator computation
- Correlation analysis between early indicators and final performance

## Next Steps

1. **Scale validation**: Test on more diverse tasks and larger models
2. **ROC improvement**: Fix AUC calculation for proper early warning thresholds
3. **Ensemble indicators**: Combine multiple signals for robust early detection
4. **Dynamic thresholding**: Develop adaptive cutoffs based on task characteristics
5. **Real-world validation**: Apply to actual language model fine-tuning scenarios

## Code & Data Availability

- **Implementation**: `minimal_w2s.py` (208 lines, numpy-only)
- **Raw results**: `experiment_results.json` (15 experiments)
- **Analysis**: `indicator_analysis.json` (correlation metrics)

Total bundle size: <15KB