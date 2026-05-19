"""
Minimal Weak-to-Strong Generalization Experiment
Using only numpy - implements basic logistic regression from scratch
"""

import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

class SimpleLogisticRegression:
    """Basic logistic regression implementation."""

    def __init__(self, learning_rate=0.01, max_iter=1000, random_state=42):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.rng = np.random.RandomState(random_state)
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        """Sigmoid activation function."""
        z = np.clip(z, -500, 500)  # Prevent overflow
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        """Train the model."""
        n_samples, n_features = X.shape

        # Initialize weights
        self.weights = self.rng.normal(0, 0.01, n_features)
        self.bias = 0.0

        # Gradient descent
        for _ in range(self.max_iter):
            # Forward pass
            z = X.dot(self.weights) + self.bias
            predictions = self.sigmoid(z)

            # Compute gradients
            dw = (1/n_samples) * X.T.dot(predictions - y)
            db = (1/n_samples) * np.sum(predictions - y)

            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_proba(self, X):
        """Predict probabilities."""
        z = X.dot(self.weights) + self.bias
        prob_1 = self.sigmoid(z)
        prob_0 = 1 - prob_1
        return np.column_stack([prob_0, prob_1])

    def predict(self, X):
        """Make predictions."""
        return (self.predict_proba(X)[:, 1] > 0.5).astype(int)

def generate_xor_data(n_samples=1000, seed=42):
    """Generate synthetic XOR data."""
    rng = np.random.RandomState(seed)
    X = rng.uniform(-2, 2, size=(n_samples, 2))
    y = ((X[:, 0] > 0) & (X[:, 1] > 0)) | ((X[:, 0] < 0) & (X[:, 1] < 0))

    # Add small amount of noise
    noise_mask = rng.random(n_samples) < 0.05
    y[noise_mask] = ~y[noise_mask]

    return X, y.astype(int)

def apply_regional_bias(X, y_true, bias_strength=0.3, seed=42):
    """Apply systematic bias to labels in upper-right quadrant."""
    rng = np.random.RandomState(seed)
    y_biased = y_true.copy()

    # Bias toward class 1 in upper-right quadrant
    bias_region = (X[:, 0] > 0) & (X[:, 1] > 0)
    flip_mask = bias_region & (rng.random(len(X)) < bias_strength)
    y_biased[flip_mask] = 1

    return y_biased

def accuracy_score(y_true, y_pred):
    """Calculate accuracy."""
    return np.mean(y_true == y_pred)

def log_loss(y_true, y_prob):
    """Calculate log loss."""
    eps = 1e-15
    y_prob = np.clip(y_prob, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_prob) + (1 - y_true) * np.log(1 - y_prob))

def compute_early_indicators(student_model, weak_model, X_val, y_val_weak):
    """Compute early warning indicators."""
    student_proba = student_model.predict_proba(X_val)[:, 1]
    student_pred = student_model.predict(X_val)
    weak_pred = weak_model.predict(X_val)

    indicators = {}

    # 1. Student-weak disagreement rate
    indicators['disagreement_rate'] = np.mean(student_pred != weak_pred)

    # 2. Student confidence on disagreement examples
    disagree_mask = student_pred != weak_pred
    if np.sum(disagree_mask) > 0:
        # Distance from 0.5 (confidence)
        confidence_scores = np.abs(student_proba[disagree_mask] - 0.5)
        indicators['confidence_on_disagreement'] = np.mean(confidence_scores)
    else:
        indicators['confidence_on_disagreement'] = 0.0

    # 3. Prediction entropy (uncertainty)
    eps = 1e-7
    p_safe = np.clip(student_proba, eps, 1 - eps)
    entropy = -p_safe * np.log(p_safe) - (1 - p_safe) * np.log(1 - p_safe)
    indicators['mean_entropy'] = np.mean(entropy)

    # 4. Loss on weak supervisor labels
    indicators['weak_loss'] = log_loss(y_val_weak, student_proba)

    # 5. Variance in predictions
    indicators['prediction_variance'] = np.var(student_proba)

    return indicators

def simple_roc_auc(y_true, y_scores):
    """Simple ROC AUC calculation."""
    # Sort by scores
    desc_score_indices = np.argsort(y_scores)[::-1]
    y_scores = y_scores[desc_score_indices]
    y_true = y_true[desc_score_indices]

    # Calculate thresholds
    thresholds = np.concatenate([[np.inf], y_scores])

    tps = np.concatenate([[0], np.cumsum(y_true)])
    fps = np.arange(len(y_true) + 1) - tps

    # Calculate TPR and FPR
    tpr = tps / np.sum(y_true) if np.sum(y_true) > 0 else np.zeros_like(tps)
    fpr = fps / np.sum(1 - y_true) if np.sum(1 - y_true) > 0 else np.zeros_like(fps)

    # Calculate AUC using trapezoidal rule
    auc = np.trapz(tpr, fpr)
    return auc

def run_w2s_experiment():
    """Run the weak-to-strong generalization experiment."""
    print("Starting Weak-to-Strong Generalization Experiment")
    print("=" * 50)

    results = []
    bias_levels = [0.1, 0.2, 0.3, 0.4, 0.5]
    n_seeds = 3

    for bias_strength in bias_levels:
        print(f"Testing bias strength: {bias_strength}")

        bias_results = []

        for seed in range(n_seeds):
            # Generate datasets
            X_train, y_train_true = generate_xor_data(500, seed=seed)
            X_val, y_val_true = generate_xor_data(200, seed=seed+100)
            X_test, y_test_true = generate_xor_data(300, seed=seed+200)

            # Apply bias to get weak supervision
            y_train_weak = apply_regional_bias(X_train, y_train_true, bias_strength, seed=seed)
            y_val_weak = apply_regional_bias(X_val, y_val_true, bias_strength, seed=seed+100)

            # Train weak supervisor (learns from biased data)
            weak_model = SimpleLogisticRegression(
                learning_rate=0.1, max_iter=500, random_state=seed
            )
            weak_model.fit(X_train, y_train_weak)

            # Train student model incrementally to track indicators
            student_model = SimpleLogisticRegression(
                learning_rate=0.1, max_iter=300, random_state=seed+1000
            )

            # Partial training (60% of data) for early indicators
            n_partial = int(0.6 * len(X_train))
            student_model.fit(X_train[:n_partial], y_train_weak[:n_partial])

            # Compute early warning indicators
            indicators = compute_early_indicators(student_model, weak_model, X_val, y_val_weak)

            # Complete training
            student_model.fit(X_train, y_train_weak)

            # Final evaluation on test set
            student_test_pred = student_model.predict(X_test)
            weak_test_pred = weak_model.predict(X_test)

            student_accuracy = accuracy_score(y_test_true, student_test_pred)
            weak_accuracy = accuracy_score(y_test_true, weak_test_pred)

            # Performance Gap Ratio (PGR)
            random_baseline = 0.5
            if weak_accuracy > random_baseline:
                pgr = (student_accuracy - random_baseline) / (weak_accuracy - random_baseline)
            else:
                pgr = 0.0

            # Imitation score (how much student mimics weak supervisor)
            imitation_score = accuracy_score(weak_test_pred, student_test_pred)

            result = {
                'bias_strength': bias_strength,
                'seed': seed,
                'student_accuracy': float(student_accuracy),
                'weak_accuracy': float(weak_accuracy),
                'pgr': float(pgr),
                'imitation_score': float(imitation_score),
                'indicators': {k: float(v) for k, v in indicators.items()}
            }

            bias_results.append(result)
            results.append(result)

        # Summary for this bias level
        pgr_values = [r['pgr'] for r in bias_results]
        imitation_values = [r['imitation_score'] for r in bias_results]
        print(f"  Mean PGR: {np.mean(pgr_values):.3f} ± {np.std(pgr_values):.3f}")
        print(f"  Mean Imitation: {np.mean(imitation_values):.3f} ± {np.std(imitation_values):.3f}")

    return results

def analyze_indicators(results):
    """Analyze the effectiveness of early warning indicators."""
    print("\nAnalyzing early warning indicators...")

    # Extract performance metrics and indicators
    pgr_values = np.array([r['pgr'] for r in results])
    imitation_values = np.array([r['imitation_score'] for r in results])

    # Get all indicator values
    indicator_names = list(results[0]['indicators'].keys())
    indicator_data = {}

    for indicator in indicator_names:
        indicator_data[indicator] = np.array([r['indicators'][indicator] for r in results])

    analysis_results = {
        'total_experiments': len(results),
        'performance_summary': {
            'pgr_mean': float(np.mean(pgr_values)),
            'pgr_std': float(np.std(pgr_values)),
            'pgr_min': float(np.min(pgr_values)),
            'pgr_max': float(np.max(pgr_values)),
            'imitation_mean': float(np.mean(imitation_values)),
            'imitation_std': float(np.std(imitation_values)),
            'high_imitation_rate': float(np.mean(imitation_values > 0.8))
        },
        'indicator_analysis': {}
    }

    # Analyze each indicator
    pgr_median = np.median(pgr_values)
    low_pgr_mask = pgr_values < pgr_median

    for indicator_name in indicator_names:
        indicator_vals = indicator_data[indicator_name]

        # Remove any NaN values
        valid_mask = ~np.isnan(indicator_vals) & ~np.isnan(pgr_values) & ~np.isnan(imitation_values)

        if np.sum(valid_mask) < 5:  # Need at least 5 valid points
            continue

        valid_indicator = indicator_vals[valid_mask]
        valid_pgr = pgr_values[valid_mask]
        valid_imitation = imitation_values[valid_mask]
        valid_low_pgr = low_pgr_mask[valid_mask]

        # Correlations
        corr_pgr = np.corrcoef(valid_indicator, valid_pgr)[0, 1]
        corr_imitation = np.corrcoef(valid_indicator, valid_imitation)[0, 1]

        # ROC AUC for predicting low PGR
        if len(np.unique(valid_low_pgr)) == 2:  # Need both classes
            auc_positive = simple_roc_auc(valid_low_pgr, valid_indicator)
            auc_negative = simple_roc_auc(valid_low_pgr, -valid_indicator)
            best_auc = max(auc_positive, auc_negative)
            direction = 'positive' if auc_positive > auc_negative else 'negative'
        else:
            best_auc = 0.5
            direction = 'none'

        analysis_results['indicator_analysis'][indicator_name] = {
            'correlation_with_pgr': float(corr_pgr),
            'correlation_with_imitation': float(corr_imitation),
            'auc_for_low_pgr_prediction': float(best_auc),
            'prediction_direction': direction,
            'mean_value': float(np.mean(valid_indicator)),
            'std_value': float(np.std(valid_indicator))
        }

    return analysis_results

def main():
    """Main experimental pipeline."""
    # Run the experiment
    results = run_w2s_experiment()

    # Analyze indicators
    analysis = analyze_indicators(results)

    # Save results
    with open('/home/user/fab_out/artifact/results/experiment_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    with open('/home/user/fab_out/artifact/results/indicator_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)

    # Print summary
    print("\n" + "="*50)
    print("EXPERIMENT SUMMARY")
    print("="*50)

    print(f"Total experiments: {analysis['total_experiments']}")
    print(f"Mean PGR: {analysis['performance_summary']['pgr_mean']:.3f}")
    print(f"PGR range: [{analysis['performance_summary']['pgr_min']:.3f}, {analysis['performance_summary']['pgr_max']:.3f}]")
    print(f"High imitation rate (>0.8): {analysis['performance_summary']['high_imitation_rate']:.1%}")

    print("\nBEST EARLY WARNING INDICATORS:")

    # Sort indicators by AUC for predicting low PGR
    sorted_indicators = sorted(
        analysis['indicator_analysis'].items(),
        key=lambda x: x[1]['auc_for_low_pgr_prediction'],
        reverse=True
    )

    for name, stats in sorted_indicators:
        print(f"  {name}:")
        print(f"    AUC (low PGR prediction): {stats['auc_for_low_pgr_prediction']:.3f}")
        print(f"    Correlation with PGR: {stats['correlation_with_pgr']:.3f}")
        print(f"    Correlation with imitation: {stats['correlation_with_imitation']:.3f}")

    print(f"\nResults saved to /home/user/fab_out/artifact/results/")

    return analysis

if __name__ == "__main__":
    main()