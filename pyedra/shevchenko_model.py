#!/usr/bin/env python

# -*- coding: utf-8 -*-


# This file is part of the

#   Pyedra Project (https://github.com/milicolazo/Pyedra/).

# Copyright (c) 2020, Milagros Colazo

# License: MIT

#   Full Text: https://github.com/milicolazo/Pyedra/blob/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""Shevchenko model for Pyedra."""


# =============================================================================
# IMPORTS
# =============================================================================

import attr

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import scipy.optimize as optimization

from . import core

# =============================================================================
# CLASSES AND FUNCTIONS
# =============================================================================


def _Shev_model(x, V_lin, b, c):
    return V_lin + c * x - b / (1 + x)


@attr.s(frozen=True)
class ShevPlot(core.BasePlot):
    """Plots for Shevchenko fit."""

    def curvefit(self, df, ax=None, **kwargs):
        """Plot the phase function using the Shev model.

        Parameters
        ----------
        df : ``pandas.DataFrame``
            The dataframe must contain 3 columns as indicated here:
            id (mpc number of the asteroid), alpha (phase angle) and
            v (reduced magnitude in Johnson's V filter).

        ax : ``matplotlib.pyplot.Axis``, (optional)
            Matplotlib axis

        **kwargs :
            Extra variables are not used


        Return
        ------
        ``matplotlib.pyplot.Axis`` :
            The axis where the method draws.

        """

        def fit_y(alpha, V_lin, b, c):
            y = V_lin + c * alpha - b / (1 + alpha)
            return y

        if ax is None:
            ax = plt.gca()

        ax.invert_yaxis()
        ax.set_title("Phase curves")
        ax.set_xlabel("Phase angle")
        ax.set_ylabel("V")

        for idx, m_row in self.model_df.iterrows():
            data = df[df["id"] == m_row.id]
            v_fit = fit_y(data.alpha, m_row.V_lin, m_row.b, m_row.c)
            ax.plot(data.alpha, v_fit, "--", label=f"Fit {int(m_row.id)}")
            ax.plot(
                data.alpha,
                data.v,
                marker="o",
                linestyle="None",
                label=f"Data {int(m_row.id)}",
            )

        ax.legend(bbox_to_anchor=(1.05, 1))
        return ax


def Shev_fit(df):
    """Fit Shevchenko equation to data from table.

    Shev_fit calculates parameters of the three-parameter empirical
    function proposed by Schevchenko [2]_, [3]_ .

    Parameters
    ----------
    df: ``pandas.DataFrame``
        The dataframe must contain 3 columns as indicated here:
        id (mpc number of the asteroid), alpha (phase angle) and
        v (reduced magnitude in Johnson's V filter).

    Returns
    -------
    model_df: ``pandas.DataFrame``
        The output dataframe contains six columns: id (mpc number of
        the asteroid), V_lin (magnitude calculated by linear
        extrapolation to zero), V_lin error (fit V_lin parameter
        error), b (fit parameter characterizing the opposition efect
        amplitude), b error (fit b parameter error), c (fit parameter
        describing the linear part of the magnitude phase dependence),
        c error (fit c parameter error) [4]_ and R (fit determination
        coefficient).

    References
    ----------
    .. [2] Shevchenko, V. G. 1996. Analysis of the asteroid phase
       dependences of brightness. Lunar Planet Sci. XXVII, 1086.

    .. [3] Shevchenko, V. G. 1997. Analysis of asteroid brightness
       phase relations. Solar System Res. 31, 219-224.

    .. [4] Belskaya, I. N., Shevchenko, V. G., 2000. Opposition effect
       of asteroids. Icarus 147, 94-105.
    """
    lt = core.obs_counter(df, 3)
    if len(lt):
        lt_str = " - ".join(str(idx) for idx in lt)
        raise ValueError(
            f"Some asteroids has less than 3 observations: {lt_str}"
        )

    noob = df.drop_duplicates(subset="id", keep="first", inplace=False)
    size = len(noob)
    id_column = np.empty(size, dtype=int)
    V_lin_column = np.empty(size)
    error_V_lin_column = np.empty(size)
    b_column = np.empty(size)
    error_b_column = np.empty(size)
    c_column = np.empty(size)
    error_c_column = np.empty(size)
    R_column = np.empty(size)

    for idx, id in enumerate(noob.id):

        data = df[df["id"] == id]

        alpha_list = data["alpha"].to_numpy()
        V_list = data["v"].to_numpy()

        op, cov = optimization.curve_fit(_Shev_model, alpha_list, V_list)

        V_lin, b, c = op
        error_V_lin, error_b, error_c = np.sqrt(np.diag(cov))

        residuals = V_list - _Shev_model(alpha_list, *op)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((V_list - np.mean(V_list)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        id_column[idx] = id
        V_lin_column[idx] = V_lin
        error_V_lin_column[idx] = error_V_lin
        b_column[idx] = b
        error_b_column[idx] = error_b
        c_column[idx] = c
        error_c_column[idx] = error_c
        R_column[idx] = r_squared

    model_df = pd.DataFrame(
        {
            "id": id_column,
            "V_lin": V_lin_column,
            "error_V_lin": error_V_lin_column,
            "b": b_column,
            "error_b": error_b_column,
            "c": c_column,
            "error_c": error_c_column,
            "R": R_column,
        }
    )

    plotter = ShevPlot(model_df=model_df)

    return core.PyedraFitDataFrame(model_df=model_df, plot=plotter)
