"""Utilities for equity selection using a simplified BARRA factor model.

The functions in this module implement a light‑weight workflow for
factor exposure estimation, idiosyncratic risk calculation and a basic
risk‑adjusted selection routine.  The goal is to provide a minimal
interface that returns a list of chosen assets given historical returns
and factor data.
"""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd


def compute_factor_exposures(
    returns: pd.DataFrame, factor_returns: pd.DataFrame
) -> pd.DataFrame:
    """Estimate factor exposures via ordinary least squares.

    Parameters
    ----------
    returns : pandas.DataFrame
        Asset returns with assets in columns and time in rows.
    factor_returns : pandas.DataFrame
        Factor returns aligned on the same index as ``returns``.

    Returns
    -------
    pandas.DataFrame
        Estimated factor exposures (betas) for each asset.
    """

    exposures = {}
    X = factor_returns.values
    for asset in returns:
        y = returns[asset].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        exposures[asset] = beta
    return pd.DataFrame(exposures, index=factor_returns.columns).T


def compute_idiosyncratic_risk(
    returns: pd.DataFrame, factor_returns: pd.DataFrame, exposures: pd.DataFrame
) -> pd.Series:
    """Compute idiosyncratic risk (residual variance) for each asset."""

    common = factor_returns.dot(exposures.T)
    residuals = returns - common
    return residuals.var()


def optimize_selection(
    expected_returns: pd.Series,
    exposures: pd.DataFrame,
    factor_cov: pd.DataFrame,
    idiosyncratic_risk: pd.Series,
    risk_aversion: float = 1.0,
    top_n: int = 10,
) -> List[str]:
    """Select assets by a simple mean‑variance score.

    Assets are ranked by ``expected_return - risk_aversion * variance``
    where variance combines both factor and idiosyncratic components.
    """

    scores = {}
    for asset in expected_returns.index:
        beta = exposures.loc[asset].values
        systematic = beta @ factor_cov.values @ beta
        total_var = systematic + idiosyncratic_risk[asset]
        scores[asset] = expected_returns[asset] - risk_aversion * total_var
    return [a for a, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]]


def select_equities(
    returns: pd.DataFrame,
    factor_returns: pd.DataFrame,
    expected_returns: pd.Series,
    factor_cov: pd.DataFrame,
    risk_aversion: float = 1.0,
    top_n: int = 10,
) -> List[str]:
    """Full pipeline returning a list of selected equities.

    This function ties together exposure estimation, idiosyncratic risk
    calculation and the simple optimization routine.
    """

    exposures = compute_factor_exposures(returns, factor_returns)
    idio = compute_idiosyncratic_risk(returns, factor_returns, exposures)
    return optimize_selection(
        expected_returns=expected_returns,
        exposures=exposures,
        factor_cov=factor_cov,
        idiosyncratic_risk=idio,
        risk_aversion=risk_aversion,
        top_n=top_n,
    )
