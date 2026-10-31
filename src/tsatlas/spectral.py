"""Known-truth frequency recovery with explicit sampling ambiguity."""
import numpy as np
import pandas as pd
from scipy.signal import lombscargle
from .common import start_run, finish_run, save_frame, markdown_table, plt
from .data import write_json

TRUTH = .17
ALIAS = 1 / 3 - TRUTH
TOLERANCE = 1 / 480
CONDITIONS = ('regular', 'irregular', 'every_three_seconds')
METHODS = ('index_fft', 'interpolated_fft', 'lomb_scargle')


def frequency_grid():
    base = np.r_[np.linspace(.01, .45, 881), TRUTH]
    family = np.concatenate([np.abs(k / 3 + sign * base)
                             for k in range(-2, 3) for sign in (-1, 1)])
    return np.unique(np.round(family[(family >= .01) & (family <= .45)], 12))


def realization(rng, condition):
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
    values = np.sin(2 * np.pi * TRUTH * time + phase) + rng.normal(0, .5, len(time))
    return time, values


def fft_spectrum(values):
    frequencies = np.fft.rfftfreq(len(values), d=1.)[1:]
    power = np.abs(np.fft.rfft(values - np.mean(values)))[1:] ** 2
    return frequencies, power


def spectra(time, values, grid=None):
    grid = frequency_grid() if grid is None else grid
    integer_time = np.arange(np.ceil(time[0]), np.floor(time[-1]) + 1)
    return {
        'index_fft': fft_spectrum(values),
        'interpolated_fft': fft_spectrum(np.interp(integer_time, time, values)),
        'lomb_scargle': (grid, lombscargle(time, values, 2 * np.pi * grid,
                                          floating_mean=True, normalize=True)),
    }


def peak(frequencies, power, tolerance=0.):
    if not np.isfinite(power).all():
        raise ValueError('Non-finite spectral power')
    tied = frequencies[power >= power.max() - tolerance]
    return float(tied.min()), int(len(tied))


def summarize(frame):
    rows = []
    for (condition, method), group in frame.groupby(['condition', 'method'], sort=False):
        rows.append({'condition': condition, 'method': method, 'replicates': len(group),
                     'median_absolute_error_hz': float(group.absolute_error_hz.median()),
                     'recovered': int(group.recovered.sum()),
                     'recovery_fraction': float(group.recovered.mean()),
                     'ambiguous_grid_peaks': int((group.tied_peak_count > 1).sum())})
    return rows


def run():
    out, started = start_run('spectral')
    rng = np.random.default_rng(20261032)
    grid = frequency_grid()
    rows, inputs, examples, sample_counts = [], [], [], []
    for condition in CONDITIONS:
        for replicate in range(100):
            time, values = realization(rng, condition)
            inputs.append(pd.DataFrame({'condition': condition, 'replicate': replicate,
                                        'time_seconds': time, 'value': values}))
            sample_counts.append({'condition': condition, 'replicate': replicate,
                                  'samples': len(time), 'span_seconds': time[-1] - time[0]})
            for method, (frequencies, power) in spectra(time, values, grid).items():
                estimate, ties = peak(frequencies, power, 1e-10 if method == 'lomb_scargle' else 0.)
                row = {'condition': condition, 'replicate': replicate, 'method': method,
                       'peak_hz': estimate, 'absolute_error_hz': abs(estimate - TRUTH),
                       'recovered': abs(estimate - TRUTH) <= TOLERANCE, 'tied_peak_count': ties}
                if method == 'lomb_scargle':
                    row.update(truth_power=float(power[np.argmin(abs(frequencies - TRUTH))]),
                               alias_power=float(power[np.argmin(abs(frequencies - ALIAS))]))
                rows.append(row)
                if replicate == 0:
                    examples.append(pd.DataFrame({'condition': condition, 'method': method,
                                                   'frequency_hz': frequencies, 'power': power}))
    frame = pd.DataFrame(rows)
    data = pd.concat(inputs, ignore_index=True)
    example = pd.concat(examples, ignore_index=True)
    sampling = pd.DataFrame(sample_counts)
    summaries = summarize(frame)
    save_frame(frame, out / 'replicates.csv.gz')
    save_frame(data, out / 'inputs.csv.gz')
    save_frame(example, out / 'example-spectra.csv.gz')
    sampling.to_csv(out / 'sampling.csv', index=False)
    write_json(out / 'metrics.json', {'truth_hz': TRUTH, 'known_alias_hz': ALIAS,
                                     'recovery_tolerance_hz': TOLERANCE,
                                     'frequency_grid_hz': grid.tolist(), 'summary': summaries})
    labels = ['Regular 1 second', 'Irregular + jitter', 'Regular 3 seconds']
    colors = ['#666666', '#cf8a25', '#167a8a']
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for i, method in enumerate(METHODS):
        selected = [next(r for r in summaries if r['condition'] == c and r['method'] == method)
                    for c in CONDITIONS]
        axes[0].bar(np.arange(3) + (i - 1) * .25,
                    [r['recovery_fraction'] for r in selected], width=.25,
                    label=method.replace('_', ' '), color=colors[i])
    axes[0].set(xticks=np.arange(3), xticklabels=labels, ylim=(0, 1.12),
                ylabel='Fraction within 1/480 Hz of truth', title='Correct frequency under the fixed rule')
    axes[0].tick_params(axis='x', labelsize=8)
    axes[0].legend(fontsize=8)
    ls = frame.query("method == 'lomb_scargle'")
    for i, condition in enumerate(CONDITIONS):
        values = ls[ls.condition == condition].tied_peak_count
        axes[1].scatter(np.full(len(values), i), values, alpha=.25, s=15)
    axes[1].set(xticks=np.arange(3), xticklabels=labels,
                ylabel='Equal-power grid peaks (each replicate)', title='Lomb–Scargle: tied peaks are ambiguous')
    axes[1].tick_params(axis='x', labelsize=8)
    fig.tight_layout(); fig.savefig(out / 'recovery-and-ambiguity.png'); plt.close(fig)
    fig, axes = plt.subplots(3, 2, figsize=(11, 8))
    for i, condition in enumerate(CONDITIONS):
        selected = data[(data.condition == condition) & (data.replicate == 0)]
        axes[i, 0].plot(selected.time_seconds, selected.value, '.-', ms=3, lw=.5)
        axes[i, 0].set(xlim=(0, 60), title=labels[i] + ': first 60 seconds', ylabel='Signal value')
        for j, method in enumerate(METHODS):
            values = example[(example.condition == condition) & (example.method == method)]
            axes[i, 1].plot(values.frequency_hz, values.power / values.power.max(),
                            label=method.replace('_', ' '), color=colors[j], alpha=.8, lw=1)
        axes[i, 1].axvline(TRUTH, color='black', ls=':', label='truth')
        axes[i, 1].axvline(ALIAS, color='purple', ls='--', alpha=.6, label='3-second alias')
        axes[i, 1].set(xlim=(0, .5), ylabel='Power / own maximum')
    axes[0, 1].legend(fontsize=7, ncol=2)
    axes[-1, 0].set_xlabel('Seconds'); axes[-1, 1].set_xlabel('Frequency (Hz; index FFT assumes 1 s/sample)')
    fig.tight_layout(); fig.savefig(out / 'preselected-examples.png'); plt.close(fig)
    report = '# Can a spectral peak survive the sampling schedule?\n\n'
    report += ('With irregular timestamps, Lomb–Scargle recovered the planted frequency in '
               '100 of 100 trials, interpolation plus FFT in 74, and the index FFT in none. '
               'With regular three-second sampling, all 100 Lomb–Scargle trials had two '
               'equal-power peaks. Its lowest-frequency tie rule selected the alias, so '
               'zero counted as recoveries; the data could not uniquely identify the frequency. '
               '**The methods use different search ranges and grids, so this does not isolate '
               'the effect of timestamp handling alone.**\n\n')
    report += ('The experiment compares an index FFT that assumes one second between samples '
               '(correct in the regular control, deliberately wrong for irregular/thinned observations), '
               'linear interpolation followed by FFT, and Lomb–Scargle using actual timestamps. '
               'Known truth is 0.17 Hz; the same noisy observations feed all methods. '
               'This supports the synthetic investigation, not a claim about ECG physiology.\n\n')
    report += markdown_table(['Sampling', 'Method', 'Median absolute error (Hz)', 'Recovered / 100', 'Replicates with tied peaks / 100'],
                             [[r['condition'], r['method'], f"{r['median_absolute_error_hz']:.5f}",
                               r['recovered'], r['ambiguous_grid_peaks']] for r in summaries])
    report += '\n![Recovery and ambiguity](recovery-and-ambiguity.png)\n\n'
    irregular_fft=frame[(frame.condition=='irregular')&(frame.method=='interpolated_fft')]
    below=int((irregular_fft.peak_hz<.01).sum())
    report += (f'Lomb–Scargle searches 0.01–0.45 Hz, whereas both FFT procedures select '
               f'from all positive native bins (up to about 0.5 under their one-second spacing). '
               f'Of the {int((~irregular_fft.recovered).sum())} irregular interpolation failures, '
               f'{below} select peaks below 0.01 Hz, outside the Lomb–Scargle search. '
               'That is a descriptive audit of the original peaks, not an estimate of what '
               'a matched-band FFT would achieve. No matched-band comparison was run or '
               'substituted after seeing results. The spectral plots now show those low frequencies.\n\n')
    report += ('Recovery means within 1/480 Hz of truth. Every-three-second sampling makes '
               '0.17 Hz and 1/3 − 0.17 Hz observationally equivalent. Lomb–Scargle searches '
               'the entire alias family of every candidate; equal maxima select the lowest '
               'frequency. Even if another tie rule selected the true peak, it would not '
               'resolve that ambiguity. Ties refer to numerical grid equality, not a confidence interval. '
               'The FFT grids need not contain both equivalent frequencies: zero exact FFT ties '
               'do not certify identifiability. Lomb–Scargle’s zero median error is also a '
               'discrete-grid result: its grid contains the planted truth, while FFT bins differ. '
               'It does not mean noiseless or infinitely precise estimation.\n\n')
    report += ('The grid was amended before any recovery results: adding only the true '
               'frequency and its alias would not expose aliases of noise-shifted maxima. '
               'The expanded grid prevents a numerical search choice from posing as identification.\n\n')
    sampling_rows=[]
    alias_rows=[]
    for condition in CONDITIONS:
        s=sampling[sampling.condition==condition]
        sampling_rows.append([condition,f'{s.samples.min()} / {s.samples.median():g} / {s.samples.max()}',
            f'{s.span_seconds.min():g} / {s.span_seconds.median():g} / {s.span_seconds.max():g}'])
        a=ls[ls.condition==condition]
        alias_rows.append([condition,f'{a.truth_power.median():.4f}',f'{a.alias_power.median():.4f}',
            f'{(a.truth_power-a.alias_power).abs().max():.3g}'])
    report += '## Sampling support and paired alias power\n\n'
    report += markdown_table(['Sampling','Sample count min / median / max','Span seconds min / median / max'],sampling_rows)
    report += '\nThe following powers use the same Lomb–Scargle normalization within each realization. The final column compares the paired powers before summarizing, rather than subtracting two unrelated summary statistics.\n\n'
    report += markdown_table(['Sampling','Median power at truth','Median power at known alias','Maximum absolute paired power gap'],alias_rows)
    report += '\nThe nearly equal paired powers under regular thinning express the sampling ambiguity; they do not establish a second physical signal. All replicate values remain in the [replicate ledger](replicates.csv.gz).\n\n'
    report += '![Preselected replicate zero](preselected-examples.png)\n\n'
    report += ('These are the preselected first replicates, not favorable examples. The left panels '
               'show the first 60 seconds; the spectra use the full observation span. Each spectrum is '
               'scaled to its own maximum for display; power heights do not compare methods. '
               'The [sampling ledger](sampling.csv) retains all sample counts and spans. '
               'Noise is drawn at actual observation times; these results depend on the declared '
               'single sinusoid, noise, observation window and grid. They establish no universal ranking.\n\n'
               '[Design](../../../studies/spectral/DESIGN.md) · [Story](../../../studies/spectral/STORY.md) · '
               '[Inputs](inputs.csv.gz) · [Replicate results](replicates.csv.gz) · '
               '[Metrics](metrics.json) · [Run evidence](run.json). Run `uv run atlas spectral`.\n')
    (out / 'REPORT.md').write_text(report)
    finish_run('spectral', out, started, {'seed': 20261032, 'replicates_per_condition': 100,
                                        'truth_hz': TRUTH, 'recovery_tolerance_hz': TOLERANCE,
                                        'grid_points': len(grid), 'tie_tolerance': 1e-10,
                                        'analytical_inputs': 'Seeded generated observations only; no external data',
                                        'snapshot_check_scope': 'Inherited CO2/electricity checks verify workspace integrity only; not analytical inputs'})
    return summaries
