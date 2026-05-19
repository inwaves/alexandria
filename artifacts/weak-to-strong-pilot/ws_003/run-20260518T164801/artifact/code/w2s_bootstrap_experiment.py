#!/usr/bin/env python3
"""
Weak-to-Strong Bootstrapping Experiment

Tests whether weak->medium->strong supervision beats direct weak->strong supervision.
Synthetic setup with controllable model capabilities and systematic error patterns.
"""

import numpy as np
import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random


@dataclass
class ModelConfig:
    """Configuration for a synthetic model's capabilities and biases."""
    name: str
    base_accuracy: float  # Overall accuracy on the task
    systematic_errors: Dict[int, int]  # Maps true_class -> predicted_class for systematic mistakes
    error_probability: float  # Probability of making the systematic error vs random error


class SyntheticModel:
    """A synthetic model with controllable accuracy and systematic error patterns."""

    def __init__(self, config: ModelConfig, num_classes: int = 10, seed: int = 42):
        self.config = config
        self.num_classes = num_classes
        self.rng = np.random.RandomState(seed)

    def predict(self, true_labels: np.ndarray) -> np.ndarray:
        """Generate predictions with controlled accuracy and systematic errors."""
        predictions = np.copy(true_labels)

        for i, true_label in enumerate(true_labels):
            if self.rng.random() > self.config.base_accuracy:
                # Make an error
                if (true_label in self.config.systematic_errors and
                    self.rng.random() < self.config.error_probability):
                    # Make systematic error
                    predictions[i] = self.config.systematic_errors[true_label]
                else:
                    # Make random error
                    wrong_classes = list(range(self.num_classes))
                    wrong_classes.remove(true_label)
                    predictions[i] = self.rng.choice(wrong_classes)

        return predictions

    def get_confusion_matrix(self, true_labels: np.ndarray, predictions: np.ndarray) -> np.ndarray:
        """Compute confusion matrix."""
        cm = np.zeros((self.num_classes, self.num_classes))
        for true, pred in zip(true_labels, predictions):
            cm[true, pred] += 1
        return cm


class WeakToStrongExperiment:
    """Main experiment comparing direct vs. bootstrapped weak-to-strong supervision."""

    def __init__(self, num_classes: int = 10, seed: int = 42):
        self.num_classes = num_classes
        self.rng = np.random.RandomState(seed)
        self.results = {}

    def create_models(self, weak_acc: float, medium_acc: float, strong_acc: float) -> Tuple[SyntheticModel, SyntheticModel, SyntheticModel]:
        """Create weak, medium, and strong models with different capabilities."""

        # Weak model: low accuracy, systematic errors on classes 0->1, 2->3
        weak_config = ModelConfig(
            name="weak",
            base_accuracy=weak_acc,
            systematic_errors={0: 1, 2: 3, 4: 5},
            error_probability=0.8  # High probability of systematic errors
        )

        # Medium model: better accuracy, fewer systematic errors
        medium_config = ModelConfig(
            name="medium",
            base_accuracy=medium_acc,
            systematic_errors={0: 1, 2: 3},  # Fewer systematic errors
            error_probability=0.6
        )

        # Strong model: high accuracy, minimal systematic errors
        strong_config = ModelConfig(
            name="strong",
            base_accuracy=strong_acc,
            systematic_errors={0: 1},  # Very few systematic errors
            error_probability=0.3
        )

        return (SyntheticModel(weak_config, self.num_classes),
                SyntheticModel(medium_config, self.num_classes),
                SyntheticModel(strong_config, self.num_classes))

    def simulate_supervision(self, supervisor_model: SyntheticModel,
                           supervised_model: SyntheticModel,
                           true_labels: np.ndarray,
                           supervision_strength: float = 1.0) -> Tuple[np.ndarray, Dict]:
        """Simulate training a model under supervision from another model."""

        # Get supervisor's labels
        supervisor_labels = supervisor_model.predict(true_labels)

        # The supervised model learns from these labels
        # supervision_strength controls how much the supervised model adapts
        supervised_predictions = supervised_model.predict(true_labels)

        # Blend supervisor influence with model's natural predictions
        final_predictions = np.copy(supervised_predictions)

        # With some probability, adopt supervisor's systematic errors
        adoption_rate = supervision_strength * 0.7  # Max 70% adoption of supervisor patterns

        for i, (sup_pred, model_pred, true_label) in enumerate(zip(supervisor_labels, supervised_predictions, true_labels)):
            if self.rng.random() < adoption_rate:
                # Adopt supervisor's prediction pattern
                if sup_pred != true_label and sup_pred in supervisor_model.config.systematic_errors.values():
                    # This is a systematic error from supervisor - might adopt it
                    final_predictions[i] = sup_pred

        # Calculate metrics
        accuracy = np.mean(final_predictions == true_labels)
        supervisor_accuracy = np.mean(supervisor_labels == true_labels)

        # Measure error pattern similarity to supervisor
        supervisor_errors = (supervisor_labels != true_labels)
        supervised_errors = (final_predictions != true_labels)
        error_overlap = np.mean(supervisor_errors & supervised_errors)

        metrics = {
            'accuracy': accuracy,
            'supervisor_accuracy': supervisor_accuracy,
            'error_overlap': error_overlap,
            'total_errors': np.mean(supervised_errors)
        }

        return final_predictions, metrics

    def run_single_experiment(self, weak_acc: float, medium_acc: float, strong_acc: float,
                             data_size: int = 1000) -> Dict:
        """Run a single experiment comparing direct vs. bootstrapped supervision."""

        # Generate ground truth data
        true_labels = self.rng.randint(0, self.num_classes, data_size)

        # Create models
        weak_model, medium_model, strong_model = self.create_models(weak_acc, medium_acc, strong_acc)

        # Direct weak->strong supervision
        direct_preds, direct_metrics = self.simulate_supervision(
            weak_model, strong_model, true_labels
        )

        # Bootstrapped weak->medium->strong supervision
        # First: weak->medium
        medium_supervised_preds, medium_metrics = self.simulate_supervision(
            weak_model, medium_model, true_labels
        )

        # Then: medium->strong (using the supervised medium model as supervisor)
        # Create a new "supervised medium" model that reflects the weak->medium training
        supervised_medium_config = ModelConfig(
            name="supervised_medium",
            base_accuracy=medium_metrics['accuracy'],
            systematic_errors=weak_model.config.systematic_errors,  # Inherited some weak patterns
            error_probability=0.5
        )
        supervised_medium_model = SyntheticModel(supervised_medium_config, self.num_classes)

        bootstrap_preds, bootstrap_metrics = self.simulate_supervision(
            supervised_medium_model, strong_model, true_labels
        )

        # Calculate capability gaps
        weak_strong_gap = strong_acc - weak_acc
        weak_medium_gap = medium_acc - weak_acc
        medium_strong_gap = strong_acc - medium_acc

        return {
            'weak_acc': weak_acc,
            'medium_acc': medium_acc,
            'strong_acc': strong_acc,
            'weak_strong_gap': weak_strong_gap,
            'weak_medium_gap': weak_medium_gap,
            'medium_strong_gap': medium_strong_gap,
            'direct': direct_metrics,
            'bootstrap': bootstrap_metrics,
            'bootstrap_advantage': bootstrap_metrics['accuracy'] - direct_metrics['accuracy'],
            'data_size': data_size
        }

    def run_gap_analysis(self) -> List[Dict]:
        """Run experiments across different capability gap configurations."""

        results = []

        # Test different capability gap configurations
        configs = [
            # (weak_acc, medium_acc, strong_acc)
            (0.3, 0.5, 0.7),   # Small gaps
            (0.3, 0.6, 0.9),   # Medium gaps
            (0.2, 0.5, 0.9),   # Large weak-strong gap
            (0.4, 0.6, 0.8),   # Small uniform gaps
            (0.1, 0.3, 0.9),   # Very large total gap
            (0.2, 0.7, 0.8),   # Large first jump, small second
            (0.5, 0.6, 0.9),   # Small first jump, large second
        ]

        for weak_acc, medium_acc, strong_acc in configs:
            # Run multiple trials for stability
            trial_results = []
            for trial in range(5):
                np.random.seed(42 + trial)
                result = self.run_single_experiment(weak_acc, medium_acc, strong_acc)
                trial_results.append(result)

            # Average across trials
            avg_result = self._average_results(trial_results)
            results.append(avg_result)

        return results

    def _average_results(self, trial_results: List[Dict]) -> Dict:
        """Average results across multiple trials."""
        avg = trial_results[0].copy()

        # Average the metrics
        for key in ['direct', 'bootstrap']:
            for metric in avg[key]:
                avg[key][metric] = np.mean([r[key][metric] for r in trial_results])

        avg['bootstrap_advantage'] = np.mean([r['bootstrap_advantage'] for r in trial_results])

        return avg


def main():
    """Run the main experiment and save results."""

    experiment = WeakToStrongExperiment(num_classes=10, seed=42)

    print("Running weak-to-strong bootstrapping experiment...")
    results = experiment.run_gap_analysis()

    # Save detailed results
    results_dir = os.path.expanduser('~/fab_out/artifact/results')
    with open(os.path.join(results_dir, 'experiment_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    # Create summary statistics
    summary = {
        'total_configs': len(results),
        'bootstrap_wins': sum(1 for r in results if r['bootstrap_advantage'] > 0.01),
        'bootstrap_neutral': sum(1 for r in results if -0.01 <= r['bootstrap_advantage'] <= 0.01),
        'bootstrap_loses': sum(1 for r in results if r['bootstrap_advantage'] < -0.01),
        'avg_bootstrap_advantage': np.mean([r['bootstrap_advantage'] for r in results]),
        'best_bootstrap_advantage': max(r['bootstrap_advantage'] for r in results),
        'worst_bootstrap_advantage': min(r['bootstrap_advantage'] for r in results)
    }

    with open(os.path.join(results_dir, 'summary_stats.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Analyze when bootstrapping helps vs. hurts
    analysis = analyze_bootstrap_patterns(results)

    with open(os.path.join(results_dir, 'pattern_analysis.json'), 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"Experiment complete. Bootstrap advantage: {summary['avg_bootstrap_advantage']:.4f}")
    print(f"Bootstrap wins: {summary['bootstrap_wins']}/{summary['total_configs']}")

    return results, summary, analysis


def analyze_bootstrap_patterns(results: List[Dict]) -> Dict:
    """Analyze patterns in when bootstrapping helps vs. hurts."""

    # Separate results by bootstrap performance
    winners = [r for r in results if r['bootstrap_advantage'] > 0.01]
    losers = [r for r in results if r['bootstrap_advantage'] < -0.01]

    def compute_stats(group):
        if not group:
            return {}
        return {
            'count': len(group),
            'avg_weak_strong_gap': np.mean([r['weak_strong_gap'] for r in group]),
            'avg_weak_medium_gap': np.mean([r['weak_medium_gap'] for r in group]),
            'avg_medium_strong_gap': np.mean([r['medium_strong_gap'] for r in group]),
            'avg_weak_acc': np.mean([r['weak_acc'] for r in group]),
            'avg_bootstrap_advantage': np.mean([r['bootstrap_advantage'] for r in group])
        }

    return {
        'bootstrap_winners': compute_stats(winners),
        'bootstrap_losers': compute_stats(losers),
        'total_results': len(results)
    }


if __name__ == "__main__":
    main()#!/usr/bin/env python3
"""
Weak-to-Strong Bootstrapping Experiment

Tests whether weak->medium->strong supervision beats direct weak->strong supervision.
Synthetic setup with controllable model capabilities and systematic error patterns.
"""

import numpy as np
import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random


@dataclass
class ModelConfig:
    """Configuration for a synthetic model's capabilities and biases."""
    name: str
    base_accuracy: float  # Overall accuracy on the task
    systematic_errors: Dict[int, int]  # Maps true_class -> predicted_class for systematic mistakes
    error_probability: float  # Probability of making the systematic error vs random error


class SyntheticModel:
    """A synthetic model with controllable accuracy and systematic error patterns."""

    def __init__(self, config: ModelConfig, num_classes: int = 10, seed: int = 42):
        self.config = config
        self.num_classes = num_classes
        self.rng = np.random.RandomState(seed)

    def predict(self, true_labels: np.ndarray) -> np.ndarray:
        """Generate predictions with controlled accuracy and systematic errors."""
        predictions = np.copy(true_labels)

        for i, true_label in enumerate(true_labels):
            if self.rng.random() > self.config.base_accuracy:
                # Make an error
                if (true_label in self.config.systematic_errors and
                    self.rng.random() < self.config.error_probability):
                    # Make systematic error
                    predictions[i] = self.config.systematic_errors[true_label]
                else:
                    # Make random error
                    wrong_classes = list(range(self.num_classes))
                    wrong_classes.remove(true_label)
                    predictions[i] = self.rng.choice(wrong_classes)

        return predictions

    def get_confusion_matrix(self, true_labels: np.ndarray, predictions: np.ndarray) -> np.ndarray:
        """Compute confusion matrix."""
        cm = np.zeros((self.num_classes, self.num_classes))
        for true, pred in zip(true_labels, predictions):
            cm[true, pred] += 1
        return cm


class WeakToStrongExperiment:
    """Main experiment comparing direct vs. bootstrapped weak-to-strong supervision."""

    def __init__(self, num_classes: int = 10, seed: int = 42):
        self.num_classes = num_classes
        self.rng = np.random.RandomState(seed)
        self.results = {}

    def create_models(self, weak_acc: float, medium_acc: float, strong_acc: float) -> Tuple[SyntheticModel, SyntheticModel, SyntheticModel]:
        """Create weak, medium, and strong models with different capabilities."""

        # Weak model: low accuracy, systematic errors on classes 0->1, 2->3
        weak_config = ModelConfig(
            name="weak",
            base_accuracy=weak_acc,
            systematic_errors={0: 1, 2: 3, 4: 5},
            error_probability=0.8  # High probability of systematic errors
        )

        # Medium model: better accuracy, fewer systematic errors
        medium_config = ModelConfig(
            name="medium",
            base_accuracy=medium_acc,
            systematic_errors={0: 1, 2: 3},  # Fewer systematic errors
            error_probability=0.6
        )

        # Strong model: high accuracy, minimal systematic errors
        strong_config = ModelConfig(
            name="strong",
            base_accuracy=strong_acc,
            systematic_errors={0: 1},  # Very few systematic errors
            error_probability=0.3
        )

        return (SyntheticModel(weak_config, self.num_classes),
                SyntheticModel(medium_config, self.num_classes),
                SyntheticModel(strong_config, self.num_classes))

    def simulate_supervision(self, supervisor_model: SyntheticModel,
                           supervised_model: SyntheticModel,
                           true_labels: np.ndarray,
                           supervision_strength: float = 1.0) -> Tuple[np.ndarray, Dict]:
        """Simulate training a model under supervision from another model."""

        # Get supervisor's labels
        supervisor_labels = supervisor_model.predict(true_labels)

        # The supervised model learns from these labels
        # supervision_strength controls how much the supervised model adapts
        supervised_predictions = supervised_model.predict(true_labels)

        # Blend supervisor influence with model's natural predictions
        final_predictions = np.copy(supervised_predictions)

        # With some probability, adopt supervisor's systematic errors
        adoption_rate = supervision_strength * 0.7  # Max 70% adoption of supervisor patterns

        for i, (sup_pred, model_pred, true_label) in enumerate(zip(supervisor_labels, supervised_predictions, true_labels)):
            if self.rng.random() < adoption_rate:
                # Adopt supervisor's prediction pattern
                if sup_pred != true_label and sup_pred in supervisor_model.config.systematic_errors.values():
                    # This is a systematic error from supervisor - might adopt it
                    final_predictions[i] = sup_pred

        # Calculate metrics
        accuracy = np.mean(final_predictions == true_labels)
        supervisor_accuracy = np.mean(supervisor_labels == true_labels)

        # Measure error pattern similarity to supervisor
        supervisor_errors = (supervisor_labels != true_labels)
        supervised_errors = (final_predictions != true_labels)
        error_overlap = np.mean(supervisor_errors & supervised_errors)

        metrics = {
            'accuracy': accuracy,
            'supervisor_accuracy': supervisor_accuracy,
            'error_overlap': error_overlap,
            'total_errors': np.mean(supervised_errors)
        }

        return final_predictions, metrics

    def run_single_experiment(self, weak_acc: float, medium_acc: float, strong_acc: float,
                             data_size: int = 1000) -> Dict:
        """Run a single experiment comparing direct vs. bootstrapped supervision."""

        # Generate ground truth data
        true_labels = self.rng.randint(0, self.num_classes, data_size)

        # Create models
        weak_model, medium_model, strong_model = self.create_models(weak_acc, medium_acc, strong_acc)

        # Direct weak->strong supervision
        direct_preds, direct_metrics = self.simulate_supervision(
            weak_model, strong_model, true_labels
        )

        # Bootstrapped weak->medium->strong supervision
        # First: weak->medium
        medium_supervised_preds, medium_metrics = self.simulate_supervision(
            weak_model, medium_model, true_labels
        )

        # Then: medium->strong (using the supervised medium model as supervisor)
        # Create a new "supervised medium" model that reflects the weak->medium training
        supervised_medium_config = ModelConfig(
            name="supervised_medium",
            base_accuracy=medium_metrics['accuracy'],
            systematic_errors=weak_model.config.systematic_errors,  # Inherited some weak patterns
            error_probability=0.5
        )
        supervised_medium_model = SyntheticModel(supervised_medium_config, self.num_classes)

        bootstrap_preds, bootstrap_metrics = self.simulate_supervision(
            supervised_medium_model, strong_model, true_labels
        )

        # Calculate capability gaps
        weak_strong_gap = strong_acc - weak_acc
        weak_medium_gap = medium_acc - weak_acc
        medium_strong_gap = strong_acc - medium_acc

        return {
            'weak_acc': weak_acc,
            'medium_acc': medium_acc,
            'strong_acc': strong_acc,
            'weak_strong_gap': weak_strong_gap,
            'weak_medium_gap': weak_medium_gap,
            'medium_strong_gap': medium_strong_gap,
            'direct': direct_metrics,
            'bootstrap': bootstrap_metrics,
            'bootstrap_advantage': bootstrap_metrics['accuracy'] - direct_metrics['accuracy'],
            'data_size': data_size
        }

    def run_gap_analysis(self) -> List[Dict]:
        """Run experiments across different capability gap configurations."""

        results = []

        # Test different capability gap configurations
        configs = [
            # (weak_acc, medium_acc, strong_acc)
            (0.3, 0.5, 0.7),   # Small gaps
            (0.3, 0.6, 0.9),   # Medium gaps
            (0.2, 0.5, 0.9),   # Large weak-strong gap
            (0.4, 0.6, 0.8),   # Small uniform gaps
            (0.1, 0.3, 0.9),   # Very large total gap
            (0.2, 0.7, 0.8),   # Large first jump, small second
            (0.5, 0.6, 0.9),   # Small first jump, large second
        ]

        for weak_acc, medium_acc, strong_acc in configs:
            # Run multiple trials for stability
            trial_results = []
            for trial in range(5):
                np.random.seed(42 + trial)
                result = self.run_single_experiment(weak_acc, medium_acc, strong_acc)
                trial_results.append(result)

            # Average across trials
            avg_result = self._average_results(trial_results)
            results.append(avg_result)

        return results

    def _average_results(self, trial_results: List[Dict]) -> Dict:
        """Average results across multiple trials."""
        avg = trial_results[0].copy()

        # Average the metrics
        for key in ['direct', 'bootstrap']:
            for metric in avg[key]:
                avg[key][metric] = np.mean([r[key][metric] for r in trial_results])

        avg['bootstrap_advantage'] = np.mean([r['bootstrap_advantage'] for r in trial_results])

        return avg


def main():
    """Run the main experiment and save results."""

    experiment = WeakToStrongExperiment(num_classes=10, seed=42)

    print("Running weak-to-strong bootstrapping experiment...")
    results = experiment.run_gap_analysis()

    # Save detailed results
    results_dir = os.path.expanduser('~/fab_out/artifact/results')
    with open(os.path.join(results_dir, 'experiment_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    # Create summary statistics
    summary = {
        'total_configs': len(results),
        'bootstrap_wins': sum(1 for r in results if r['bootstrap_advantage'] > 0.01),
        'bootstrap_neutral': sum(1 for r in results if -0.01 <= r['bootstrap_advantage'] <= 0.01),
        'bootstrap_loses': sum(1 for r in results if r['bootstrap_advantage'] < -0.01),
        'avg_bootstrap_advantage': np.mean([r['bootstrap_advantage'] for r in results]),
        'best_bootstrap_advantage': max(r['bootstrap_advantage'] for r in results),
        'worst_bootstrap_advantage': min(r['bootstrap_advantage'] for r in results)
    }

    with open(os.path.join(results_dir, 'summary_stats.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Analyze when bootstrapping helps vs. hurts
    analysis = analyze_bootstrap_patterns(results)

    with open(os.path.join(results_dir, 'pattern_analysis.json'), 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"Experiment complete. Bootstrap advantage: {summary['avg_bootstrap_advantage']:.4f}")
    print(f"Bootstrap wins: {summary['bootstrap_wins']}/{summary['total_configs']}")

    return results, summary, analysis


def analyze_bootstrap_patterns(results: List[Dict]) -> Dict:
    """Analyze patterns in when bootstrapping helps vs. hurts."""

    # Separate results by bootstrap performance
    winners = [r for r in results if r['bootstrap_advantage'] > 0.01]
    losers = [r for r in results if r['bootstrap_advantage'] < -0.01]

    def compute_stats(group):
        if not group:
            return {}
        return {
            'count': len(group),
            'avg_weak_strong_gap': np.mean([r['weak_strong_gap'] for r in group]),
            'avg_weak_medium_gap': np.mean([r['weak_medium_gap'] for r in group]),
            'avg_medium_strong_gap': np.mean([r['medium_strong_gap'] for r in group]),
            'avg_weak_acc': np.mean([r['weak_acc'] for r in group]),
            'avg_bootstrap_advantage': np.mean([r['bootstrap_advantage'] for r in group])
        }

    return {
        'bootstrap_winners': compute_stats(winners),
        'bootstrap_losers': compute_stats(losers),
        'total_results': len(results)
    }


if __name__ == "__main__":
    main()