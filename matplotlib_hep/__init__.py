from __future__ import division

import numpy as np
import scipy.stats as stats
import scipy as sp
import logging

__all__ = ['histpoints', 'calc_nbins']

def calc_nbins(x, maximum=150):
    n =  (max(x) - min(x)) / (2 * len(x)**(-1/3) * (np.percentile(x, 75) - np.percentile(x, 25)))
    return min(n, maximum)

def poisson_limits(N, kind, confidence=0.6827):
    alpha = 1 - confidence
    upper = np.zeros(len(N))
    lower = np.zeros(len(N))
    if kind == 'gamma':
        lower = stats.gamma.ppf(alpha / 2, N)
        upper = stats.gamma.ppf(1 - alpha / 2, N + 1)
    elif kind == 'sqrt':
        lower = sqrt(N)
        upper = lower
    else:
        raise ValueError('Unknown errorbar kind: {}'.format(kind))
    # clip lower bars
    lower[N==0] = 0
    return N - lower, upper - N

def histpoints(x, bins=None, xerr=None, yerr='gamma', normed=False, **kwargs):
    """
    Plot a histogram as a series of data points.

    Compute and draw the histogram of *x* using individual (x,y) points
    for the bin contents.

    By default, vertical poisson error bars are calculated using the
    gamma distribution.

    Horizontal error bars are omitted by default.
    These can be enable using the *xerr* argument.
    Use ``xerr='binwidth'`` to draw horizontal error bars that indicate
    the width of each histogram bin.

    Paramters
    ---------

    x : (n,) array or sequence of (n,) arrays
        Input values. This takes either a single array or a sequency of
        arrays which are not required to be of the same length

    """
    import matplotlib.pyplot as plt

    if bins is None:
        bins = calc_nbins(x)

    h, bins = np.histogram(x, bins=bins)
    width = bins[1] - bins[0]
    center = (bins[:-1] + bins[1:]) / 2
    area = sum(h * width)

    if isinstance(yerr, str):
        yerr = poisson_limits(h, yerr)

    if xerr == 'binwidth':
        xerr = width / 2

    if normed:
        h = h / area
        yerr = yerr / area
        area = 1.

    if not 'color' in kwargs:
        kwargs['color'] = 'black'

    if not 'fmt' in kwargs:
        kwargs['fmt'] = 'o'

    plt.errorbar(center, h, xerr=xerr, yerr=yerr, **kwargs)

    return center, h, area

