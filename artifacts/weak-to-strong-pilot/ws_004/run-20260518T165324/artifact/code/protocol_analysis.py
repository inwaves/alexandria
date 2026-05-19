#!/usr/bin/env python3
"""
Protocol Analysis: Quantifying optimism bias vs submission budget
and proposing concrete mitigation protocols.
"""

import numpy as np
import json
from goodhart_experiment import SyntheticW2STask, SimpleW2SMethod, evaluate_method

def test_submission_budgets(task: SyntheticW2STask, budgets: list = [5, 10, 20, 50, 100]):
    """Test how optimism bias scales with submission budget."""

    results = {}

    for budget in budgets:
        print(f"Testing budget of {budget} submissions...")

        # Base method
        base_method = SimpleW2SMethod("base", alpha=1.0, beta=0.0)
        base_heldout = evaluate_method(base_method, task.X_heldout, task.weak_heldout, task.true_heldout)
        base_test = evaluate_method(base_method, task.X_test, task.weak_test, task.true_test)

        # Generate many random methods
        methods = []
        heldout_scores = []
        test_scores = []

        for i in range(budget):
            # Random hyperparameters
            alpha = max(0.1, np.random.normal(1.0, 0.3))
            beta = np.random.normal(0.0, 0.2)
            threshold = np.clip(np.random.normal(0.5, 0.2), 0.1, 0.9)
            noise_std = max(0.01, np.random.normal(0.1, 0.05))

            method = SimpleW2SMethod(f"method_{i}", alpha, beta, threshold, noise_std)
            methods.append(method)

            h_score = evaluate_method(method, task.X_heldout, task.weak_heldout, task.true_heldout)
            t_score = evaluate_method(method, task.X_test, task.weak_test, task.true_test)

            heldout_scores.append(h_score)
            test_scores.append(t_score)

        # Find best method according to held-out
        best_idx = np.argmax(heldout_scores)
        best_heldout = heldout_scores[best_idx]
        best_test = test_scores[best_idx]

        # Calculate bias
        apparent_improvement = best_heldout - base_heldout
        actual_improvement = best_test - base_test
        optimism_bias = apparent_improvement - actual_improvement

        results[budget] = {
            'base_heldout': base_heldout,
            'base_test': base_test,
            'best_heldout': best_heldout,
            'best_test': best_test,
            'apparent_improvement': apparent_improvement,
            'actual_improvement': actual_improvement,
            'optimism_bias': optimism_bias,
            'bias_ratio': optimism_bias / max(apparent_improvement, 1e-6),
            'n_submissions': budget
        }

        print(f"  Apparent improvement: {apparent_improvement:.3f}")
        print(f"  Actual improvement: {actual_improvement:.3f}")
        print(f"  Optimism bias: {optimism_bias:.3f}")

    return results

def test_holdout_rotation(task: SyntheticW2STask, n_rotations: int = 5,
                         submissions_per_rotation: int = 10):
    """Test holdout rotation protocol."""

    print(f"Testing holdout rotation: {n_rotations} rotations, {submissions_per_rotation} submissions each")

    # Split held-out data into rotation sets
    n_heldout = len(task.X_heldout)
    rotation_size = n_heldout // n_rotations

    rotation_results = []
    cumulative_test_scores = []

    best_method = SimpleW2SMethod("base", alpha=1.0, beta=0.0)

    for rotation in range(n_rotations):
        start_idx = rotation * rotation_size
        end_idx = min((rotation + 1) * rotation_size, n_heldout)

        # Use this rotation's held-out slice
        X_rot = task.X_heldout[start_idx:end_idx]
        weak_rot = task.weak_heldout[start_idx:end_idx]
        true_rot = task.true_heldout[start_idx:end_idx]

        # Generate methods for this rotation
        best_rot_score = -1
        best_rot_method = best_method

        for i in range(submissions_per_rotation):
            alpha = max(0.1, best_method.alpha + np.random.normal(0, 0.2))
            beta = best_method.beta + np.random.normal(0, 0.1)
            threshold = np.clip(best_method.threshold + np.random.normal(0, 0.1), 0.1, 0.9)
            noise_std = max(0.01, best_method.noise_std + np.random.normal(0, 0.05))

            method = SimpleW2SMethod(f"rot_{rotation}_method_{i}", alpha, beta, threshold, noise_std)

            rot_score = evaluate_method(method, X_rot, weak_rot, true_rot)
            if rot_score > best_rot_score:
                best_rot_score = rot_score
                best_rot_method = method

        # Evaluate best method on full test set
        test_score = evaluate_method(best_rot_method, task.X_test, task.weak_test, task.true_test)

        rotation_results.append({
            'rotation': rotation,
            'best_rotation_score': best_rot_score,
            'test_score': test_score
        })

        cumulative_test_scores.append(test_score)
        best_method = best_rot_method

        print(f"  Rotation {rotation}: score={best_rot_score:.3f}, test={test_score:.3f}")

    return rotation_results, cumulative_test_scores

def propose_protocols(budget_results: dict) -> dict:
    """Propose concrete protocols based on experimental results."""

    # Analyze how bias scales with budget
    budgets = sorted(budget_results.keys())
    biases = [budget_results[b]['optimism_bias'] for b in budgets]

    # Find elbow point (diminishing returns)
    bias_diffs = np.diff(biases)
    if len(bias_diffs) > 0:
        elbow_idx = np.argmax(bias_diffs) + 1
        recommended_budget = budgets[elbow_idx] if elbow_idx < len(budgets) else budgets[-1]
    else:
        recommended_budget = budgets[0] if budgets else 10

    protocols = {
        'submission_budget': {
            'recommended_limit': int(recommended_budget),
            'rationale': f'Elbow point in bias curve at {recommended_budget} submissions',
            'expected_bias': budget_results.get(recommended_budget, {}).get('optimism_bias', 0)
        },
        'holdout_rotation': {
            'recommended_rotations': 3,
            'submissions_per_rotation': int(recommended_budget // 3),
            'rationale': 'Limit exposure to any single held-out split'
        },
        'bias_correction': {
            'method': 'bootstrap_confidence_interval',
            'description': 'Estimate optimism bias via bootstrap resampling of held-out'
        },
        'early_stopping': {
            'patience': 5,
            'min_improvement': 0.001,
            'description': 'Stop if no meaningful improvement in held-out score'
        }
    }

    return protocols

def run_protocol_analysis():
    """Run the protocol analysis experiment."""

    print("Running protocol analysis...")

    # Create task
    task = SyntheticW2STask(n_samples=1200, seed=123)  # Larger for rotation test

    # Test different submission budgets
    budgets = [5, 10, 20, 50, 100]
    budget_results = test_submission_budgets(task, budgets)

    print("\n" + "="*40)
    print("BUDGET ANALYSIS:")
    for budget in budgets:
        result = budget_results[budget]
        print(f"Budget {budget:3d}: bias={result['optimism_bias']:+.3f}, "
              f"ratio={result['bias_ratio']:+.2f}")

    # Test holdout rotation
    print("\n" + "="*40)
    rotation_results, cumulative_test = test_holdout_rotation(task)

    # Propose protocols
    protocols = propose_protocols(budget_results)

    print("\n" + "="*40)
    print("PROPOSED PROTOCOLS:")
    print(f"1. Submission budget: {protocols['submission_budget']['recommended_limit']}")
    print(f"2. Holdout rotation: {protocols['holdout_rotation']['recommended_rotations']} rotations")
    print(f"3. Early stopping patience: {protocols['early_stopping']['patience']}")

    return {
        'budget_results': budget_results,
        'rotation_results': rotation_results,
        'protocols': protocols
    }

if __name__ == "__main__":
    results = run_protocol_analysis()

    with open('/home/user/fab_out/artifact/results/protocol_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nProtocol analysis saved.")