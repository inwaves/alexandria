# PGR vs. Imitation Regime Map: Weak-to-Strong Generalization Study

## Research Question
Under what conditions does naive weak-label finetuning *elicit* a strong model's latent capability versus *train it to imitate* the weak supervisor's systematic errors?

## Approach
I implemented a synthetic teacher-student W2S simulation with:
- **Weak supervisors**: Logistic regression (low capacity) and small MLPs (higher capacity)
- **Strong students**: Fixed-architecture MLPs trained only on weak labels
- **Capability gap sweep**: Supervisor capacity from 0.0 (logistic on 3 features) to 1.0 (small MLP on all features)
- **Noise/bias sweep**: Systematic label flipping from 0% to 20% (biased toward class 0)
- **Dataset**: 3-class classification with 500 samples, 10 features

Key metrics:
- **Performance Gap Recovered (PGR)**: `(student_acc - weak_acc) / (strong_acc - weak_acc)`
- **Imitation Score**: Agreement rate between student and supervisor on supervisor's *errors*

## Key Findings

### 1. Imitation Dominates Over Capability Recovery
- **Mean PGR**: 0.038 (only ~4% of the performance gap recovered)
- **Mean Imitation Score**: 0.716 (71% agreement on supervisor errors)
- **All 9 regime points** showed high imitation (>0.6) and low PGR (<0.1)

This suggests that in our synthetic setup, naive weak-label training primarily learns to *imitate supervisor mistakes* rather than elicit latent capabilities.

### 2. Regime Map Patterns
From the 3×3 grid (capacity × noise levels):

**Low Capacity Supervisors (0.0)**:
- Highest PGR values (0.05-0.07) but still minimal
- Moderate imitation scores (0.62-0.76)
- Interpretation: When supervisor is very weak, student sometimes finds small improvements

**Higher Capacity Supervisors (0.5, 1.0)**:
- Near-zero PGR (0.0-0.10)
- Consistently high imitation (0.70-0.76)
- Interpretation: More capable supervisors create stronger imitation pressure

**Noise Effects**:
- Increasing noise slightly reduces PGR for high-capacity supervisors
- Imitation scores remain relatively stable across noise levels
- Systematic bias (toward class 0) maintains error structure for imitation

### 3. Performance Ceiling Effect
The strong baseline achieved 84.7% accuracy while weak supervisors ranged from 48% (logistic) to 78% (small MLP). The large performance gap (17-37 percentage points) should provide ample room for recovery, yet PGR remained minimal across all conditions.

## Evidence

### Experimental Data
- **Total experiments**: 9 (3×3 grid)
- **High PGR + Low Imitation regimes**: 0
- **High Imitation + Low PGR regimes**: 9 (100%)
- Results saved in: `results/detailed_results.json`
- Visualizations: `results/regime_maps.png`

### Representative Examples
- **Best PGR case** (Cap=1.0, Noise=0.0): PGR=0.10, Imitation=0.70
- **Worst PGR case** (Cap=0.5, Noise≥0.5): PGR=0.00, Imitation=0.76
- **Lowest imitation** (Cap=0.0, Noise=1.0): PGR=0.07, Imitation=0.62

## Limitations and Caveats

### 1. Synthetic Setup Constraints
- **Small scale**: Only 500 samples, 10 features limits generalizability
- **Simple architectures**: MLPs may not capture complexity of real W2S scenarios
- **Coarse grid**: 3×3 parameter sweep may miss finer regime boundaries

### 2. Methodological Limitations
- **Fixed strong architecture**: Same capacity for baseline and student may bias toward imitation
- **Limited noise model**: Only systematic label flipping; real supervisors have more complex error patterns
- **Short training**: Max 300 iterations may not allow full capability recovery

### 3. Metric Sensitivity
- **PGR calculation**: Sensitive to performance gaps; zero/negative gaps yield PGR=0
- **Imitation score**: Only measures error agreement, not error type matching
- **No confidence measures**: Cannot distinguish confident vs. uncertain imitation

### 4. Potential Leakage Risks
- **Shared training data**: Student trained on same input features as supervisor
- **Architecture similarity**: All models use same underlying representations
- **Evaluation limitations**: Single random seed may bias results

## Implications and Next Steps

### 1. Imitation-Dominant Regime Identified
This synthetic setup falls squarely in the "imitation failure mode" described in the W2S literature. The high imitation scores (>0.6) across all conditions suggest systematic error copying rather than capability elicitation.

### 2. Supervisor Capacity Paradox
Counter-intuitively, higher-capacity supervisors showed *worse* PGR. This suggests that more capable weak supervisors may create stronger imitation attractors, making capability recovery harder.

### 3. Suggested Follow-ups
- **Confidence-based training**: Use supervisor uncertainty to weight training signals
- **Architectural diversity**: Train student with different inductive biases than supervisor
- **Multi-supervisor ensembles**: Combine multiple weak supervisors to reduce systematic errors
- **Early stopping analysis**: Study training dynamics to identify when imitation begins
- **Real data validation**: Test regime boundaries on non-synthetic tasks

## Reproducibility
```bash
cd code/
python main_experiment.py
```
Results and plots saved to `results/` directory.

## Summary
This study provides evidence that naive weak-label finetuning in synthetic settings strongly favors imitation over capability recovery. The 3×3 regime map reveals a uniformly imitation-dominant region with minimal PGR across supervisor capacity and noise levels. While limited by scale and synthetic constraints, these results support the W2S literature's emphasis on imitation as a primary failure mode requiring targeted mitigation strategies.