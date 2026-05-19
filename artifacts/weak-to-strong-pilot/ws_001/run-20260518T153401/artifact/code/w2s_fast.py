#!/usr/bin/env python3
"""
Fast Weak-to-Strong Generalization: PGR vs Imitation Regime Map

Simplified version for quick execution.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json
import os
import warnings
warnings.filterwarnings('ignore')


def generate_synthetic_data(n_samples=2000, n_features=15, n_classes=3, random_state=42):
    """Generate synthetic classification dataset."""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_features//2,
        n_redundant=n_features//4,
        n_classes=n_classes,
        class_sep=1.2,
        random_state=random_state
    )
    return X, y


def create_weak_supervisor(capacity_level, noise_level, X_train, y_train, random_state=42):
    """Create weak supervisor with specified capacity and noise."""

    if capacity_level < 0.5:
        # Low capacity: Logistic regression with limited features
        n_features_used = max(3, int(X_train.shape[1] * (0.2 + capacity_level)))
        feature_indices = np.random.RandomState(random_state).choice(
            X_train.shape[1], n_features_used, replace=False
        )

        model = LogisticRegression(random_state=random_state, max_iter=200)
        model.fit(X_train[:, feature_indices], y_train)

        def predict(X):
            return model.predict(X[:, feature_indices])
    else:
        # Higher capacity: Small MLP
        hidden_size = int(5 + capacity_level * 15)
        model = MLPClassifier(
            hidden_layer_sizes=(hidden_size,),
            random_state=random_state,
            max_iter=200
        )
        model.fit(X_train, y_train)
        predict = model.predict

    # Add systematic bias/noise
    def noisy_predict(X):
        clean_pred = predict(X)
        if noise_level > 0:
            # Add systematic label flipping bias
            flip_prob = noise_level * 0.2  # Max 20% flipping
            n_samples = len(clean_pred)
            flip_mask = np.random.RandomState(random_state + 1).random(n_samples) < flip_prob

            noisy_pred = clean_pred.copy()
            # Systematic bias: flip to class 0 more often
            for i in range(n_samples):
                if flip_mask[i]:
                    noisy_pred[i] = 0

            return noisy_pred
        return clean_pred

    return noisy_predict


def create_strong_student(X_train, y_weak_labels, random_state=42):
    """Create strong student (higher capacity MLP) trained only on weak labels."""
    model = MLPClassifier(
        hidden_layer_sizes=(30, 15),
        random_state=random_state,
        max_iter=300
    )
    model.fit(X_train, y_weak_labels)
    return model.predict


def calculate_pgr(weak_acc, strong_acc, student_acc):
    """Calculate Performance Gap Recovered (PGR)."""
    if strong_acc <= weak_acc:
        return 0.0  # No gap to recover
    return max(0.0, (student_acc - weak_acc) / (strong_acc - weak_acc))


def calculate_imitation_score(weak_predictions, student_predictions, y_true):
    """Calculate imitation score: agreement on weak supervisor's errors."""
    weak_errors = (weak_predictions != y_true)
    if not np.any(weak_errors):
        return 0.0  # No errors to imitate

    # Among cases where weak supervisor was wrong, how often does student agree?
    agreement_on_errors = (weak_predictions[weak_errors] == student_predictions[weak_errors])
    return np.mean(agreement_on_errors)


def run_single_experiment(capacity_level, noise_level, X_train, y_train, X_test, y_test, random_state=42):
    """Run a single W2S experiment with given capacity and noise levels."""

    # Create ground truth strong baseline
    strong_baseline = MLPClassifier(
        hidden_layer_sizes=(30, 15),
        random_state=random_state,
        max_iter=300
    )
    strong_baseline.fit(X_train, y_train)
    strong_acc = accuracy_score(y_test, strong_baseline.predict(X_test))

    # Create weak supervisor
    weak_predict = create_weak_supervisor(capacity_level, noise_level, X_train, y_train, random_state)

    # Get weak supervisor's accuracy
    weak_pred_test = weak_predict(X_test)
    weak_acc = accuracy_score(y_test, weak_pred_test)

    # Generate weak labels for training strong student
    weak_labels_train = weak_predict(X_train)

    # Train strong student on weak labels only
    student_predict = create_strong_student(X_train, weak_labels_train, random_state)
    student_pred_test = student_predict(X_test)
    student_acc = accuracy_score(y_test, student_pred_test)

    # Calculate metrics
    pgr = calculate_pgr(weak_acc, strong_acc, student_acc)
    imitation_score = calculate_imitation_score(weak_pred_test, student_pred_test, y_test)

    return {
        'weak_acc': weak_acc,
        'strong_acc': strong_acc,
        'student_acc': student_acc,
        'pgr': pgr,
        'imitation_score': imitation_score
    }


def create_regime_map(n_capacity=5, n_noise=5, random_state=42):
    """Create 2D regime map of PGR vs imitation score."""
    print("Generating synthetic dataset...")
    X, y = generate_synthetic_data(random_state=random_state)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=random_state
    )

    capacity_levels = np.linspace(0.0, 1.0, n_capacity)
    noise_levels = np.linspace(0.0, 1.0, n_noise)

    results = {
        'capacity_levels': capacity_levels,
        'noise_levels': noise_levels,
        'pgr_map': np.zeros((n_noise, n_capacity)),
        'imitation_map': np.zeros((n_noise, n_capacity)),
        'detailed_results': []
    }

    print(f"Running {n_capacity * n_noise} experiments...")

    for i, noise_level in enumerate(noise_levels):
        for j, capacity_level in enumerate(capacity_levels):
            print(f"  Capacity {capacity_level:.2f}, Noise {noise_level:.2f}", flush=True)

            result = run_single_experiment(
                capacity_level, noise_level, X_train, y_train, X_test, y_test,
                random_state=random_state + i * n_capacity + j
            )

            results['pgr_map'][i, j] = result['pgr']
            results['imitation_map'][i, j] = result['imitation_score']
            results['detailed_results'].append({
                'capacity_level': capacity_level,
                'noise_level': noise_level,
                **result
            })

    return results


def plot_regime_maps(results, output_dir):
    """Generate and save regime map visualizations."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # PGR map
    im1 = ax1.imshow(results['pgr_map'], aspect='auto', origin='lower',
                     extent=[0, 1, 0, 1], cmap='viridis')
    ax1.set_xlabel('Capacity Level')
    ax1.set_ylabel('Noise Level')
    ax1.set_title('Performance Gap Recovered (PGR)')
    plt.colorbar(im1, ax=ax1)

    # Imitation score map
    im2 = ax2.imshow(results['imitation_map'], aspect='auto', origin='lower',
                     extent=[0, 1, 0, 1], cmap='plasma')
    ax2.set_xlabel('Capacity Level')
    ax2.set_ylabel('Noise Level')
    ax2.set_title('Imitation Score')
    plt.colorbar(im2, ax=ax2)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'regime_maps.png'), dpi=100, bbox_inches='tight')
    plt.close()

    # Combined analysis plot
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    # Scatter plot of PGR vs Imitation Score, colored by noise level
    pgr_flat = results['pgr_map'].flatten()
    imitation_flat = results['imitation_map'].flatten()

    capacity_grid, noise_grid = np.meshgrid(results['capacity_levels'], results['noise_levels'])
    noise_flat = noise_grid.flatten()

    scatter = ax.scatter(imitation_flat, pgr_flat, c=noise_flat, cmap='coolwarm', alpha=0.7)
    ax.set_xlabel('Imitation Score')
    ax.set_ylabel('Performance Gap Recovered (PGR)')
    ax.set_title('PGR vs Imitation Score (colored by noise level)')
    plt.colorbar(scatter, ax=ax, label='Noise Level')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'pgr_vs_imitation.png'), dpi=100, bbox_inches='tight')
    plt.close()


def main():
    """Main experiment runner."""
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')

    print("Starting Fast Weak-to-Strong Generalization Regime Mapping...")

    # Run the main experiment (small size for speed)
    results = create_regime_map(n_capacity=5, n_noise=5, random_state=42)

    # Save detailed results
    with open(os.path.join(results_dir, 'detailed_results.json'), 'w') as f:
        # Convert numpy arrays to lists for JSON serialization
        json_results = {
            'capacity_levels': results['capacity_levels'].tolist(),
            'noise_levels': results['noise_levels'].tolist(),
            'pgr_map': results['pgr_map'].tolist(),
            'imitation_map': results['imitation_map'].tolist(),
            'detailed_results': results['detailed_results']
        }
        json.dump(json_results, f, indent=2)

    # Generate plots
    plot_regime_maps(results, results_dir)

    # Analysis summary
    pgr_mean = np.mean(results['pgr_map'])
    imitation_mean = np.mean(results['imitation_map'])

    # Find regime boundaries
    high_pgr_low_imitation = np.sum((results['pgr_map'] > 0.5) & (results['imitation_map'] < 0.5))
    high_imitation_low_pgr = np.sum((results['imitation_map'] > 0.5) & (results['pgr_map'] < 0.5))

    summary = {
        'total_experiments': len(results['detailed_results']),
        'mean_pgr': float(pgr_mean),
        'mean_imitation_score': float(imitation_mean),
        'high_pgr_low_imitation_count': int(high_pgr_low_imitation),
        'high_imitation_low_pgr_count': int(high_imitation_low_pgr),
        'pgr_std': float(np.std(results['pgr_map'])),
        'imitation_std': float(np.std(results['imitation_map']))
    }

    with open(os.path.join(results_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print("Experiment completed. Results saved to:", results_dir)
    print(f"Mean PGR: {pgr_mean:.3f}")
    print(f"Mean Imitation Score: {imitation_mean:.3f}")

    return results


if __name__ == '__main__':
    main()