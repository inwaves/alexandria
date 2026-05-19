"""
Simple Weak-to-Strong Generalization Experiment
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score
import json
import warnings
warnings.filterwarnings('ignore')

def generate_xor_data(n_samples=1000, seed=42):
    """Generate synthetic XOR data."""
    rng = np.random.RandomState(seed)
    X = rng.uniform(-2, 2, size=(n_samples, 2))
    y = ((X[:, 0] > 0) & (X[:, 1] > 0)) | ((X[:, 0] < 0) & (X[:, 1] < 0))
    return X, y.astype(int)

def apply_bias(X, y_true, bias_strength=0.3, seed=42):
    """Apply regional bias to labels."""
    rng = np.random.RandomState(seed)
    y_biased = y_true.copy()

    # Bias toward class 1 in upper-right quadrant
    bias_mask = (X[:, 0] > 0) & (X[:, 1] > 0)
    flip_indices = bias_mask & (rng.random(len(X)) < bias_strength)
    y_biased[flip_indices] = 1

    return y_biased

def compute_indicators(student_model, weak_model, X_val, y_val_weak):
    """Compute early warning indicators."""
    student_proba = student_model.predict_proba(X_val)[:, 1]
    student_pred = (student_proba > 0.5).astype(int)
    weak_pred = weak_model.predict(X_val)

    indicators = {}

    # Disagreement rate
    indicators['disagreement_rate'] = np.mean(student_pred != weak_pred)

    # Confidence on disagreements
    disagree_mask = student_pred != weak_pred
    if np.sum(disagree_mask) > 0:
        indicators['confidence_on_disagreement'] = np.mean(
            np.abs(student_proba[disagree_mask] - 0.5)
        )
    else:
        indicators['confidence_on_disagreement'] = 0.0

    # Prediction entropy
    eps = 1e-7
    p = np.clip(student_proba, eps, 1-eps)
    entropy = -p * np.log(p) - (1-p) * np.log(1-p)
    indicators['mean_entropy'] = np.mean(entropy)

    # Loss on weak labels
    indicators['weak_loss'] = log_loss(y_val_weak, student_proba)

    return indicators

def run_experiment():
    """Run the main experiment."""
    print("Running W2S experiment...")

    results = []
    bias_levels = [0.1, 0.2, 0.3, 0.4, 0.5]

    for bias in bias_levels:
        print(f"Testing bias strength: {bias}")

        for seed in range(3):  # 3 seeds per bias level
            # Generate data
            X_train, y_train_true = generate_xor_data(800, seed=seed)
            X_val, y_val_true = generate_xor_data(200, seed=seed+100)
            X_test, y_test_true = generate_xor_data(500, seed=seed+200)

            # Apply bias
            y_train_weak = apply_bias(X_train, y_train_true, bias, seed=seed)
            y_val_weak = apply_bias(X_val, y_val_true, bias, seed=seed+100)

            # Train weak supervisor
            weak_model = LogisticRegression(random_state=seed, max_iter=1000)
            weak_model.fit(X_train, y_train_weak)

            # Train student incrementally
            student_model = LogisticRegression(random_state=seed, max_iter=1000)

            # Train on 60% of data to compute mid-training indicators
            n_mid = int(0.6 * len(X_train))
            student_model.fit(X_train[:n_mid], y_train_weak[:n_mid])

            # Compute indicators at mid-training
            indicators = compute_indicators(student_model, weak_model, X_val, y_val_weak)

            # Full training
            student_model.fit(X_train, y_train_weak)

            # Final evaluation
            student_pred_test = student_model.predict(X_test)
            weak_pred_test = weak_model.predict(X_test)

            student_acc = accuracy_score(y_test_true, student_pred_test)
            weak_acc = accuracy_score(y_test_true, weak_pred_test)

            # PGR calculation
            random_acc = 0.5
            pgr = (student_acc - random_acc) / (weak_acc - random_acc) if weak_acc > random_acc else 0

            # Imitation score
            imitation_score = accuracy_score(weak_pred_test, student_pred_test)

            result = {
                'bias_strength': bias,
                'seed': seed,
                'student_accuracy': student_acc,
                'weak_accuracy': weak_acc,
                'pgr': pgr,
                'imitation_score': imitation_score,
                'indicators': indicators
            }

            results.append(result)

        print(f"  Completed bias level {bias}")

    return results

def analyze_results(results):
    """Analyze correlation between indicators and performance."""

    # Extract data
    pgr_values = [r['pgr'] for r in results]
    imitation_values = [r['imitation_score'] for r in results]

    indicator_names = list(results[0]['indicators'].keys())
    correlations = {}

    for indicator in indicator_names:
        indicator_values = [r['indicators'][indicator] for r in results]

        # Correlation with PGR
        corr_pgr = np.corrcoef(indicator_values, pgr_values)[0, 1]

        # Correlation with imitation
        corr_imitation = np.corrcoef(indicator_values, imitation_values)[0, 1]

        # ROC for predicting low PGR
        pgr_threshold = np.median(pgr_values)
        low_pgr = np.array(pgr_values) < pgr_threshold

        try:
            auc = max(
                roc_auc_score(low_pgr, indicator_values),
                roc_auc_score(low_pgr, [-x for x in indicator_values])
            )
        except:
            auc = 0.5

        correlations[indicator] = {
            'correlation_with_pgr': corr_pgr,
            'correlation_with_imitation': corr_imitation,
            'auc_low_pgr_prediction': auc
        }

    analysis = {
        'total_experiments': len(results),
        'pgr_statistics': {
            'mean': np.mean(pgr_values),
            'std': np.std(pgr_values),
            'min': np.min(pgr_values),
            'max': np.max(pgr_values)
        },
        'imitation_statistics': {
            'mean': np.mean(imitation_values),
            'std': np.std(imitation_values),
            'high_imitation_rate': np.mean(np.array(imitation_values) > 0.8)
        },
        'indicator_correlations': correlations
    }

    return analysis

def main():
    """Main function."""
    results = run_experiment()
    analysis = analyze_results(results)

    # Save results
    with open('/home/user/fab_out/artifact/results/simple_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    with open('/home/user/fab_out/artifact/results/simple_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2, default=str)

    print("\nResults Summary:")
    print(f"Total experiments: {analysis['total_experiments']}")
    print(f"Mean PGR: {analysis['pgr_statistics']['mean']:.3f}")
    print(f"High imitation rate: {analysis['imitation_statistics']['high_imitation_rate']:.1%}")

    print("\nBest indicators for predicting low PGR:")
    correlations = analysis['indicator_correlations']
    sorted_indicators = sorted(correlations.items(),
                              key=lambda x: x[1]['auc_low_pgr_prediction'],
                              reverse=True)

    for name, stats in sorted_indicators:
        print(f"  {name}: AUC={stats['auc_low_pgr_prediction']:.3f}, "
              f"PGR_corr={stats['correlation_with_pgr']:.3f}")

    return analysis

if __name__ == "__main__":
    main()