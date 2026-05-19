#!/usr/bin/env python3
"""
Minimal Weak-to-Strong Generalization: PGR vs Imitation Regime Map

Ultra-simplified version for very fast execution.
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


def run_experiment():
    """Run minimal experiment."""
    print("Generating data...")

    # Very small synthetic dataset
    X, y = make_classification(n_samples=500, n_features=10, n_informative=8,
                             n_classes=3, random_state=42, class_sep=1.5)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Test 3x3 grid for speed
    capacity_levels = np.array([0.0, 0.5, 1.0])
    noise_levels = np.array([0.0, 0.5, 1.0])

    results = {
        'capacity_levels': capacity_levels,
        'noise_levels': noise_levels,
        'pgr_map': np.zeros((3, 3)),
        'imitation_map': np.zeros((3, 3)),
        'detailed_results': []
    }

    print("Running 9 quick experiments...")

    for i, noise_level in enumerate(noise_levels):
        for j, capacity_level in enumerate(capacity_levels):
            print(f"  Cap {capacity_level:.1f}, Noise {noise_level:.1f}")

            # Ground truth strong baseline
            strong_model = MLPClassifier(hidden_layer_sizes=(20,), max_iter=100, random_state=42)
            strong_model.fit(X_train, y_train)
            strong_acc = accuracy_score(y_test, strong_model.predict(X_test))

            # Weak supervisor
            if capacity_level < 0.5:
                # Very weak: logistic on 3 features only
                weak_model = LogisticRegression(max_iter=100, random_state=42)
                weak_model.fit(X_train[:, :3], y_train)  # Only first 3 features
                weak_pred_train = weak_model.predict(X_train[:, :3])
                weak_pred_test = weak_model.predict(X_test[:, :3])
            else:
                # Less weak: small MLP
                weak_model = MLPClassifier(hidden_layer_sizes=(5,), max_iter=100, random_state=42)
                weak_model.fit(X_train, y_train)
                weak_pred_train = weak_model.predict(X_train)
                weak_pred_test = weak_model.predict(X_test)

            weak_acc = accuracy_score(y_test, weak_pred_test)

            # Add noise to weak predictions
            if noise_level > 0:
                n_flip = int(len(weak_pred_train) * noise_level * 0.2)  # Up to 20% flips
                flip_idx = np.random.choice(len(weak_pred_train), n_flip, replace=False)
                weak_pred_train[flip_idx] = 0  # Bias toward class 0

            # Strong student trained on weak labels
            student_model = MLPClassifier(hidden_layer_sizes=(20,), max_iter=100, random_state=42)
            student_model.fit(X_train, weak_pred_train)
            student_pred_test = student_model.predict(X_test)
            student_acc = accuracy_score(y_test, student_pred_test)

            # Calculate PGR
            if strong_acc > weak_acc:
                pgr = max(0.0, (student_acc - weak_acc) / (strong_acc - weak_acc))
            else:
                pgr = 0.0

            # Calculate imitation score
            weak_errors = (weak_pred_test != y_test)
            if np.any(weak_errors):
                imitation_score = np.mean(weak_pred_test[weak_errors] == student_pred_test[weak_errors])
            else:
                imitation_score = 0.0

            results['pgr_map'][i, j] = pgr
            results['imitation_map'][i, j] = imitation_score

            results['detailed_results'].append({
                'capacity_level': capacity_level,
                'noise_level': noise_level,
                'weak_acc': weak_acc,
                'strong_acc': strong_acc,
                'student_acc': student_acc,
                'pgr': pgr,
                'imitation_score': imitation_score
            })

    return results


def plot_results(results, output_dir):
    """Generate plots."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # PGR map
    im1 = ax1.imshow(results['pgr_map'], aspect='auto', origin='lower',
                     extent=[0, 1, 0, 1], cmap='viridis')
    ax1.set_xlabel('Capacity Level')
    ax1.set_ylabel('Noise Level')
    ax1.set_title('PGR')
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


def main():
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')

    print("Starting minimal W2S experiment...")
    results = run_experiment()

    # Save results
    json_results = {
        'capacity_levels': results['capacity_levels'].tolist(),
        'noise_levels': results['noise_levels'].tolist(),
        'pgr_map': results['pgr_map'].tolist(),
        'imitation_map': results['imitation_map'].tolist(),
        'detailed_results': results['detailed_results']
    }

    with open(os.path.join(results_dir, 'detailed_results.json'), 'w') as f:
        json.dump(json_results, f, indent=2)

    # Plot
    plot_results(results, results_dir)

    # Summary
    pgr_mean = np.mean(results['pgr_map'])
    imitation_mean = np.mean(results['imitation_map'])

    summary = {
        'total_experiments': len(results['detailed_results']),
        'mean_pgr': float(pgr_mean),
        'mean_imitation_score': float(imitation_mean),
        'high_pgr_low_imitation_count': int(np.sum((results['pgr_map'] > 0.5) & (results['imitation_map'] < 0.5))),
        'high_imitation_low_pgr_count': int(np.sum((results['imitation_map'] > 0.5) & (results['pgr_map'] < 0.5))),
        'pgr_std': float(np.std(results['pgr_map'])),
        'imitation_std': float(np.std(results['imitation_map']))
    }

    with open(os.path.join(results_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"Experiment completed! Mean PGR: {pgr_mean:.3f}, Mean Imitation: {imitation_mean:.3f}")
    print("Results saved to results/")

    return results


if __name__ == '__main__':
    main()