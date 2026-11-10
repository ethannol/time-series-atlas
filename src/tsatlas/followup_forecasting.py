"""Declared post-publication forecasting comparisons; original artifacts stay intact."""
from pathlib import Path

import numpy as np
import pandas as pd

from .common import markdown_table, plt, save_frame
from .data import write_json
from .metrics import forecast_scores


LINEAR_MODELS = ['linear_expanding', 'linear_120months']
CO2_LABELS = {
    'linear_expanding': 'All-history linear',
    'linear_120months': 'Trailing-decade linear',
    'linear_expanding_anchored': 'All-history linear, anchored',
    'linear_120months_anchored': 'Trailing-decade linear, anchored',
}
MEDIAN_MODEL = 'median_52weeks'


def anchored_co2_predictions(frame, predictions):
    """Return original/anchored rows, calibration offsets, and origin diagnostics.

    The saved December predictions identify the fitted December intercept.
    Neither the reconstruction nor its level adjustment reads a target outcome.
    """
    original = predictions.loc[predictions.model.isin(LINEAR_MODELS)].copy()
    if set(original.model) != set(LINEAR_MODELS):
        raise ValueError('Both original linear models are required')
    if original.duplicated(['model', 'origin_month', 'horizon']).any():
        raise ValueError('Duplicate CO2 prediction keys')
    if set(original.split) != {'calibration', 'test'}:
        raise ValueError('Expected the original calibration and test splits')
    if (original.origin_month.dt.month != 12).any():
        raise ValueError('Origin reconstruction requires December origins')
    first_test_origin = original.loc[original.split == 'test', 'origin_month'].min()
    if not (original.loc[original.split == 'calibration', 'target'] < first_test_origin).all():
        raise ValueError('Calibration outcomes must precede the first test origin')

    anchored, diagnostics, offsets = [], [], []
    for model in LINEAR_MODELS:
        group = original.loc[original.model == model].copy()
        pivot = group.pivot(index='origin_month', columns='horizon', values='prediction')
        if not {12, 36}.issubset(pivot.columns) or not np.isfinite(pivot[[12, 36]]).all().all():
            raise ValueError('Each origin requires finite 12- and 36-month predictions')
        origins = frame.reindex(pivot.index)
        if not origins.usable.fillna(False).all() or not np.isfinite(origins.average).all():
            raise ValueError('Origin anchoring requires a usable observed December value')
        fitted = (3 * pivot[12] - pivot[36]) / 2
        gap = origins.average - fitted
        diagnostic = pd.DataFrame({
            'model': model, 'observed_origin': origins.average,
            'fitted_origin': fitted, 'origin_gap': gap,
            'split': group.groupby('origin_month').split.first(),
        }).rename_axis('origin_month').reset_index()
        diagnostics.append(diagnostic)
        group['prediction'] = group.prediction + group.origin_month.map(gap)
        group['model'] = model + '_anchored'
        for horizon, horizon_rows in group.groupby('horizon'):
            calibration = horizon_rows.loc[horizon_rows.split == 'calibration']
            residuals = (calibration.actual - calibration.prediction).to_numpy()
            if not len(residuals) or not np.isfinite(residuals).all():
                raise ValueError('Each anchored model/horizon needs finite calibration residuals')
            low, high = np.quantile(residuals, [.1, .9], method='linear')
            mask = group.horizon == horizon
            group.loc[mask, 'lower'] = group.loc[mask, 'prediction'] + low
            group.loc[mask, 'upper'] = group.loc[mask, 'prediction'] + high
            offsets.append({
                'model': model + '_anchored', 'horizon': int(horizon),
                'n_calibration': len(calibration), 'lower_offset': float(low),
                'upper_offset': float(high),
                'last_calibration_target': calibration.target.max(),
                'first_test_origin': first_test_origin,
            })
        anchored.append(group)
    return (pd.concat([original, *anchored], ignore_index=True),
            pd.DataFrame(offsets), pd.concat(diagnostics, ignore_index=True))


def co2_followup_scores(predictions):
    """Score identical test targets, retaining the target-only site sensitivity."""
    test = predictions.loc[predictions.split == 'test']
    result = {}
    for name, selected in [('test', test), ('exclude_site_targets', test.loc[~test.site_substitution])]:
        result[name] = {
            f'{model}/{horizon}': forecast_scores(g.actual, g.prediction, g.lower, g.upper)
            for (model, horizon), g in selected.groupby(['model', 'horizon'])
        }
    return result


def co2_followup(out, frame, predictions):
    """Write separately named CO2 evidence and return an appendable report section."""
    out = Path(out)
    combined, calibration, gaps = anchored_co2_predictions(frame, predictions)
    scores = co2_followup_scores(combined)
    save_frame(combined, out / 'followup-predictions.csv.gz')
    save_frame(gaps, out / 'followup-origin-gaps.csv.gz')
    calibration.to_csv(out / 'followup-calibration.csv', index=False)
    write_json(out / 'followup-metrics.json', scores)
    score_rows = []
    for sample, methods in scores.items():
        for key, values in methods.items():
            model, horizon = key.rsplit('/', 1)
            score_rows.append({'sample': sample, 'model': model, 'horizon': int(horizon), **values})
    pd.DataFrame(score_rows).to_csv(out / 'followup-scores.csv', index=False)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    axes[0].plot(frame.index, frame.average.where(frame.usable), color='#64748b', lw=1,
                 label='Usable monthly source observations')
    test_origins = gaps.loc[gaps.split == 'test'].drop_duplicates('origin_month')
    axes[0].scatter(test_origins.origin_month, test_origins.observed_origin,
                    color='#111827', s=22, label='Observed test-origin December', zorder=3)
    for model, color in zip(LINEAR_MODELS, ['#d97706', '#0f766e']):
        group = gaps.loc[gaps.model == model].sort_values('origin_month')
        test = group.loc[group.split == 'test']
        axes[0].scatter(test.origin_month, test.fitted_origin, marker='x', s=28,
                        color=color, label=CO2_LABELS[model] + ' fitted origin')
        for split, marker in [('calibration', 'o'), ('test', 's')]:
            part = group.loc[group.split == split]
            axes[1].plot(part.origin_month, part.origin_gap, marker=marker, color=color,
                         label=CO2_LABELS[model] + ' / ' + split, markersize=4)
    site_dates = frame.index[frame.site_substitution]
    if len(site_dates):
        axes[0].axvspan(site_dates.min(), site_dates.max() + pd.DateOffset(months=1),
                        color='#a78bfa', alpha=.18, label='Site-substitution period')
    axes[0].set(ylabel='CO₂ (ppm)', title='Source series and original fitted starting levels')
    axes[0].legend(fontsize=8, ncol=2, loc='upper left')
    axes[1].axhline(0, color='black', lw=.8)
    axes[1].set(xlabel='December origin', ylabel='Observed minus fitted origin (ppm)',
                title='Level added to every horizon; slope and month effects stay fixed')
    axes[1].legend(fontsize=8, ncol=2)
    fig.suptitle('Post-publication exploratory follow-up: origin anchoring')
    fig.tight_layout()
    fig.savefig(out / 'followup-origin-anchoring.png')
    plt.close(fig)

    rows = []
    for model in CO2_LABELS:
        for horizon in [1, 12, 36]:
            v = scores['test'][f'{model}/{horizon}']
            rows.append([CO2_LABELS[model], horizon, v['n'], f"{v['mae']:.3f}",
                         f"{v['bias']:+.3f}", f"{v['coverage80']:.1%}",
                         f"{v['width80']:.3f}", f"{v['interval_score80']:.3f}"])
    differences = []
    for model in LINEAR_MODELS:
        change = scores['test'][f'{model}_anchored/36']['mae'] - scores['test'][f'{model}/36']['mae']
        differences.append(f"{CO2_LABELS[model]}: {change:+.3f} ppm")
    sensitivity_rows = []
    for model in CO2_LABELS:
        v = scores['exclude_site_targets'][f'{model}/36']
        sensitivity_rows.append([CO2_LABELS[model], v['n'], f"{v['mae']:.3f}",
                                 f"{v['bias']:+.3f}", f"{v['coverage80']:.1%}",
                                 f"{v['width80']:.3f}", f"{v['interval_score80']:.3f}"])
    return (
        '\n## Post-publication exploratory follow-up: anchor the starting level\n\n'
        '**This comparison was declared after the original results were known.** '
        'It adds two fixed alternatives; the original predictions and scores remain unchanged. '
        'For each linear fit, fitted December = (3 × p12 − p36) / 2. '
        'We add observed December minus fitted December to every forecast horizon, '
        'preserving the fitted slope and month effects. Only usable observed origins are allowed.\n\n'
        '![Source history and the origin-level adjustment](followup-origin-anchoring.png)\n\n'
        'The primary endpoint remains December three years later. The signed change in '
        '36-month MAE (anchored minus original; negative favors anchoring) is '
        + '; '.join(differences) + '. Bias below is prediction minus observation.\n\n'
        + markdown_table(['Fit', 'Months', 'Targets', 'MAE ppm', 'Bias ppm', '80% coverage',
                          'Width ppm', 'Interval score'], rows)
        + '\nEach anchored fit/horizon uses its own residual 10th/90th quantiles from '
        'the original pre-test calibration period only. The nominal 80% level is not a '
        'coverage guarantee. Only observations available by an origin enter that forecast’s '
        'adjustment; all interval calibration outcomes precede the first test origin.\n\n'
        'Excluding site-substitution-affected **targets** gives this three-year sensitivity; '
        'intervals are not recalibrated. All three horizons are in the linked score table.\n\n'
        + markdown_table(['Fit', 'Targets', 'MAE ppm', 'Bias ppm', '80% coverage',
                          'Width ppm', 'Interval score'], sensitivity_rows)
        + '\nTarget exclusion does not remove substituted-site values from training or '
        'from a later origin anchor (including December 2022). This arithmetic intervention '
        'is not causal attribution about the atmosphere or a decomposition of MAE. '
        'Overlapping multiyear errors are dependent; no superiority test is claimed.\n\n'
        '[All calibration/test predictions](followup-predictions.csv.gz) · '
        '[Calibration offsets](followup-calibration.csv) · '
        '[Origin gaps](followup-origin-gaps.csv.gz) · '
        '[All horizons and site sensitivity](followup-scores.csv) · '
        '[Metrics](followup-metrics.json) · [Follow-up contract](../../../studies/followups/DESIGN.md).\n'
    )


def trailing_weekly_median(series, origin):
    """Median of exactly 52 complete Monday–Sunday totals strictly before origin."""
    origin = pd.Timestamp(origin)
    if origin.dayofweek != 0 or origin != origin.normalize():
        raise ValueError('Weekly origin must be Monday midnight')
    if not series.index.is_unique:
        raise ValueError('Daily history must have unique dates')
    dates = pd.date_range(origin - pd.Timedelta(days=364), periods=364, freq='D')
    values = series.reindex(dates).to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError('Median requires 364 complete finite nonnegative preceding days')
    return float(np.median(values.reshape(52, 7).sum(axis=1)))


def retail_median_predictions(panel, predictions):
    """Append one comparator with the exact original targets and training scales."""
    from .retail import MODELS

    if set(predictions.model) != set(MODELS):
        raise ValueError('Expected all five original retail methods')
    if predictions.duplicated(['origin', 'product', 'model']).any():
        raise ValueError('Duplicate retail prediction keys')
    groups = predictions.groupby(['origin', 'product'])
    if not groups.size().eq(len(MODELS)).all():
        raise ValueError('Every product-week requires all original methods')
    if (groups[['observed', 'training_weekly_scale', 'target_end']].nunique() != 1).any().any():
        raise ValueError('Original methods must share targets and fixed scales')
    if not predictions.groupby('product').training_weekly_scale.nunique().eq(1).all():
        raise ValueError('Training normalization must remain fixed per stock code')
    median = predictions.loc[predictions.model == 'zero'].copy()
    if not np.isfinite(median.training_weekly_scale).all() or (median.training_weekly_scale <= 0).any():
        raise ValueError('Training scales must be finite and positive')
    median['model'] = MEDIAN_MODEL
    median['prediction'] = [trailing_weekly_median(panel[row.product], row.origin)
                            for row in median.itertuples()]
    return pd.concat([predictions, median], ignore_index=True)


def retail_leave_one_out(predictions):
    """Retain every stock-code exclusion and every method, without cohort selection."""
    from .retail import summarize

    products = sorted(predictions['product'].unique())
    if len(products) < 2:
        raise ValueError('Leave-one-code-out needs at least two stock codes')
    rows = []
    for product in products:
        retained = predictions.loc[predictions['product'] != product]
        rows.extend({'excluded_product': product, **row} for row in summarize(retained))
    return pd.DataFrame(rows)


def last_week_bias_identity(panel, predictions):
    """Audit telescoping forecast-minus-actual totals separately for every code."""
    last_week = predictions.loc[predictions.model == 'last_week']
    rows = []
    for product, group in last_week.groupby('product', sort=True):
        group = group.sort_values('origin')
        origins = pd.DatetimeIndex(group.origin)
        if not origins.equals(pd.date_range(origins.min(), origins.max(), freq='7D')):
            raise ValueError('Bias telescoping requires contiguous nonduplicate target weeks')
        previous = panel[product].reindex(pd.date_range(origins.min() - pd.Timedelta(days=7), periods=7))
        final = panel[product].reindex(pd.date_range(origins.max(), periods=7))
        if not np.isfinite(previous).all() or not np.isfinite(final).all():
            raise ValueError('Bias identity requires complete boundary weeks')
        signed_error = float((group.prediction - group.observed).sum())
        boundary_difference = float(previous.sum() - final.sum())
        if not np.isclose(signed_error, boundary_difference, rtol=1e-12, atol=1e-10):
            raise ValueError('Saved last-week forecasts fail the boundary-week bias identity')
        rows.append({'product': product, 'weeks': len(group),
                     'pretest_week_units': float(previous.sum()), 'final_week_units': float(final.sum()),
                     'signed_total_error_units': signed_error,
                     'boundary_difference_units': boundary_difference,
                     'identity_residual_units': signed_error - boundary_difference})
    return pd.DataFrame(rows)


def _winners(table, column):
    """List exact ties too, instead of depending on incidental method ordering."""
    return ', '.join(table.loc[table[column] == table[column].min(), 'model'])


def retail_followup(out, panel, predictions):
    """Write the six-method comparison and diagnostics without altering originals."""
    from .retail import MODELS, summarize

    out = Path(out)
    combined = retail_median_predictions(panel, predictions)
    methods = [*MODELS, MEDIAN_MODEL]
    metrics = pd.DataFrame(summarize(combined)).set_index('model').loc[methods].reset_index()
    exclusions = retail_leave_one_out(combined)
    bias = last_week_bias_identity(panel, predictions)
    base = predictions.loc[predictions.model == 'zero']
    concentration = base.groupby('product')['observed'].sum().sort_values(ascending=False).rename('test_units').reset_index()
    total_units = float(concentration.test_units.sum())
    if total_units <= 0:
        raise ValueError('Volume concentration requires positive total test sales')
    concentration['unit_share'] = concentration.test_units / total_units
    concentration['cumulative_unit_share'] = concentration.unit_share.cumsum()
    product_rows, quarter_rows = [], []
    for product, group in combined.groupby('product', sort=True):
        product_rows.extend({'product': product, **row} for row in summarize(group))
    for quarter, group in combined.groupby(combined.origin.dt.quarter):
        quarter_rows.extend({'quarter': int(quarter), 'weeks': group.origin.nunique(), **row}
                            for row in summarize(group))
    quarters = pd.DataFrame(quarter_rows)
    original = metrics.loc[metrics.model.isin(MODELS)].sort_values('macro_scaled_mae')
    first, second = original.iloc[0], original.iloc[1]
    original_gap = float(second.macro_scaled_mae - first.macro_scaled_mae)
    totals = bias[['pretest_week_units', 'final_week_units', 'signed_total_error_units']].sum()
    write_json(out / 'followup-metrics.json', {
        'primary': metrics.to_dict('records'), 'products': int(base['product'].nunique()),
        'weeks': int(base.origin.nunique()), 'post_publication_exploratory': True,
        'original_scaled_gap': {'best_model': first.model, 'next_model': second.model,
                                'next_minus_best': original_gap},
        'last_week_bias_identity': {key: float(value) for key, value in totals.items()},
    })
    save_frame(combined, out / 'followup-predictions.csv.gz')
    pd.DataFrame(product_rows).to_csv(out / 'followup-per-product.csv', index=False)
    quarters.to_csv(out / 'followup-per-quarter.csv', index=False)
    exclusions.to_csv(out / 'followup-leave-one-code-out.csv', index=False)
    concentration.to_csv(out / 'followup-volume-shares.csv', index=False)
    bias.to_csv(out / 'followup-bias-identity.csv', index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    colors = ['#6b7280', '#9ca3af', '#2563eb', '#0f766e', '#b45309', '#7c3aed']
    bars = axes[0].barh(metrics.model, metrics.macro_scaled_mae, color=colors)
    axes[0].bar_label(bars, fmt='%.3f', padding=3)
    axes[0].set_xlim(0, max(float(metrics.macro_scaled_mae.max()) * 1.2, .1))
    axes[0].set(xlabel='Weekly MAE / fixed mean training-week sales', title='Equal weight for exact stock codes')
    percent_bias = (metrics.forecast_total_units / metrics.observed_total_units - 1) * 100
    axes[1].barh(metrics.model, percent_bias, color=colors)
    axes[1].axvline(0, color='black', lw=.8)
    axes[1].set(xlabel='Forecast total minus recorded units (%)', title='Signed total bias remains visible')
    fig.suptitle('Post-publication exploratory follow-up: 52-week median')
    fig.tight_layout()
    fig.savefig(out / 'followup-median-comparison.png')
    plt.close(fig)

    table_rows = [[r.model, f'{r.macro_scaled_mae:.6f}', f'{r.unit_mae:.3f}',
                   f'{r.forecast_total_units:.1f}', f'{r.signed_total_error_units:+.1f}']
                  for r in metrics.itertuples()]
    quarter_summary = []
    for quarter, group in quarters.groupby('quarter'):
        old = group.loc[group.model.isin(MODELS)]
        quarter_summary.append([f'2011 Q{quarter}', int(group.weeks.iloc[0]),
                                _winners(old, 'macro_scaled_mae'), _winners(old, 'unit_mae'),
                                _winners(group, 'macro_scaled_mae'), _winners(group, 'unit_mae')])
    exclusion_summary = []
    for product, group in exclusions.groupby('excluded_product', sort=True):
        exclusion_summary.append([product, _winners(group, 'macro_scaled_mae'),
                                  _winners(group, 'unit_mae')])
    largest = concentration.iloc[0]
    return (
        '\n## Post-publication exploratory follow-up: a historical weekly median\n\n'
        '**This comparator and the following diagnostics were declared after the original '
        'results were known.** At each existing Monday origin, `median_52weeks` takes the '
        'ordinary sample median of 52 complete Monday–Sunday sales totals from exactly '
        'the preceding 364 calendar days. Every day must be finite; the current target '
        'week is excluded. The exact stock codes, test weeks and fixed 2010 scales are unchanged. '
        'There is no tuning. This is a history-conditioned empirical median, not proof of '
        'an optimal conditional quantile or order quantity.\n\n'
        f"Among all six methods, the lowest scaled weekly MAE is attained by {_winners(metrics, 'macro_scaled_mae')}; "
        f"the lowest raw-unit MAE is attained by {_winners(metrics, 'unit_mae')}. "
        'These remain descriptive comparisons for the fixed panel.\n\n'
        + markdown_table(['Method', 'Scaled MAE', 'Unit MAE', 'Forecast units', 'Signed total error'], table_rows)
        + '\n![Six-method errors and bias](followup-median-comparison.png)\n\n'
        f"The original five-method scaled-score gap was {original_gap:.6f}: "
        f"{second.model} ({second.macro_scaled_mae:.6f}) minus {first.model} ({first.macro_scaled_mae:.6f}). "
        f"Exact code `{largest['product']}` contributes {largest.test_units:.0f} of {total_units:.0f} "
        f"recorded test units ({largest.unit_share:.2%}). "
        'That is a share of recorded volume, not a weight in the equally weighted scaled score. '
        'Raw-unit error can be concentrated among large sellers. [Every code’s volume share](followup-volume-shares.csv).\n\n'
        'Quarterly minima show the time context; quarter 4 contains only the complete scored '
        'weeks through December 4. These dependent subsets do not establish a persistent winner.\n\n'
        + markdown_table(['Quarter', 'Weeks', 'Original scaled minimum', 'Original unit minimum',
                          'Six-method scaled minimum', 'Six-method unit minimum'], quarter_summary)
        + '\nEvery leave-one-code-out exclusion is retained below. The '
        '[full score table](followup-leave-one-code-out.csv) reports all six methods for '
        f"all {len(exclusion_summary)} exclusions, with the original per-code training scales. "
        'These overlapping subsets describe sensitivity; no replacement cohort is chosen, '
        'and they are not independent replications. Exact ties are listed together.\n\n'
        + markdown_table(['Excluded exact code', 'Scaled-MAE minimum', 'Unit-MAE minimum'], exclusion_summary)
        + '\nFor the last-week forecast, summed prediction minus observation telescopes '
        'over contiguous weeks to the pre-test week minus the final target week: '
        f"{totals.pretest_week_units:.0f} − {totals.final_week_units:.0f} = "
        f"{totals.signed_total_error_units:+.0f} units. "
        'A near-matching total can therefore coexist with large week-by-week allocation errors. '
        'The identity is checked separately for every exact code; it is not evidence of an '
        'inventory policy’s value.\n\n'
        '[All six prediction sets](followup-predictions.csv.gz) · '
        '[Metrics](followup-metrics.json) · [Per-code scores](followup-per-product.csv) · '
        '[Quarterly scores](followup-per-quarter.csv) · [Boundary-week identity](followup-bias-identity.csv) · '
        '[Follow-up contract](../../../studies/followups/DESIGN.md).\n'
    )
