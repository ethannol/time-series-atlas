# Exploratory spectral robustness: every declared cell

Each procedure has 50 trials per cell; all five procedures use the same realizations. Intervals are pointwise marginal 95% Wilson intervals, not simultaneous bands or paired tests of differences. The 2,403-point LS grid is unchanged. A common band does not align native FFT and LS bins. Regular three-second sampling is analytically ambiguous regardless of numerical ties or whether the lowest-frequency peak recovers the truth.

## Truth 0.08325 Hz, noise SD 0.5

| Sampling | Procedure | Recovered / trials | Fraction [95% Wilson] | Median absolute error (Hz) | Numerical ties / trials | Analytic ambiguity / trials |
| --- | --- | --- | --- | --- | --- | --- |
| regular | index_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | index_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.08959 | 0 | 0 |
| irregular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.08959 | 0 | 0 |
| irregular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| every_three_seconds | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.16675 | 0 | 50 |
| every_three_seconds | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00043 | 0 | 50 |
| every_three_seconds | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 50 | 50 |
| every_three_seconds | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.16675 | 0 | 50 |
| every_three_seconds | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00043 | 0 | 50 |

## Truth 0.08325 Hz, noise SD 1

| Sampling | Procedure | Recovered / trials | Fraction [95% Wilson] | Median absolute error (Hz) | Numerical ties / trials | Analytic ambiguity / trials |
| --- | --- | --- | --- | --- | --- | --- |
| regular | index_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | index_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.09436 | 0 | 0 |
| irregular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.09436 | 0 | 0 |
| irregular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| every_three_seconds | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.16675 | 0 | 50 |
| every_three_seconds | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00043 | 0 | 50 |
| every_three_seconds | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 50 | 50 |
| every_three_seconds | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.16675 | 0 | 50 |
| every_three_seconds | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00043 | 0 | 50 |

## Truth 0.17 Hz, noise SD 0.5

| Sampling | Procedure | Recovered / trials | Fraction [95% Wilson] | Median absolute error (Hz) | Numerical ties / trials | Analytic ambiguity / trials |
| --- | --- | --- | --- | --- | --- | --- |
| regular | index_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| regular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| regular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00000 | 0 | 0 |
| regular | index_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| regular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| irregular | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.10949 | 0 | 0 |
| irregular | interpolated_fft | 44 / 50 | 88.0% [76.2%, 94.4%] | 0.00083 | 0 | 0 |
| irregular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00000 | 0 | 0 |
| irregular | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.10949 | 0 | 0 |
| irregular | interpolated_fft_common_band | 44 / 50 | 88.0% [76.2%, 94.4%] | 0.00083 | 0 | 0 |
| every_three_seconds | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.31750 | 0 | 50 |
| every_three_seconds | interpolated_fft | 1 / 50 | 2.0% [0.4%, 10.5%] | 0.00682 | 0 | 50 |
| every_three_seconds | lomb_scargle | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.00667 | 50 | 50 |
| every_three_seconds | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.15188 | 0 | 50 |
| every_three_seconds | interpolated_fft_common_band | 1 / 50 | 2.0% [0.4%, 10.5%] | 0.00682 | 0 | 50 |

## Truth 0.17 Hz, noise SD 1

| Sampling | Procedure | Recovered / trials | Fraction [95% Wilson] | Median absolute error (Hz) | Numerical ties / trials | Analytic ambiguity / trials |
| --- | --- | --- | --- | --- | --- | --- |
| regular | index_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| regular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| regular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00000 | 0 | 0 |
| regular | index_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| regular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00083 | 0 | 0 |
| irregular | index_fft | 1 / 50 | 2.0% [0.4%, 10.5%] | 0.11164 | 0 | 0 |
| irregular | interpolated_fft | 9 / 50 | 18.0% [9.8%, 30.8%] | 0.13250 | 0 | 0 |
| irregular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00000 | 0 | 0 |
| irregular | index_fft_common_band | 1 / 50 | 2.0% [0.4%, 10.5%] | 0.10860 | 0 | 0 |
| irregular | interpolated_fft_common_band | 9 / 50 | 18.0% [9.8%, 30.8%] | 0.12625 | 0 | 0 |
| every_three_seconds | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.31750 | 0 | 50 |
| every_three_seconds | interpolated_fft | 1 / 50 | 2.0% [0.4%, 10.5%] | 0.00682 | 0 | 50 |
| every_three_seconds | lomb_scargle | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.00667 | 50 | 50 |
| every_three_seconds | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.13750 | 0 | 50 |
| every_three_seconds | interpolated_fft_common_band | 1 / 50 | 2.0% [0.4%, 10.5%] | 0.00682 | 0 | 50 |

## Truth 0.28725 Hz, noise SD 0.5

| Sampling | Procedure | Recovered / trials | Fraction [95% Wilson] | Median absolute error (Hz) | Numerical ties / trials | Analytic ambiguity / trials |
| --- | --- | --- | --- | --- | --- | --- |
| regular | index_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| regular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| regular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | index_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| regular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| irregular | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.10856 | 0 | 0 |
| irregular | interpolated_fft | 4 / 50 | 8.0% [3.2%, 18.8%] | 0.26746 | 0 | 0 |
| irregular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | index_fft_common_band | 1 / 50 | 2.0% [0.4%, 10.5%] | 0.09791 | 0 | 0 |
| irregular | interpolated_fft_common_band | 5 / 50 | 10.0% [4.3%, 21.4%] | 0.25808 | 0 | 0 |
| every_three_seconds | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.14975 | 0 | 50 |
| every_three_seconds | interpolated_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.24122 | 0 | 50 |
| every_three_seconds | lomb_scargle | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.24125 | 50 | 50 |
| every_three_seconds | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.14975 | 0 | 50 |
| every_three_seconds | interpolated_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.24122 | 0 | 50 |

## Truth 0.28725 Hz, noise SD 1

| Sampling | Procedure | Recovered / trials | Fraction [95% Wilson] | Median absolute error (Hz) | Numerical ties / trials | Analytic ambiguity / trials |
| --- | --- | --- | --- | --- | --- | --- |
| regular | index_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| regular | interpolated_fft | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| regular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| regular | index_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| regular | interpolated_fft_common_band | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00025 | 0 | 0 |
| irregular | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.14907 | 0 | 0 |
| irregular | interpolated_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.25600 | 0 | 0 |
| irregular | lomb_scargle | 50 / 50 | 100.0% [92.9%, 100.0%] | 0.00008 | 0 | 0 |
| irregular | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.11722 | 0 | 0 |
| irregular | interpolated_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.25392 | 0 | 0 |
| every_three_seconds | index_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.14975 | 0 | 50 |
| every_three_seconds | interpolated_fft | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.24122 | 0 | 50 |
| every_three_seconds | lomb_scargle | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.24108 | 50 | 50 |
| every_three_seconds | index_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.14975 | 0 | 50 |
| every_three_seconds | interpolated_fft_common_band | 0 / 50 | 0.0% [0.0%, 7.1%] | 0.24122 | 0 | 50 |

