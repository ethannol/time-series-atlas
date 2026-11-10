import json

import numpy as np
import pandas as pd
import pytest

from tsatlas.ecg import CLASSES, MODELS, classification_scores, fold_indices
from tsatlas import followup_ecg as followup


def test_patient_bootstrap_keeps_cluster_multiplicity_and_pairs_all_methods():
    counts = np.zeros((2, 4, 4, 4), dtype=int)
    # Unequal patient sizes distinguish pooled confusion scoring from patient averaging.
    counts[0, :, 0, 0] = 9
    counts[1, :, 1, 0] = 1
    counts[1, 3, 1, 0] = 0
    counts[1, 3, 1, 1] = 1
    draws = np.array([[0, 0], [0, 1], [1, 1]])
    result = followup.bootstrap_confusions(counts, draws)
    np.testing.assert_array_equal(result[0], 2 * counts[0])
    np.testing.assert_array_equal(result[1], counts[0] + counts[1])
    np.testing.assert_array_equal(result[2], 2 * counts[1])
    scores = followup.confusion_metrics(result)
    assert scores['n'][:, 0].tolist() == [18, 10, 2]
    assert scores['accuracy'][1, 2] == .9
    assert scores['accuracy'][1, 3] == 1.
    assert scores['macro_f1'][0, 0] == .25  # Other fixed classes receive zero F1.
    assert scores['macro_f1'][1, 3] - scores['macro_f1'][1, 2] == pytest.approx(.5 - 18 / 19 / 4)


def test_confusion_metrics_match_direct_scoring_with_missing_class():
    direct = classification_scores(['N', 'N', 'S', 'V'], ['N', 'S', 'S', 'N'])
    scores = followup.confusion_metrics(np.array(direct['confusion']))
    assert scores['accuracy'] == direct['accuracy']
    assert scores['macro_f1'] == direct['macro_f1']
    with pytest.raises(ValueError, match='empty'):
        followup.confusion_metrics(np.zeros((4, 4), dtype=int))


def test_assignments_sort_strings_and_preserve_shared_people_and_complete_coverage():
    people = [str(100 + i) for i in range(43)]
    beats = np.array([(person, person) for person in people] + [('202', '101')],
                     dtype=[('record', 'U3'), ('person', 'U3')])
    for seed in followup.REPEAT_SEEDS:
        mapping = followup.patient_fold_mapping(reversed(people), seed)
        permutation = np.random.default_rng(seed).permutation(sorted(people))
        assert mapping == {person: i % 5 for i, person in enumerate(permutation)}
        assert sorted(np.bincount(list(mapping.values())).tolist()) == [8, 8, 9, 9, 9]
        held_out = []
        for fold in range(5):
            train, test = fold_indices(beats, mapping, fold)
            assert not set(beats['person'][train]) & set(beats['person'][test])
            if '101' in beats['person'][test]:
                assert set(beats['record'][test]) >= {'101', '202'}
            held_out.extend(test)
        assert sorted(held_out) == list(range(len(beats)))


def _toy():
    beats = np.array([(str(100 + i), str(100 + i), i, 'N', CLASSES[i % 4]) for i in range(43)],
                     dtype=[('record', 'U3'), ('person', 'U3'), ('sample', 'i8'), ('symbol', 'U1'), ('label', 'U1')])
    mapping = followup.patient_fold_mapping(beats['person'], 20261031)
    frames = [pd.DataFrame({'beat_index': np.arange(len(beats)),
                           'fold': [mapping[p] for p in beats['person']],
                           'record': beats['record'], 'person': beats['person'], 'sample': beats['sample'],
                           'symbol': beats['symbol'], 'truth': beats['label'], 'model': model,
                           'prediction': beats['label']}) for model in MODELS]
    predictions = pd.concat(frames, ignore_index=True)
    return beats, mapping, predictions


def test_prediction_guards_reject_missing_duplicate_or_misaligned_models():
    beats, mapping, predictions = _toy()
    followup.validate_predictions(predictions, beats, mapping)
    for broken in [predictions.iloc[1:], pd.concat([predictions, predictions.iloc[:1]])]:
        with pytest.raises(ValueError, match='coverage'):
            followup.validate_predictions(broken, beats, mapping)
    broken = predictions.copy()
    broken.loc[0, 'truth'] = 'V'
    with pytest.raises(ValueError, match='truth'):
        followup.validate_predictions(broken, beats, mapping)
    with pytest.raises(ValueError, match='identical'):
        followup.patient_confusions(broken)


def test_followup_retains_every_attempt_and_exposes_failure_without_partial_pool(tmp_path, monkeypatch):
    beats, mapping, predictions = _toy()
    metrics = {model: classification_scores(group.truth, group.prediction)
               for model, group in predictions.groupby('model')}
    calls = []

    def fake_fit(waves, actual_beats, train, test, fold):
        calls.append((fold, test.copy()))
        if len(calls) == 2:
            raise ValueError('deliberate toy failure')
        result = predictions[predictions.beat_index.isin(test)].copy()
        result['fold'] = fold
        return result, {'fold': fold, 'training_people': sorted(set(actual_beats['person'][train]))}

    monkeypatch.setattr(followup, 'fit_fold', fake_fit)
    monkeypatch.setattr(followup, 'BOOTSTRAP_REPLICATES', 7)
    original = tmp_path / 'metrics.json'
    original.write_text('unchanged original bytes')
    report = followup.ecg_followup(tmp_path, np.zeros((43, 60)), beats, predictions, metrics, mapping)
    assert original.read_text() == 'unchanged original bytes'
    assert len(calls) == 15
    assert 'Incomplete: 1 fold fit(s) failed' in report
    status = json.loads((tmp_path / 'followup-status.json').read_text())
    assert status['status'] == 'incomplete'
    assert status['failures'][0]['error'] == 'deliberate toy failure'
    comparison = pd.read_csv(tmp_path / 'followup-split-comparison.csv.gz')
    assert len(comparison) == 16
    failed = comparison[comparison.assignment == 'repeat-20261110']
    assert set(failed.status) == {'incomplete'}
    assert failed.macro_f1.isna().all()
    assert (comparison[comparison.assignment == 'original'].macro_f1 == 1).all()
    scores = pd.read_csv(tmp_path / 'followup-scores.csv.gz')
    assert not ((scores.assignment == 'repeat-20261110') & (scores.fold == 'pooled')).any()
    for seed in followup.REPEAT_SEEDS:
        membership = pd.read_csv(tmp_path / f'followup-repeat-{seed}-training-membership.csv.gz')
        assert len(membership) == 43 * 4  # Failed folds still preserve training membership.
        saved = pd.read_csv(tmp_path / f'followup-repeat-{seed}-predictions.csv.gz')
        expected = (43 - len(calls[1][1])) * 4 if seed == 20261110 else 43 * 4
        assert len(saved) == expected
    draws = pd.read_csv(tmp_path / 'followup-bootstrap-draws.csv.gz')
    retained = pd.read_csv(tmp_path / 'followup-bootstrap-confusions.csv.gz')
    assert len(draws) == 7 * 43
    assert len(retained) == 7 * 4
    assert set(retained.model) == set(MODELS)
