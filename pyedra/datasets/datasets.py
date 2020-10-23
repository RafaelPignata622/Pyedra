#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Pyedra Project (https://github.com/milicolazo/Pyedra/).
# Copyright (c) 2020, Milagros Colazo
# License: MIT
#   Full Text: https://github.com/milicolazo/Pyedra/blob/master/LICENSE

"""
The pyedra.datasets module includes utilities to load datasets.

It also features some artificial data generators.
"""

# ============================================================================
# IMPORTS
# ============================================================================

import os
import pathlib

import pandas as pd

# ============================================================================
# CONSTANTS
# ============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

# ============================================================================
# FUNCTIONS
# ============================================================================


def load_carbognani2019():
    """Input for testing the phase functions.

    This dataset contains the first and second columns of Table 2 of
    Carbognani et al. (2019). These columns correspond to: phase angle
    (°) and V_max (mag). V_max is the reduced magnitude of the
    lightcurve maximum.

    References
    ----------
    .. [1] Carbognani, A., Cellino, A., & Caminiti, S. (2019). New
    phase-magnitude curves for some main belt asteroids, fit of
    different photometric systems and calibration of the
    albedo-Photometry relation. Planetary and Space Science,
    169, 15-34.
    """
    path = PATH / "carbognani2019.csv"

    return pd.read_csv(path)


def load_penttila2016():
    """Tabulated values of the base functions for H-G1-G2 system.

    This dataset corresponds to Table B.4 of Penttila et al. (2016).

    References
    ----------
    .. [1] A. Penttil ̈a,  V. G. Shevchenko, O. Wilkman, & K. Muinonen
    (2016). H,G1, G2 photometric phase function extended to
    low-accuracy data. 123:117–125.
    """
    path = PATH / "penttila2016.csv"

    return pd.read_csv(path)
