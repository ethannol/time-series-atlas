"""Finite, post-publication sensitivity checks for the synthetic studies.

These functions write only ``followup-*`` artifacts. Original in-memory inputs,
results, calibration thresholds and the original procedures remain unchanged.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .common import markdown_table, plt, save_frame
from .data import write_json

DETECTION_SEED = 20261113
DETECTION_RHOS = (0., .3, .6, .9)
DETECTION_SHIFTS = (0., .5, 1., 2.)
DETECTION_REPLICATES = 200
SPECTRAL_SEED = 20261114
SPECTRAL_TRUTHS = (.08325, .17, .28725)
SPECTRAL_NOISE = (.5, 1.)
SPECTRAL_REPLICATES = 50
COMMON_BAND = (.01, .45)
WILSON_Z = 1.959963984540054


def wilson_interval(successes: int, total: int) -> tuple[float, float] | None:
    """Pointwise 95% Wilson interval; no eligible trials means undefined."""
    if total < 0 or successes < 0 or successes > total:
        raise ValueError('Binomial counts must satisfy 0 <= successes <= total')
    if total == 0:
        return None
    proportion = successes / total
    z2 = WILSON_Z ** 2
    denominator = 1 + z2 / total
    center = (proportion + z2 / (2 * total)) / denominator
    half_width = WILSON_Z * np.sqrt(proportion * (1 - proportion) / total
                                   + z2 / (4 * total ** 2)) / denominator
    # Exact endpoint conventions avoid roundoff such as a tiny negative lower bound.
    return (0. if successes == 0 else float(center - half_width),
            1. if successes == total else float(center + half_width))


def _rate_fields(name: str, successes: int, total: int) -> dict:
    interval = wilson_interval(successes, total)
    return {name: successes / total if total else None,
            name + '_denominator': total,
            name + '_wilson_lower': interval[0] if interval else None,
            name + '_wilson_upper': interval[1] if interval else None}


def _rate_text(row: dict, name: str) -> str:
    if row.get(name) is None:
        return 'undefined'
    return (f"{row[name]:.1%} [{row[name + '_wilson_lower']:.1%}, "
            f"{row[name + '_wilson_upper']:.1%}]")


def detection_stream(rng, rho: float, shift_magnitude: float) -> np.ndarray:
    """Draw the original no-change process, then add the declared index-200 shift."""
    from .synthetic import stream

    values = stream(rng, rho=rho, shift=False)
    values[200:] += shift_magnitude
    return values


def detection_summary(frame: pd.DataFrame) -> list[dict]:
    """Partition first alarms without restarting streams after early alarms."""
    rows = []
    for (rho, magnitude, method), group in frame.groupby(
            ['rho', 'shift_magnitude', 'method'], sort=False):
        alarms = group.alarm.to_numpy(dtype=float)
        if np.any(np.isfinite(alarms) & ((alarms < 100) | (alarms >= 400))):
            raise ValueError('First alarms must be monitored indices 100 through 399')
        if np.isinf(alarms).any():
            raise ValueError('No alarm must be represented by a missing value')
        n = len(alarms)
        early = int((alarms < 200).sum())
        late = int((alarms >= 200).sum())
        absent = int(np.isnan(alarms).sum())
        eligible = n - early
        row = {'rho': float(rho), 'shift_magnitude': float(magnitude),
               'method': method, 'n': n, 'prechange_alarms': early,
               'postchange_alarms': late, 'no_alarms': absent, 'eligible': eligible,
               'changed_stream': bool(magnitude > 0)}
        row.update(_rate_fields('prechange_alarm_rate', early, n))
        if magnitude == 0:
            # Index 200 only marks a reference boundary here; no change occurred.
            row.update(false_alarms=early + late)
            row.update(_rate_fields('false_alarm_rate', early + late, n))
        else:
            delays = alarms[alarms >= 200] - 200
            row.update(detections=late, misses=absent,
                       median_detected_delay=float(np.median(delays)) if late else None)
            row.update(_rate_fields('overall_detection_rate', late, n))
            row.update(_rate_fields('eligible_detection_rate', late, eligible))
            row.update(_rate_fields('overall_miss_rate', absent, n))
            row.update(_rate_fields('eligible_miss_rate', absent, eligible))
        assert early + late + absent == n
        rows.append(row)
    return rows


def _detection_plot(rows: list[dict], out: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, sharey=True)
    for i, method in enumerate(('shewhart', 'cusum')):
        for j, metric in enumerate(('overall_detection_rate', 'eligible_detection_rate')):
            values = np.full((len(DETECTION_RHOS), len(DETECTION_SHIFTS) - 1), np.nan)
            for ri, rho in enumerate(DETECTION_RHOS):
                for si, shift in enumerate(DETECTION_SHIFTS[1:]):
                    row = next(r for r in rows if r['method'] == method
                               and r['rho'] == rho and r['shift_magnitude'] == shift)
                    if row[metric] is not None:
                        values[ri, si] = row[metric]
                    denominator = row[metric + '_denominator']
                    axes[i, j].text(si, ri, f"{row['detections']}/{denominator}",
                                    ha='center', va='center', fontsize=10,
                                    color='white' if values[ri, si] > .55 else 'black')
            im = axes[i, j].imshow(values, vmin=0, vmax=1, cmap='Blues', aspect='auto')
            axes[i, j].set(title=f"{method}: {'overall' if j == 0 else 'eligible conditional'}",
                           xticks=range(3), xticklabels=DETECTION_SHIFTS[1:],
                           yticks=range(4), yticklabels=DETECTION_RHOS)
            if i == 1:
                axes[i, j].set_xlabel('Shift magnitude (marginal SD units)')
            if j == 0:
                axes[i, j].set_ylabel('AR(1) rho')
    fig.suptitle('Postchange first alarms: count / stated denominator\n'
                 'Fixed calibration; finite exploratory grid; no restart after an early alarm', fontsize=11)
    fig.tight_layout(rect=(0, .06, 1, .93))
    fig.colorbar(im, ax=axes, location='bottom', fraction=.035, pad=.09,
                 label='Detection fraction (pointwise intervals in linked tables)')
    fig.savefig(out / 'followup-detection-grid.png')
    plt.close(fig)


def detection_followup(out: Path, thresholds: dict, original_frame: pd.DataFrame) -> str:
    """Run the frozen 16-cell detection grid and return a report section."""
    from .synthetic import first_alarm, scores

    rng = np.random.default_rng(DETECTION_SEED)
    rows = []
    realization_id = 0
    for rho in DETECTION_RHOS:
        for magnitude in DETECTION_SHIFTS:
            for replicate in range(DETECTION_REPLICATES):
                values = detection_stream(rng, rho, magnitude)
                for method, score in scores(values).items():
                    rows.append({'realization_id': realization_id, 'rho': rho,
                                 'shift_magnitude': magnitude, 'replicate': replicate,
                                 'method': method, 'alarm': first_alarm(score, thresholds[method])})
                realization_id += 1
    frame = pd.DataFrame(rows)
    summaries = detection_summary(frame)
    original = original_frame.copy()
    original['shift_magnitude'] = original['shift'].astype(float)
    original_summaries = detection_summary(original)
    save_frame(frame, out / 'followup-replicates.csv.gz')
    pd.DataFrame(summaries).to_csv(out / 'followup-summary.csv', index=False)
    pd.DataFrame(original_summaries).to_csv(out / 'followup-original-summary.csv', index=False)
    configuration = {
        'status': 'post-publication exploratory follow-up', 'seed': DETECTION_SEED,
        'rho_grid': list(DETECTION_RHOS), 'shift_magnitude_grid': list(DETECTION_SHIFTS),
        'replicates_per_cell': DETECTION_REPLICATES, 'realizations': realization_id,
        'loop_order': ['rho', 'shift_magnitude', 'replicate'],
        'generator': 'original synthetic.stream(rng, rho, shift=False); add magnitude at indices 200:400',
        'stream_length': 400, 'baseline_indices': [0, 99], 'monitoring_indices': [100, 399],
        'change_index': 200, 'thresholds': dict(thresholds), 'recalibrated': False,
        'first_alarm_only': True, 'restart_after_early_alarm': False,
        'interval': 'pointwise 95% Wilson, independent stream unit, conditional on frozen calibration',
        'wilson_z': WILSON_Z,
    }
    write_json(out / 'followup-metrics.json', {'configuration': configuration,
                                            'grid': summaries, 'original': original_summaries})
    _detection_plot(summaries, out)
    report = ('\n## Exploratory follow-up: dependence and shift grid\n\n'
              'This finite comparison was declared after the original results. The original '
              'calibration thresholds, standardization, first-alarm rule and no-restart policy '
              'remain fixed. Each cell uses 200 independently generated streams; both methods '
              'receive the same stream. The grid cannot establish smoothness between tested values.\n\n'
              '![Finite detection grid](followup-detection-grid.png)\n\n'
              'Zero shift means no change: every alarm is false, including those after index 200. '
              'The early count uses indices 100–199 only.\n\n')
    report += markdown_table(
        ['Method', 'rho', 'False alarms / 200', 'False-alarm fraction [95% Wilson]', 'Early / 200'],
        [[r['method'], r['rho'], r['false_alarms'], _rate_text(r, 'false_alarm_rate'),
          r['prechange_alarms']] for r in summaries if not r['changed_stream']])
    report += ('\nFor changed streams, overall detection divides postchange first alarms by 200. '
               'Conditional detection divides by the eligible count after removing early alarms. '
               'A miss has no alarm by index 399; an early false alarm is a separate outcome. '
               'Median delay includes detected streams only, so it is undefined without a detection.\n\n')
    report += markdown_table(
        ['Method', 'rho', 'Shift', 'Early / 200', 'Eligible', 'Detected / 200',
         'Overall fraction [95% Wilson]', 'Conditional fraction [95% Wilson]',
         'No-alarm misses', 'Median detected delay'],
        [[r['method'], r['rho'], r['shift_magnitude'], r['prechange_alarms'], r['eligible'],
          r['detections'], _rate_text(r, 'overall_detection_rate'),
          _rate_text(r, 'eligible_detection_rate'), r['misses'],
          r['median_detected_delay'] if r['median_detected_delay'] is not None else 'undefined']
         for r in summaries if r['changed_stream']])
    report += '\nThe original changed-stream results also have these overall denominators:\n\n'
    report += markdown_table(
        ['Method', 'rho', 'Early / 200', 'Eligible', 'Detected / 200',
         'Overall fraction [95% Wilson]', 'Median detected delay'],
        [[r['method'], r['rho'], r['prechange_alarms'], r['eligible'], r['detections'],
          _rate_text(r, 'overall_detection_rate'),
          r['median_detected_delay'] if r['median_detected_delay'] is not None else 'undefined']
         for r in original_summaries if r['changed_stream']])
    report += ('\nIntervals describe pointwise Monte Carlo variation conditional on the frozen '
               'calibration, not simultaneous coverage across cells or calibration uncertainty. '
               'Method outcomes are paired within streams; marginal Wilson intervals are not '
               'paired inference about method differences. The '
               '[complete cell table](followup-summary.csv) includes early-alarm and miss '
               'proportions, denominators and intervals; [every first alarm](followup-replicates.csv.gz), '
               '[original denominator audit](followup-original-summary.csv) and '
               '[fixed configuration and metrics](followup-metrics.json) are retained.\n')
    return report


def common_band_peak(frequencies, power) -> tuple[float, int]:
    """Select only native FFT bins in the inclusive band; do not move bins."""
    from .spectral import peak

    frequencies = np.asarray(frequencies)
    power = np.asarray(power)
    if frequencies.ndim != 1 or frequencies.shape != power.shape:
        raise ValueError('Frequency and power arrays must be matching vectors')
    if not np.isfinite(frequencies).all():
        raise ValueError('Non-finite frequency')
    included = (frequencies >= COMMON_BAND[0]) & (frequencies <= COMMON_BAND[1])
    if not included.any():
        raise ValueError('No native FFT bins in the inclusive common band')
    return peak(frequencies[included], power[included])


def spectral_realization(rng, condition: str, truth_hz: float, noise_sd: float):
    """Preserve the original phase -> schedule -> actual-time noise draw order."""
    phase = rng.uniform(0, 2 * np.pi)
    if condition == 'regular':
        time = np.arange(480, dtype=float)
    elif condition == 'irregular':
        interior = np.arange(1, 479)[rng.random(478) < .4].astype(float)
        time = np.r_[0., interior + rng.uniform(-.4, .4, len(interior)), 479.]
    elif condition == 'every_three_seconds':
        time = np.arange(0, 480, 3, dtype=float)
    else:
        raise ValueError(condition)
    values = np.sin(2 * np.pi * truth_hz * time + phase) + rng.normal(0, noise_sd, len(time))
    return time, values


def _spectral_result(method: str, estimate: float, ties: int, truth_hz: float) -> dict:
    from .spectral import TOLERANCE

    error = abs(estimate - truth_hz)
    return {'method': method, 'peak_hz': estimate, 'absolute_error_hz': error,
            'recovered': error <= TOLERANCE, 'tied_peak_count': ties}


def spectral_procedures(time, values, truth_hz: float, grid) -> list[dict]:
    """Five paired procedures, using exactly the supplied fixed LS grid."""
    from .spectral import peak, spectra

    computed = spectra(time, values, grid)
    rows = []
    for method, (frequencies, power) in computed.items():
        estimate, ties = peak(frequencies, power, 1e-10 if method == 'lomb_scargle' else 0.)
        rows.append(_spectral_result(method, estimate, ties, truth_hz))
    for method in ('index_fft', 'interpolated_fft'):
        estimate, ties = common_band_peak(*computed[method])
        rows.append(_spectral_result(method + '_common_band', estimate, ties, truth_hz))
    return rows


def spectral_summary(frame: pd.DataFrame) -> list[dict]:
    rows = []
    for (truth, noise, condition, method), group in frame.groupby(
            ['truth_hz', 'noise_sd', 'condition', 'method'], sort=False):
        row = {'truth_hz': float(truth), 'noise_sd': float(noise),
               'condition': condition, 'method': method, 'replicates': len(group),
               'recovered': int(group.recovered.sum()),
               'median_absolute_error_hz': float(group.absolute_error_hz.median()),
               'numerically_tied_peak_replicates': int((group.tied_peak_count > 1).sum()),
               'analytically_ambiguous_realizations': int(group.analytically_ambiguous_sampling.sum())}
        row.update(_rate_fields('recovery_fraction', row['recovered'], len(group)))
        rows.append(row)
    return rows


def _spectral_table(rows: list[dict]) -> str:
    return markdown_table(
        ['Sampling', 'Procedure', 'Recovered / trials', 'Fraction [95% Wilson]',
         'Median absolute error (Hz)', 'Numerical ties / trials', 'Analytic ambiguity / trials'],
        [[r['condition'], r['method'], f"{r['recovered']} / {r['replicates']}",
          _rate_text(r, 'recovery_fraction'), f"{r['median_absolute_error_hz']:.5f}",
          r['numerically_tied_peak_replicates'], r['analytically_ambiguous_realizations']] for r in rows])


def _spectral_plot(rows: list[dict], methods: tuple[str, ...], conditions, out: Path) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(12, 10), sharex=True, sharey=True)
    colors = ('#666666', '#cf8a25', '#167a8a', '#a5a5a5', '#f1c77d')
    for i, truth in enumerate(SPECTRAL_TRUTHS):
        for j, noise in enumerate(SPECTRAL_NOISE):
            ax = axes[i, j]
            for k, method in enumerate(methods):
                selected = [next(r for r in rows if r['truth_hz'] == truth and r['noise_sd'] == noise
                                 and r['condition'] == condition and r['method'] == method)
                            for condition in conditions]
                ax.bar(np.arange(3) + (k - 2) * .15,
                       [r['recovery_fraction'] for r in selected], width=.15,
                       color=colors[k], label=method.replace('_', ' '))
            ax.set(title=f'Truth {truth:g} Hz; noise SD {noise:g}', ylim=(0, 1.08),
                   xticks=range(3), xticklabels=['Regular 1 s', 'Irregular', 'Regular 3 s*'])
            if j == 0:
                ax.set_ylabel('Recovered fraction / 50 trials')
    fig.suptitle('Fixed exploratory frequency/noise grid\n'
                 '*Three-second sampling is analytically ambiguous, regardless of recovery', fontsize=12)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=3, fontsize=9)
    fig.tight_layout(rect=(0, .07, 1, .94))
    fig.savefig(out / 'followup-spectral-grid.png')
    plt.close(fig)


def spectral_followup(out: Path, original_inputs, original_results) -> str:
    """Add paired common-band peaks and the declared 900-realization fixed grid.

    Inputs may be the original concatenated DataFrame or list of input frames;
    results may be the original result DataFrame or list of result dictionaries.
    """
    from .spectral import CONDITIONS, METHODS, TOLERANCE, TRUTH, frequency_grid, spectra

    data = (original_inputs.copy() if isinstance(original_inputs, pd.DataFrame)
            else pd.concat(original_inputs, ignore_index=True))
    original = pd.DataFrame(original_results).copy()
    input_keys = set(map(tuple, data[['condition', 'replicate']].drop_duplicates().to_numpy()))
    result_keys = set(map(tuple, original[['condition', 'replicate']].drop_duplicates().to_numpy()))
    if input_keys != result_keys:
        raise ValueError('Original spectral input/result realization keys differ')
    if original.duplicated(['condition', 'replicate', 'method']).any():
        raise ValueError('Duplicate original spectral procedure result')
    for _, group in original.groupby(['condition', 'replicate'], sort=False):
        if set(group.method) != set(METHODS):
            raise ValueError('Original realization is missing a spectral procedure')
    grid = frequency_grid()
    matched_rows = []
    for (condition, replicate), group in data.groupby(['condition', 'replicate'], sort=False):
        time = group.time_seconds.to_numpy()
        values = group.value.to_numpy()
        computed = spectra(time, values, grid)
        for method in ('index_fft', 'interpolated_fft'):
            estimate, ties = common_band_peak(*computed[method])
            matched_rows.append({'condition': condition, 'replicate': int(replicate),
                                 **_spectral_result(method + '_common_band', estimate, ties, TRUTH)})
    matched = pd.concat([original, pd.DataFrame(matched_rows)], ignore_index=True)
    matched['truth_hz'] = TRUTH
    matched['noise_sd'] = .5
    matched['analytically_ambiguous_sampling'] = matched.condition == 'every_three_seconds'
    matched_summary = spectral_summary(matched)
    save_frame(matched, out / 'followup-matched-band-replicates.csv.gz')
    pd.DataFrame(matched_summary).to_csv(out / 'followup-matched-band-summary.csv', index=False)

    rng = np.random.default_rng(SPECTRAL_SEED)
    rows, inputs = [], []
    realization_id = 0
    for truth in SPECTRAL_TRUTHS:
        for noise in SPECTRAL_NOISE:
            for condition in CONDITIONS:
                for replicate in range(SPECTRAL_REPLICATES):
                    time, values = spectral_realization(rng, condition, truth, noise)
                    identifiers = {'realization_id': realization_id, 'truth_hz': truth,
                                   'noise_sd': noise, 'condition': condition, 'replicate': replicate}
                    inputs.append(pd.DataFrame({**identifiers, 'time_seconds': time, 'value': values}))
                    for result in spectral_procedures(time, values, truth, grid):
                        rows.append({**identifiers, **result, 'samples': len(time),
                                     'span_seconds': float(time[-1] - time[0]),
                                     'analytically_ambiguous_sampling': condition == 'every_three_seconds'})
                    realization_id += 1
    robust = pd.DataFrame(rows)
    robust_summary = spectral_summary(robust)
    save_frame(pd.concat(inputs, ignore_index=True), out / 'followup-robustness-inputs.csv.gz')
    save_frame(robust, out / 'followup-robustness-replicates.csv.gz')
    pd.DataFrame(robust_summary).to_csv(out / 'followup-robustness-summary.csv', index=False)
    methods = (*METHODS, 'index_fft_common_band', 'interpolated_fft_common_band')
    configuration = {
        'status': 'post-publication exploratory follow-up', 'seed': SPECTRAL_SEED,
        'truth_grid_hz': list(SPECTRAL_TRUTHS), 'noise_sd_grid': list(SPECTRAL_NOISE),
        'sampling_schedules': list(CONDITIONS), 'procedures': list(methods),
        'replicates_per_cell': SPECTRAL_REPLICATES, 'new_realizations': realization_id,
        'loop_order': ['truth_hz', 'noise_sd', 'condition', 'replicate'],
        'draw_order': ['phase', 'schedule retention and jitter if irregular', 'noise at actual sampled times'],
        'matched_band_hz_inclusive': list(COMMON_BAND),
        'fft_bins_changed': False, 'frequency_grid_hz': grid.tolist(),
        'frequency_grid_points': len(grid), 'new_truth_values_added_to_grid': False,
        'recovery_tolerance_hz': TOLERANCE, 'lomb_scargle_tie_tolerance': 1e-10,
        'tie_break': 'lowest frequency', 'original_realizations': len(input_keys),
        'interval': 'pointwise 95% Wilson; marginal procedure rates, not paired difference intervals',
        'wilson_z': WILSON_Z,
    }
    write_json(out / 'followup-metrics.json', {'configuration': configuration,
                                            'matched_band': matched_summary,
                                            'robustness_grid': robust_summary})
    table_report = ('# Exploratory spectral robustness: every declared cell\n\n'
                    'Each procedure has 50 trials per cell; all five procedures use the same '
                    'realizations. Intervals are pointwise marginal 95% Wilson intervals, not '
                    'simultaneous bands or paired tests of differences. The 2,403-point LS grid '
                    'is unchanged. A common band does not align native FFT and LS bins. '
                    'Regular three-second sampling is analytically ambiguous regardless of '
                    'numerical ties or whether the lowest-frequency peak recovers the truth.\n\n')
    for truth in SPECTRAL_TRUTHS:
        for noise in SPECTRAL_NOISE:
            table_report += f'## Truth {truth:g} Hz, noise SD {noise:g}\n\n'
            table_report += _spectral_table([r for r in robust_summary
                                            if r['truth_hz'] == truth and r['noise_sd'] == noise]) + '\n'
    (out / 'followup-robustness-tables.md').write_text(table_report)
    _spectral_plot(robust_summary, methods, CONDITIONS, out)
    report = ('\n## Exploratory follow-up: common band and signal settings\n\n'
              'These comparisons were declared after seeing the original results. First, the '
              'two added FFT procedures select native peaks only within 0.01–0.45 Hz inclusive '
              'on the original realizations. The three original procedure results are retained. '
              '**A common search band does not align frequency bins or isolate timestamp handling:** '
              'spacing assumptions, interpolation and frequency grids still differ.\n\n')
    report += _spectral_table(matched_summary)
    report += ('\nThe second comparison uses all 18 declared frequency/noise/sampling cells, '
               '50 independent realizations per cell (900 total), and the same five procedures '
               'on each realization. The original 2,403-point Lomb–Scargle grid and 1/480 Hz '
               'recovery tolerance are unchanged; the new off-grid truths are not inserted. '
               'Phase, retention/jitter and noise are drawn in the declared order, with noise '
               'at actual observation times.\n\n'
               '![All fixed spectral grid cells](followup-spectral-grid.png)\n\n'
               '[Every cell with counts, errors and pointwise 95% Wilson intervals]'
               '(followup-robustness-tables.md) is retained, including poor recovery. '
               'Intervals describe Monte Carlo variation of each procedure separately. '
               'The paired procedure outcomes are dependent, so these marginal intervals do '
               'not provide paired inference about a difference or simultaneous coverage.\n\n'
               'Regular three-second sampling retains analytic alias ambiguity at every tested '
               'frequency and noise level. Even when numerical maxima are not tied, or the '
               'lowest-frequency rule selects the planted truth, recovery does not demonstrate '
               'unique physical identification. Numerical tie counts and analytic ambiguity '
               'are therefore recorded separately. No universal method ranking follows.\n\n'
               '[Original-realization paired results](followup-matched-band-replicates.csv.gz) · '
               '[Matched-band summary](followup-matched-band-summary.csv) · '
               '[New actual-time inputs](followup-robustness-inputs.csv.gz) · '
               '[New paired results](followup-robustness-replicates.csv.gz) · '
               '[Every new cell](followup-robustness-summary.csv) · '
               '[Fixed grid, seeds and metrics](followup-metrics.json).\n')
    return report
