#!/usr/bin/env python3
"""
Goodhart's Law in Automated W2S Research: Held-out Leakage Experiment

This simulates how repeated submission to held-out validation inflates
apparent progress in automated weak-to-strong generalization research.
"""

import numpy as np
import json
import random
from typing import Dict, List, Tuple

class SyntheticW2STask:
    """Synthetic weak-to-strong generalization task."""

    def __init__(self, n_samples: int = 1000, noise_level: float = 0.1, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)

        # Generate true function (what the strong model knows)
        self.X = np.random.randn(n_samples, 10)  # 10D input
        self.true_labels = (self.X[:, 0] + 0.5 * self.X[:, 1] - 0.3 * self.X[:, 2] > 0).astype(int)

        # Weak supervisor has systematic bias: flips 30% of positive labels
        self.weak_labels = self.true_labels.copy()
        pos_mask = self.true_labels == 1
        flip_mask = np.random.random(np.sum(pos_mask)) < 0.3
        self.weak_labels[pos_mask] = np.where(flip_mask, 0, self.weak_labels[pos_mask])

        # Add some noise to weak labels
        noise_mask = np.random.random(n_samples) < noise_level
        self.weak_labels[noise_mask] = 1 - self.weak_labels[noise_mask]

        # Split data
        n_train = n_samples // 2
        n_heldout = n_samples // 4
        n_test = n_samples - n_train - n_heldout

        self.X_train = self.X[:n_train]
        self.weak_train = self.weak_labels[:n_train]
        self.true_train = self.true_labels[:n_train]

        self.X_heldout = self.X[n_train:n_train+n_heldout]
        self.weak_heldout = self.weak_labels[n_train:n_train+n_heldout]
        self.true_heldout = self.true_labels[n_train:n_train+n_heldout]

        self.X_test = self.X[n_train+n_heldout:]
        self.weak_test = self.weak_labels[n_train+n_heldout:]
        self.true_test = self.true_labels[n_train+n_heldout:]

class SimpleW2SMethod:
    """Simple weak-to-strong method with hyperparameter variants."""

    def __init__(self, method_id: str, alpha: float = 1.0, beta: float = 0.0,
                 threshold: float = 0.5, noise_std: float = 0.1):
        self.method_id = method_id
        self.alpha = alpha  # Weight on weak labels
        self.beta = beta    # Correction factor
        self.threshold = threshold
        self.noise_std = noise_std

    def predict(self, X: np.ndarray, weak_preds: np.ndarray) -> np.ndarray:
        """Predict using weak supervision + some 'learned' correction."""
        # Simple linear combination with noise (simulating method uncertainty)
        raw_scores = self.alpha * weak_preds + self.beta * (2 * weak_preds - 1)
        raw_scores += np.random.normal(0, self.noise_std, len(raw_scores))
        return (raw_scores > self.threshold).astype(int)

def evaluate_method(method: SimpleW2SMethod, X: np.ndarray,
                   weak_labels: np.ndarray, true_labels: np.ndarray) -> float:
    """Evaluate method accuracy against true labels."""
    preds = method.predict(X, weak_labels)
    return np.mean(preds == true_labels)

def simulate_automated_researcher(task: SyntheticW2STask, n_iterations: int = 50,
                                methods_per_iteration: int = 10) -> Dict:
    """Simulate an automated researcher repeatedly submitting to held-out."""

    results = {
        'heldout_scores': [],
        'test_scores': [],
        'best_methods': [],
        'iteration': []
    }

    # Base method performance (before any optimization)
    base_method = SimpleW2SMethod("base", alpha=1.0, beta=0.0)
    base_heldout = evaluate_method(base_method, task.X_heldout, task.weak_heldout, task.true_heldout)
    base_test = evaluate_method(base_method, task.X_test, task.weak_test, task.true_test)

    print(f"Base method - Held-out: {base_heldout:.3f}, Test: {base_test:.3f}")

    current_best_heldout = base_heldout
    current_best_method = base_method

    for iteration in range(n_iterations):
        # Generate random method variants
        methods = []
        for i in range(methods_per_iteration):
            # Random hyperparameters around current best
            alpha = max(0.1, current_best_method.alpha + np.random.normal(0, 0.2))
            beta = current_best_method.beta + np.random.normal(0, 0.1)
            threshold = np.clip(current_best_method.threshold + np.random.normal(0, 0.1), 0.1, 0.9)
            noise_std = max(0.01, current_best_method.noise_std + np.random.normal(0, 0.05))

            method = SimpleW2SMethod(f"iter_{iteration}_method_{i}", alpha, beta, threshold, noise_std)
            methods.append(method)

        # Evaluate all methods on held-out (this is the problematic part!)
        heldout_scores = []
        test_scores = []

        for method in methods:
            heldout_score = evaluate_method(method, task.X_heldout, task.weak_heldout, task.true_heldout)
            test_score = evaluate_method(method, task.X_test, task.weak_test, task.true_test)
            heldout_scores.append(heldout_score)
            test_scores.append(test_score)

        # Select best method based on held-out score
        best_idx = np.argmax(heldout_scores)
        best_heldout = heldout_scores[best_idx]
        best_test = test_scores[best_idx]

        if best_heldout > current_best_heldout:
            current_best_heldout = best_heldout
            current_best_method = methods[best_idx]

        results['heldout_scores'].append(best_heldout)
        results['test_scores'].append(best_test)
        results['best_methods'].append(current_best_method.method_id)
        results['iteration'].append(iteration)

        if iteration % 10 == 0:
            print(f"Iteration {iteration}: Best held-out: {best_heldout:.3f}, "
                  f"corresponding test: {best_test:.3f}")

    return results

def analyze_optimism_bias(results: Dict) -> Dict:
    """Analyze the optimism bias in held-out vs test performance."""
    heldout_scores = np.array(results['heldout_scores'])
    test_scores = np.array(results['test_scores'])

    # Calculate running maximums (what the researcher sees)
    running_max_heldout = np.maximum.accumulate(heldout_scores)

    # Initial scores
    initial_heldout = heldout_scores[0] if len(heldout_scores) > 0 else 0
    initial_test = test_scores[0] if len(test_scores) > 0 else 0

    # Final scores
    final_heldout = running_max_heldout[-1]
    final_test = test_scores[np.argmax(np.cumsum(heldout_scores == running_max_heldout))]

    # Optimism bias
    apparent_improvement_heldout = final_heldout - initial_heldout
    actual_improvement_test = final_test - initial_test
    optimism_bias = apparent_improvement_heldout - actual_improvement_test

    analysis = {
        'initial_heldout': initial_heldout,
        'initial_test': initial_test,
        'final_heldout': final_heldout,
        'final_test': final_test,
        'apparent_improvement_heldout': apparent_improvement_heldout,
        'actual_improvement_test': actual_improvement_test,
        'optimism_bias': optimism_bias,
        'bias_ratio': optimism_bias / max(apparent_improvement_heldout, 1e-6)
    }

    return analysis

def run_experiment():
    """Run the main experiment."""
    print("Running Goodhart's Law experiment for automated W2S research...")

    # Create synthetic task
    task = SyntheticW2STask(n_samples=1000, seed=42)

    print(f"Task statistics:")
    print(f"  Weak supervisor accuracy: {np.mean(task.weak_train == task.true_train):.3f}")
    print(f"  Held-out weak accuracy: {np.mean(task.weak_heldout == task.true_heldout):.3f}")
    print(f"  Test weak accuracy: {np.mean(task.weak_test == task.true_test):.3f}")

    # Run automated researcher simulation
    results = simulate_automated_researcher(task, n_iterations=50, methods_per_iteration=15)

    # Analyze results
    analysis = analyze_optimism_bias(results)

    print("\n" + "="*50)
    print("RESULTS:")
    print(f"Initial held-out score: {analysis['initial_heldout']:.3f}")
    print(f"Final held-out score: {analysis['final_heldout']:.3f}")
    print(f"Apparent improvement: {analysis['apparent_improvement_heldout']:.3f}")
    print(f"Initial test score: {analysis['initial_test']:.3f}")
    print(f"Final test score: {analysis['final_test']:.3f}")
    print(f"Actual improvement: {analysis['actual_improvement_test']:.3f}")
    print(f"Optimism bias: {analysis['optimism_bias']:.3f}")
    print(f"Bias ratio: {analysis['bias_ratio']:.3f}")

    return results, analysis

if __name__ == "__main__":
    results, analysis = run_experiment()

    # Save results
    with open('/home/user/fab_out/artifact/results/experiment_results.json', 'w') as f:
        json.dump({
            'results': results,
            'analysis': analysis
        }, f, indent=2)

    print(f"\nResults saved to experiment_results.json")