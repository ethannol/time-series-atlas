import numpy as np
import pandas as pd
import pytest

from tsatlas.followup_simulation import (
    common_band_peak, detection_stream, detection_summary,
    spectral_procedures, spectral_realization, wilson_interval,
)
from tsatlas.spectral import CONDITIONS, frequency_grid, realization
from tsatlas.synthetic import scores, stream


def test_wilson_endpoints_and_no_eligible_trials():
    assert wilson_interval(0, 10) == pytest.approx((0., .2775327998628892))
    assert wilson_interval(10, 10) == pytest.approx((.7224672001371107, 1.))
    assert wilson_interval(5, 10) == pytest.approx((.236593090512564, .763406909487436))
    assert wilson_interval(0, 0) is None
    with pytest.raises(ValueError):
        wilson_interval(1, 0)


def test_first_alarm_partitions_keep_overall_and_conditional_denominators():
    frame = pd.DataFrame({'rho': 0., 'shift_magnitude': 1., 'method': 'cusum',
                          'alarm': [150., 200., 230., np.nan]})
    row = detection_summary(frame)[0]
    assert (row['prechange_alarms'], row['eligible'], row['detections'], row['misses']) == (1, 3, 2, 1)
    assert row['overall_detection_rate'] == .5
    assert row['eligible_detection_rate'] == 2 / 3
    assert row['median_detected_delay'] == 15
    assert row['overall_detection_rate_wilson_lower'] == wilson_interval(2, 4)[0]
    assert row['eligible_detection_rate_wilson_lower'] == wilson_interval(2, 3)[0]
    early_only = detection_summary(frame.iloc[:1])[0]
    assert early_only['eligible_detection_rate'] is None
    assert early_only['eligible_detection_rate_wilson_lower'] is None
    assert early_only['median_detected_delay'] is None
    no_change = detection_summary(frame.assign(shift_magnitude=0.))[0]
    assert no_change['false_alarms'] == 3
    assert no_change['false_alarm_rate'] == .75
    assert 'detections' not in no_change


def test_detection_shift_starts_at_200_without_changing_the_random_draw():
    rng = np.random.default_rng(47)
    reference_rng = np.random.default_rng(47)
    changed = detection_stream(rng, .6, 2.)
    unchanged = stream(reference_rng, rho=.6, shift=False)
    np.testing.assert_array_equal(changed[:200], unchanged[:200])
    np.testing.assert_array_equal(changed[200:], unchanged[200:] + 2.)
    assert rng.random() == reference_rng.random()


def test_future_observations_cannot_change_past_detector_scores():
    values = stream(np.random.default_rng(93), rho=.3)
    changed_future = values.copy()
    changed_future[250:] += 100.
    original_scores, future_scores = scores(values), scores(changed_future)
    for method in original_scores:
        # Score index 149 corresponds to stream index 249, before the intervention.
        np.testing.assert_array_equal(original_scores[method][:150], future_scores[method][:150])


def test_common_band_is_inclusive_uses_native_bins_and_rejects_empty_band():
    frequencies = np.array([.009, .01, .2, .45, .451])
    power = np.array([100., 5., 2., 5., 100.])
    before = power.copy()
    assert common_band_peak(frequencies, power) == (.01, 2)
    np.testing.assert_array_equal(power, before)
    assert common_band_peak(np.array([.017, .451]), np.array([3., 100.])) == (.017, 1)
    with pytest.raises(ValueError, match='No native FFT bins'):
        common_band_peak(np.array([.009, .451]), np.array([1., 2.]))


@pytest.mark.parametrize('condition', CONDITIONS)
def test_parameterized_spectral_generator_preserves_original_default_draws(condition):
    rng = np.random.default_rng(13)
    reference_rng = np.random.default_rng(13)
    time, values = spectral_realization(rng, condition, .17, .5)
    reference_time, reference_values = realization(reference_rng, condition)
    np.testing.assert_array_equal(time, reference_time)
    np.testing.assert_array_equal(values, reference_values)
    assert rng.random() == reference_rng.random()


def test_irregular_generation_draws_phase_schedule_then_actual_time_noise():
    class ScriptedRng:
        def __init__(self):
            self.calls = []

        def uniform(self, low, high, size=None):
            self.calls.append(('uniform', low, high, size))
            return .7 if size is None else np.array([-.2, .1, .3])

        def random(self, size):
            self.calls.append(('random', size))
            retention = np.ones(size)
            retention[[0, 100, 477]] = 0.
            return retention

        def normal(self, mean, sd, size):
            self.calls.append(('normal', mean, sd, size))
            return np.arange(size) / 10

    rng = ScriptedRng()
    time, values = spectral_realization(rng, 'irregular', .08325, 1.)
    expected_time = np.array([0., .8, 101.1, 478.3, 479.])
    np.testing.assert_allclose(time, expected_time)
    np.testing.assert_allclose(values, np.sin(2 * np.pi * .08325 * expected_time + .7) + np.arange(5) / 10)
    assert rng.calls == [('uniform', 0, 2 * np.pi, None), ('random', 478),
                         ('uniform', -.4, .4, 3), ('normal', 0, 1., 5)]


def test_five_procedures_keep_the_original_grid_for_off_grid_truth():
    grid = frequency_grid()
    before = grid.copy()
    assert len(grid) == 2403
    assert np.min(abs(grid - .08325)) > 1e-6
    time = np.arange(480, dtype=float)
    values = np.sin(2 * np.pi * .08325 * time + .4)
    rows = spectral_procedures(time, values, .08325, grid)
    np.testing.assert_array_equal(grid, before)
    by_method = {row['method']: row for row in rows}
    assert len(by_method) == 5
    assert by_method['lomb_scargle']['peak_hz'] in grid
    for method in ('index_fft', 'interpolated_fft'):
        assert by_method[method + '_common_band']['peak_hz'] == by_method[method]['peak_hz']
