#!/usr/bin/env python
##############################################################################
#
# diffpy.utils      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 The Trustees of Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE_DANSE.txt for license information.
#
##############################################################################

"""Various utilities related to data parsing and manipulation."""

import numpy as np


def wsinterp(x, xp, fp, left=None, right=None):
    """One-dimensional Whittaker-Shannon interpolation.

    Reconstruct a continuous signal from discrete data points by utilizing sinc functions
    as interpolation kernels. This function interpolates the values of fp (array),
    which are defined over xp (array), at new points x (array or float).
    The implementation is based on E. T. Whittaker's 1915 paper
    (https://doi.org/10.1017/S0370164600017806).

    Parameters
    ----------
    x: ndarray
        The x values at which interpolation is computed.
    xp: ndarray
        The array of known x values.
    fp: ndarray
        The array of y values associated with xp.
    left: float
        If given, set fp for x < xp[0] to left. Otherwise, if left is None (default) or not given,
        set fp for x < xp[0] to fp evaluated at xp[-1].
    right: float
        If given, set fp for x > xp[-1] to right. Otherwise, if right is None (default) or not given, set fp for
        x > xp[-1] to fp evaluated at xp[-1].

    Returns
    -------
    ndarray or float
        The interpolated values at points x. Returns a single float if x is a scalar,
        otherwise returns a numpy.ndarray.
    """
    scalar = np.isscalar(x)
    if scalar:
        x = np.array(x)
        x.resize(1)
    # shape = (nxp, nx), nxp copies of x data span axis 1
    u = np.resize(x, (len(xp), len(x)))
    # Must take transpose of u for proper broadcasting with xp.
    # shape = (nx, nxp), v(xp) data spans axis 1
    v = (xp - u.T) / (xp[1] - xp[0])
    # shape = (nx, nxp), m(v) data spans axis 1
    m = fp * np.sinc(v)
    # Sum over m(v) (axis 1)
    fp_at_x = np.sum(m, axis=1)

    # Enforce left and right
    if left is None:
        left = fp[0]
    fp_at_x[x < xp[0]] = left
    if right is None:
        right = fp[-1]
    fp_at_x[x > xp[-1]] = right

    # Return a float if we got a float
    if scalar:
        return float(fp_at_x[0])

    return fp_at_x


def resample(r, s, dr):
    """Resample a PDF on a new grid.

    This uses the Whittaker-Shannon interpolation formula to put s1 on a new grid if dr is less than the sampling
    interval of r1, or linear interpolation if dr is greater than the sampling interval of r1.

    Parameters
    ----------
    r
        The r-grid used for s1.
    s
        The signal to be resampled.
    dr
        The new sampling interval.

    Returns
    -------
    Returns resampled (r, s).
    """

    dr0 = r[1] - r[0]  # Constant timestep

    if dr0 < dr:
        rnew = np.arange(r[0], r[-1] + 0.5 * dr, dr)
        snew = np.interp(rnew, r, s)
        return rnew, snew

    elif dr0 > dr:
        # Tried to pad the end of s to dampen, but nothing works.
        # m = (s[-1] - s[-2]) / dr0
        # b = (s[-2] * r[-1] - s[-1] * r[-2]) / dr0
        # rpad = r[-1] + np.arange(1, len(s))*dr0
        # spad = rpad * m + b
        # spad = np.concatenate([s,spad])
        # rnew = np.arange(0, rpad[-1], dr)
        # snew = np.zeros_like(rnew)
        # Accommodate for the fact that r[0] might not be 0
        # u = (rnew-r[0]) / dr0
        # for n in range(len(spad)):
        #    snew += spad[n] * np.sinc(u - n)

        # sel = np.logical_and(rnew >= r[0], rnew <= r[-1])

        rnew = np.arange(0, r[-1], dr)
        snew = np.zeros_like(rnew)
        u = (rnew - r[0]) / dr0
        for n in range(len(s)):
            snew += s[n] * np.sinc(u - n)
        sel = np.logical_and(rnew >= r[0], rnew <= r[-1])
        return rnew[sel], snew[sel]

    # If we got here, then no resampling is required
    return r.copy(), s.copy()
