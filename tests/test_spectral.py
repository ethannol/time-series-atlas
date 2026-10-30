import numpy as np
from scipy.signal import lombscargle
from tsatlas.spectral import frequency_grid, spectra, peak, TRUTH, ALIAS


def test_alias_family_remains_equal_with_noise():
    time = np.arange(0, 480, 3, dtype=float)
    values = np.sin(2 * np.pi * TRUTH * time + .7) + np.random.default_rng(4).normal(0, .5, len(time))
    grid = frequency_grid()
    power = lombscargle(time, values, 2 * np.pi * grid, floating_mean=True, normalize=True)
    estimate, ties = peak(grid, power, 1e-10)
    assert ties >= 2
    for frequency in grid[power >= power.max() - 1e-10]:
        alias = abs(1 / 3 - frequency)
        if .01 <= alias <= .45:
            index = np.argmin(abs(grid - alias))
            assert abs(grid[index] - alias) < 1e-12
            assert abs(power[index] - power.max()) < 1e-10
    assert len(grid) == len(np.unique(grid))


def test_jitter_breaks_known_alias_identity():
    rng = np.random.default_rng(5)
    time = np.arange(0, 480, 3, dtype=float) + rng.uniform(-.4, .4, 160)
    values = np.sin(2 * np.pi * TRUTH * time + .7)
    power = lombscargle(time, values, 2 * np.pi * np.array([TRUTH, ALIAS]),
                       floating_mean=True, normalize=True)
    assert power[0] > .99
    assert power[0] - power[1] > .05


def test_index_fft_loses_time_units():
    time = np.arange(0, 480, 3, dtype=float)
    values = np.sin(2 * np.pi * .05 * time)
    result = spectra(time, values)
    estimate, _ = peak(*result['index_fft'])
    assert abs(estimate - .15) < 1 / len(time)
    estimate, _ = peak(*result['interpolated_fft'])
    assert abs(estimate - .05) < 1 / 480
