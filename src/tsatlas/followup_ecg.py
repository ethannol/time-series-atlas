"""Declared exploratory ECG follow-ups, leaving original evidence untouched."""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .common import markdown_table, save_frame
from .data import write_json
from .ecg import CLASSES, MODELS, SEED, classification_scores, fit_fold, fold_indices

BOOTSTRAP_SEED = 20261110
BOOTSTRAP_REPLICATES = 2000
REPEAT_SEEDS = (20261110, 20261111, 20261112)
CONFUSION_COLUMNS = [f'truth_{truth}_prediction_{prediction}'
                     for truth in CLASSES for prediction in CLASSES]
PREDICTION_COLUMNS = ['beat_index', 'fold', 'record', 'person', 'sample',
                      'symbol', 'truth', 'model', 'prediction']


def patient_fold_mapping(people, seed, folds=5):
    """Sort string IDs, permute once, and assign permutation positions modulo five."""
    people = sorted(set(map(str, people)))
    if folds < 2 or len(people) < folds:
        raise ValueError('Need at least one person per fold')
    permuted = np.random.default_rng(seed).permutation(people)
    return {str(person): int(position % folds) for position, person in enumerate(permuted)}


def validate_predictions(predictions, beats, mapping, indices=None):
    """Require the same eligible held-out beats and metadata for every method."""
    indices = np.arange(len(beats)) if indices is None else np.sort(np.asarray(indices))
    if set(predictions.model) != set(MODELS):
        raise ValueError('Prediction methods do not match the four declared methods')
    for model in MODELS:
        group = predictions[predictions.model == model].sort_values('beat_index')
        if not group.beat_index.is_unique or not np.array_equal(group.beat_index, indices):
            raise ValueError(f'Incomplete or duplicate held-out coverage: {model}')
        for column, field in [('person', 'person'), ('record', 'record'), ('sample', 'sample'),
                              ('symbol', 'symbol'), ('truth', 'label')]:
            if not np.array_equal(group[column].to_numpy(), beats[field][indices]):
                raise ValueError(f'Misaligned {column}: {model}')
        expected_folds = [mapping[str(person)] for person in beats['person'][indices]]
        if not np.array_equal(group.fold, expected_folds):
            raise ValueError(f'Incorrect held-out fold: {model}')
        if not np.isin(group.prediction, CLASSES).all():
            raise ValueError(f'Unknown predicted class: {model}')


def patient_confusions(predictions):
    """Return person × method × true class × predicted class counts."""
    people = sorted(set(map(str, predictions.person)))
    counts = np.zeros((len(people), len(MODELS), len(CLASSES), len(CLASSES)), dtype=np.int64)
    grouped = predictions.groupby([predictions.person.astype(str), 'model'])
    for i, person in enumerate(people):
        reference = None
        for j, model in enumerate(MODELS):
            if (person, model) not in grouped.indices:
                raise ValueError('Methods must have identical unique patient/beat/truth rows')
            group = grouped.get_group((person, model)).sort_values('beat_index')
            identity = list(zip(group.beat_index, group.truth))
            if not identity or not group.beat_index.is_unique or (reference is not None and identity != reference):
                raise ValueError('Methods must have identical unique patient/beat/truth rows')
            reference = identity
            counts[i, j] = classification_scores(group.truth, group.prediction)['confusion']
    return people, counts


def bootstrap_confusions(counts, draws):
    """Sum whole-person counts using one shared draw matrix for all methods."""
    counts = np.asarray(counts)
    draws = np.asarray(draws)
    if (counts.ndim != 4 or counts.shape[1:] != (len(MODELS), len(CLASSES), len(CLASSES))
            or not np.issubdtype(counts.dtype, np.integer) or (counts < 0).any()):
        raise ValueError('Expected nonnegative integer person/method/class confusion counts')
    if (draws.ndim != 2 or draws.shape[1] != len(counts) or not np.issubdtype(draws.dtype, np.integer)
            or (draws < 0).any() or (draws >= len(counts)).any()):
        raise ValueError('Expected one valid patient index per sampled group')
    weights = np.stack([np.bincount(row, minlength=len(counts)) for row in draws])
    return np.einsum('rp,pmij->rmij', weights, counts)


def confusion_metrics(confusions):
    """Pooled accuracy and fixed-four-class F1; absent/never-predicted F1 is zero."""
    confusions = np.asarray(confusions)
    tp = np.diagonal(confusions, axis1=-2, axis2=-1)
    denominator = confusions.sum(axis=-1) + confusions.sum(axis=-2)
    f1 = np.divide(2. * tp, denominator, out=np.zeros_like(tp, dtype=float), where=denominator != 0)
    n = confusions.sum(axis=(-2, -1))
    if (n <= 0).any():
        raise ValueError('Cannot score an empty confusion matrix')
    return {'n': n, 'accuracy': tp.sum(axis=-1) / n, 'macro_f1': f1.mean(axis=-1)}


def _score_frames(predictions, assignment, seed):
    scores, classes = [], []
    for fold, frame in [('pooled', predictions), *list(predictions.groupby('fold'))]:
        for model, group in frame.groupby('model'):
            score = classification_scores(group.truth, group.prediction)
            base = {'assignment': assignment, 'assignment_seed': seed, 'fold': str(fold), 'model': model}
            scores.append({**base, **{key: score[key] for key in
                                     ['n', 'accuracy', 'macro_f1', 'supported_macro_f1',
                                      'supported_macro_recall', 'supported_classes']}})
            classes.extend({**base, **row} for row in score['per_class'])
    return scores, classes


def _support_rows(beats, mapping, assignment, seed):
    rows = []
    for fold in range(5):
        train, test = fold_indices(beats, mapping, fold)
        for label in CLASSES:
            train_class = train[beats['label'][train] == label]
            test_class = test[beats['label'][test] == label]
            rows.append({'assignment': assignment, 'assignment_seed': seed, 'fold': fold, 'class': label,
                         'capped_training_beats': len(train_class), 'test_beats': len(test_class),
                         'training_people_with_class': len(set(beats['person'][train_class])),
                         'test_people_with_class': len(set(beats['person'][test_class])),
                         'training_people': len(set(beats['person'][train])),
                         'test_people': len(set(beats['person'][test]))})
    return rows


def _bootstrap(out, predictions):
    people, counts = patient_confusions(predictions)
    draws = np.random.default_rng(BOOTSTRAP_SEED).integers(
        0, len(people), size=(BOOTSTRAP_REPLICATES, len(people)))
    summed = bootstrap_confusions(counts, draws)
    scores = confusion_metrics(summed)
    patient_rows = [{'patient_index': i, 'person': person, 'model': model,
                     **dict(zip(CONFUSION_COLUMNS, counts[i, j].reshape(-1)))}
                    for i, person in enumerate(people) for j, model in enumerate(MODELS)]
    save_frame(pd.DataFrame(patient_rows), out / 'followup-patient-confusions.csv.gz')
    save_frame(pd.DataFrame({'replicate': np.repeat(np.arange(BOOTSTRAP_REPLICATES), len(people)),
                             'draw_position': np.tile(np.arange(len(people)), BOOTSTRAP_REPLICATES),
                             'patient_index': draws.reshape(-1),
                             'person': np.asarray(people)[draws.reshape(-1)]}),
               out / 'followup-bootstrap-draws.csv.gz')
    replicates = pd.DataFrame({'replicate': np.arange(BOOTSTRAP_REPLICATES)})
    summary = []
    for j, model in enumerate(MODELS):
        for metric in ['n', 'accuracy', 'macro_f1']:
            replicates[f'{model}_{metric}'] = scores[metric][:, j]
            if metric != 'n':
                quantiles = np.quantile(scores[metric][:, j], [.025, .5, .975])
                summary.append({'method_or_contrast': model, 'metric': metric,
                                **dict(zip(['p2_5', 'p50', 'p97_5'], quantiles))})
    difference = scores['macro_f1'][:, MODELS.index('forest')] - scores['macro_f1'][:, MODELS.index('logistic')]
    replicates['forest_minus_logistic_macro_f1'] = difference
    summary.append({'method_or_contrast': 'forest-minus-logistic', 'metric': 'macro_f1',
                    **dict(zip(['p2_5', 'p50', 'p97_5'], np.quantile(difference, [.025, .5, .975])))})
    save_frame(replicates, out / 'followup-bootstrap-replicates.csv.gz')
    confusion_frame = pd.DataFrame(summed.reshape(-1, 16), columns=CONFUSION_COLUMNS)
    confusion_frame.insert(0, 'model', np.tile(MODELS, BOOTSTRAP_REPLICATES))
    confusion_frame.insert(0, 'replicate', np.repeat(np.arange(BOOTSTRAP_REPLICATES), len(MODELS)))
    save_frame(confusion_frame, out / 'followup-bootstrap-confusions.csv.gz')
    save_frame(pd.DataFrame(summary), out / 'followup-bootstrap-summary.csv.gz')
    return summary


def ecg_followup(out, waves, beats, predictions, metrics, mapping):
    """Write all declared follow-up evidence and return a labeled report section."""
    if len(set(map(str, beats['person']))) != 43 or set(mapping) != set(map(str, beats['person'])):
        raise ValueError('The declared ECG follow-up requires the original 43 patient groups')
    validate_predictions(predictions, beats, mapping)
    # Detect stale or mismatched original metrics before comparisons or new fits.
    for model in MODELS:
        group = predictions[predictions.model == model]
        if classification_scores(group.truth, group.prediction) != metrics[model]:
            raise ValueError(f'Original metric/prediction mismatch: {model}')
    bootstrap_summary = _bootstrap(out, predictions)
    original_scores, class_rows = _score_frames(predictions, 'original', SEED)
    score_rows = list(original_scores)
    support_rows = _support_rows(beats, mapping, 'original', SEED)
    comparison = [{'assignment': 'original', 'assignment_seed': SEED, 'model': model,
                   'status': 'complete', **{key: metrics[model][key] for key in ['n', 'macro_f1', 'accuracy']}}
                  for model in MODELS]
    failures = []
    for seed in REPEAT_SEEDS:
        assignment = f'repeat-{seed}'
        prefix = f'followup-{assignment}'
        repeat_mapping = patient_fold_mapping(beats['person'], seed)
        write_json(out / f'{prefix}-mapping.json', {
            'assignment_seed': seed, 'rule': 'sorted string patient IDs; default_rng permutation; position % 5',
            'patient_to_fold': repeat_mapping, 'fitting_seed': SEED, 'training_cap_per_person': 1000})
        support_rows.extend(_support_rows(beats, repeat_mapping, assignment, seed))
        frames, attempted_frames, membership, audits = [], [], [], {}
        for fold in range(5):
            train, test = fold_indices(beats, repeat_mapping, fold)
            membership.append(pd.DataFrame({'fold': fold, 'beat_index': train, 'person': beats['person'][train],
                                            'record': beats['record'][train], 'sample': beats['sample'][train],
                                            'label': beats['label'][train]}))
            audit = None
            try:
                frame, audit = fit_fold(waves, beats, train, test, fold)
                attempted_frames.append(frame)
                validate_predictions(frame, beats, repeat_mapping, test)
                frames.append(frame)
                audits[str(fold)] = {'status': 'complete', 'audit': audit}
            except Exception as error:
                failure = {'assignment': assignment, 'assignment_seed': seed, 'fold': fold,
                           'status': 'failed', 'error_type': type(error).__name__, 'error': str(error),
                           'train_beats': len(train), 'test_beats': len(test),
                           'training_people': sorted(set(map(str, beats['person'][train]))),
                           'test_people': sorted(set(map(str, beats['person'][test])))}
                failures.append(failure)
                audits[str(fold)] = {**failure, 'audit': audit}
        frame = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=PREDICTION_COLUMNS)
        attempted = pd.concat(attempted_frames, ignore_index=True) if attempted_frames else frame
        save_frame(attempted, out / f'{prefix}-predictions.csv.gz')
        save_frame(pd.concat(membership, ignore_index=True), out / f'{prefix}-training-membership.csv.gz')
        write_json(out / f'{prefix}-model-audit.json', audits)
        complete = len(frames) == 5
        pooled = {}
        if complete:
            validate_predictions(frame, beats, repeat_mapping)
            pooled = {model: classification_scores(group.truth, group.prediction)
                      for model, group in frame.groupby('model')}
        # Retain available fold scores after failures, but never call a partial pool a repeat score.
        if len(frame):
            repeat_scores, repeat_classes = _score_frames(frame, assignment, seed)
            score_rows.extend(row for row in repeat_scores if complete or row['fold'] != 'pooled')
            class_rows.extend(row for row in repeat_classes if complete or row['fold'] != 'pooled')
        write_json(out / f'{prefix}-metrics.json', {'status': 'complete' if complete else 'incomplete',
                                                  'pooled': pooled, 'completed_folds': len(frames),
                                                  'expected_folds': 5})
        for model in MODELS:
            comparison.append({'assignment': assignment, 'assignment_seed': seed, 'model': model,
                               'status': 'complete' if complete else 'incomplete',
                               **{key: pooled[model][key] if complete else None for key in ['n', 'macro_f1', 'accuracy']}})
    save_frame(pd.DataFrame(score_rows), out / 'followup-scores.csv.gz')
    save_frame(pd.DataFrame(class_rows), out / 'followup-class-scores.csv.gz')
    save_frame(pd.DataFrame(support_rows), out / 'followup-fold-support.csv.gz')
    comparison_frame = pd.DataFrame(comparison)
    save_frame(comparison_frame, out / 'followup-split-comparison.csv.gz')
    ranges = []
    for model in MODELS:
        group = comparison_frame[(comparison_frame.model == model) & (comparison_frame.status == 'complete')]
        for metric in ['macro_f1', 'accuracy']:
            ranges.append({'model': model, 'metric': metric, 'minimum': float(group[metric].min()),
                           'maximum': float(group[metric].max()), 'completed_assignments': len(group),
                           'declared_assignments': 1 + len(REPEAT_SEEDS), 'includes_original': True})
    save_frame(pd.DataFrame(ranges), out / 'followup-split-ranges.csv.gz')
    write_json(out / 'followup-status.json', {
        'status': 'complete' if not failures else 'incomplete', 'failures': failures,
        'bootstrap': {'seed': BOOTSTRAP_SEED, 'replicates': BOOTSTRAP_REPLICATES, 'patient_groups': 43,
                      'patient_order': sorted(mapping), 'quantile_method': 'numpy linear',
                      'unit': 'patient group, all saved held-out beats together',
                      'same_draws_all_methods': True, 'f1_zero_denominator': 0},
        'repeat_assignment_seeds': list(REPEAT_SEEDS), 'fitting_seed': SEED,
        'training_cap_per_person': 1000, 'folds': 5})
    _figure(out, comparison_frame, pd.DataFrame(support_rows))
    return _report(metrics, bootstrap_summary, comparison, ranges, failures)


def _figure(out, comparison, support):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    labels = ['original', *[f'repeat-{seed}' for seed in REPEAT_SEEDS]]
    for model in MODELS:
        values = comparison[comparison.model == model].set_index('assignment').reindex(labels)
        axes[0].plot(range(len(labels)), values.macro_f1, marker='o', label=model)
    axes[0].set_xticks(range(len(labels)), ['Original', *map(str, REPEAT_SEEDS)], rotation=20)
    axes[0].set_ylabel('Pooled fixed-four-class macro F1'); axes[0].set_ylim(0, 1)
    axes[0].legend(fontsize=8)
    for i, assignment in enumerate(labels):
        fusion = support[(support.assignment == assignment) & (support['class'] == 'F')]
        axes[1].scatter(fusion.test_beats, fusion.capped_training_beats, label=assignment.replace('repeat-', ''))
        for row in fusion.itertuples():
            axes[1].annotate(str(row.fold), (row.test_beats, row.capped_training_beats), fontsize=7)
    axes[1].set_xlabel('F beats held out in fold'); axes[1].set_ylabel('F beats in capped training set')
    axes[1].set_title('Rare-group support; point labels identify folds'); axes[1].legend(fontsize=8)
    fig.suptitle('Exploratory split sensitivity • dependent reuse of 43 historic patient groups')
    fig.tight_layout(); fig.savefig(out / 'followup-split-sensitivity.png'); plt.close(fig)


def _report(metrics, bootstrap_summary, comparison, ranges, failures):
    display = lambda value: 'undefined' if value is None else f'{value:.3f}'
    classes = markdown_table(['Method', 'Class', 'True support', 'Predicted count', 'Precision', 'Recall'],
        [[model, row['class'], row['support'], row['predicted'], display(row['precision']), display(row['recall'])]
         for model in MODELS for row in metrics[model]['per_class']])
    bootstrap = markdown_table(['Method or paired contrast', 'Metric', '2.5th percentile', 'Median', '97.5th percentile'],
        [[row['method_or_contrast'], row['metric'], *[f"{row[key]:.3f}" for key in ['p2_5', 'p50', 'p97_5']]]
         for row in bootstrap_summary])
    split = markdown_table(['Assignment', 'Method', 'Status', 'Macro F1', 'Accuracy'],
        [[row['assignment'], row['model'], row['status'], display(row['macro_f1']), display(row['accuracy'])]
         for row in comparison])
    range_table = markdown_table(['Method', 'Metric', 'Minimum', 'Maximum', 'Complete assignments / declared'],
        [[row['model'], row['metric'], f"{row['minimum']:.3f}", f"{row['maximum']:.3f}",
          f"{row['completed_assignments']} / {row['declared_assignments']}"] for row in ranges])
    failure_text = (f"**Incomplete: {len(failures)} fold fit(s) failed.** All failures are retained in "
                    '[follow-up status](followup-status.json); affected pooled repeat scores are undefined.'
                    if failures else 'All three additional assignments completed all five folds.')
    return f'''
## Exploratory follow-up: patient composition and split sensitivity

Declared after seeing the original results, these additions preserve the original
comparison. The full precision/recall table makes both missed groups and groups
the model never predicts visible; undefined values are retained.

{classes}

### Resampling the original saved predictions

The {BOOTSTRAP_REPLICATES:,} patient-cluster bootstrap draws (seed {BOOTSTRAP_SEED}) each sample all 43
patient groups with replacement, retaining each sampled person's beats together.
The same draw feeds every method. Scores pool the sampled confusion counts and
average F1 across the same four classes, using zero when its denominator is zero.
The forest-minus-logistic contrast is paired within each draw.

{bootstrap}

These empirical percentiles describe patient-composition variation conditional
on the fixed saved predictions. They omit training uncertainty and are neither
independent fold replications, population confidence guarantees nor clinical
validation. Audit the [sampled patient indices](followup-bootstrap-draws.csv.gz),
[patient confusion counts](followup-patient-confusions.csv.gz),
[replicate confusion counts](followup-bootstrap-confusions.csv.gz),
[replicate metrics and paired differences](followup-bootstrap-replicates.csv.gz),
and [percentiles](followup-bootstrap-summary.csv.gz).

### Three additional patient assignments

Sorted patient strings are permuted with seeds 20261110, 20261111 and 20261112,
then assigned by permutation position modulo five. Every person is held out once
per completed repeat; both recordings from the shared person remain together.
The original fitting functions, 1,000-beat-per-person training cap and model seeds
remain fixed. Changed membership also changes the capped sampling RNG traversal
and the fold-specific model seed assigned to a person. This is whole-procedure
split sensitivity, not an isolated causal fold effect.

{failure_text}

{split}

The descriptive ranges below include the original and every complete new
assignment. These are dependent reuses of the same historic people, not
independent trials or a p-value for superiority. No repeat is selected as best.

{range_table}

![Split scores and rare-class training/test support](followup-split-sensitivity.png)

The figure shows the same 43 patient groups under four assignments; its support
panel reports F-class counts after the training cap and before held-out scoring.
See [pooled and fold scores](followup-scores.csv.gz),
[pooled and fold class precision/recall/support](followup-class-scores.csv.gz),
[fold training/test support](followup-fold-support.csv.gz),
[all-assignment comparison](followup-split-comparison.csv.gz) and
[descriptive ranges](followup-split-ranges.csv.gz). Every repeat retains its own
mapping, prediction rows, capped training membership, model audit and metrics:

''' + '\n'.join(
        f"- Seed {seed}: [mapping](followup-repeat-{seed}-mapping.json), "
        f"[predictions](followup-repeat-{seed}-predictions.csv.gz), "
        f"[training membership](followup-repeat-{seed}-training-membership.csv.gz), "
        f"[model audit](followup-repeat-{seed}-model-audit.json), "
        f"[metrics](followup-repeat-{seed}-metrics.json)." for seed in REPEAT_SEEDS) + '\n'
