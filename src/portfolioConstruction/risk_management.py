import numpy as np
import pandas as pd
from typing import Optional, Dict


def calculate_var(portfolio_returns: pd.Series, confidence_level: float = 0.95) -> float:
    """Compute historical Value at Risk (VaR).

    Parameters
    ----------
    portfolio_returns : pd.Series
        Series of portfolio returns.
    confidence_level : float, optional
        Confidence level for the VaR calculation, by default 0.95.

    Returns
    -------
    float
        VaR expressed as a positive loss number.
    """
    if portfolio_returns.empty:
        return 0.0

    percentile = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
    return -percentile


def calculate_cvar(portfolio_returns: pd.Series, confidence_level: float = 0.95) -> float:
    """Compute Conditional Value at Risk (CVaR) also known as expected shortfall.

    Parameters
    ----------
    portfolio_returns : pd.Series
        Series of portfolio returns.
    confidence_level : float, optional
        Confidence level for the CVaR calculation, by default 0.95.

    Returns
    -------
    float
        CVaR expressed as a positive loss number.
    """
    if portfolio_returns.empty:
        return 0.0

    var_threshold = np.percentile(portfolio_returns, (1 - confidence_level) * 100)
    tail_losses = portfolio_returns[portfolio_returns <= var_threshold]

    return -tail_losses.mean() if not tail_losses.empty else -var_threshold


def apply_volatility_targeting(
    weights: np.ndarray, returns: pd.DataFrame, target_volatility: float
) -> np.ndarray:
    """Scale weights to target a desired portfolio volatility.

    Parameters
    ----------
    weights : np.ndarray
        Current portfolio weights.
    returns : pd.DataFrame
        Historical asset returns.
    target_volatility : float
        Target volatility for the portfolio.

    Returns
    -------
    np.ndarray
        Scaled weights targeting the desired volatility.
    """
    weights = np.asarray(weights, dtype=float)
    returns = pd.DataFrame(returns)
    portfolio_returns = returns.dot(weights)
    current_vol = portfolio_returns.std(ddof=1)

    if current_vol <= 0:
        return weights

    scale = target_volatility / current_vol
    return weights * scale


def check_limits(
    weights: np.ndarray, weight_limit: float = 0.2, leverage_limit: float = 1.0
) -> Dict[str, bool]:
    """Check basic portfolio limits.

    Parameters
    ----------
    weights : np.ndarray
        Portfolio weights.
    weight_limit : float, optional
        Maximum absolute position size per asset, by default 0.2.
    leverage_limit : float, optional
        Maximum total absolute exposure, by default 1.0.

    Returns
    -------
    dict
        Dictionary indicating whether any limits have been breached.
    """
    weights = np.asarray(weights, dtype=float)
    breaches = {
        "weight_limit": bool(np.any(np.abs(weights) > weight_limit)),
        "leverage_limit": bool(np.sum(np.abs(weights)) > leverage_limit),
    }
    return breaches


def evaluate_risk(
    weights: np.ndarray,
    returns: pd.DataFrame,
    confidence_level: float = 0.95,
    target_volatility: Optional[float] = None,
    weight_limit: float = 0.2,
    leverage_limit: float = 1.0,
) -> Dict[str, object]:
    """Evaluate risk metrics for a portfolio.

    This function combines VaR/CVaR calculations, volatility targeting and
    limit checks. It is intended to be used after portfolio allocation or
    selection steps to ensure the resulting portfolio is within risk
    tolerance.

    Parameters
    ----------
    weights : np.ndarray
        Portfolio weights.
    returns : pd.DataFrame
        Historical asset returns used to evaluate risk.
    confidence_level : float, optional
        Confidence level for VaR/CVaR, by default 0.95.
    target_volatility : float | None, optional
        Target portfolio volatility. If provided, weights are scaled to meet
        this volatility, by default None.
    weight_limit : float, optional
        Maximum absolute position size per asset, by default 0.2.
    leverage_limit : float, optional
        Maximum total absolute exposure, by default 1.0.

    Returns
    -------
    dict
        Dictionary containing scaled weights, VaR, CVaR, volatility and limit
        breaches.
    """
    weights = np.asarray(weights, dtype=float)
    returns = pd.DataFrame(returns)

    # Apply volatility targeting if requested
    scaled_weights = (
        apply_volatility_targeting(weights, returns, target_volatility)
        if target_volatility is not None
        else weights
    )

    portfolio_returns = returns.dot(scaled_weights)
    var_value = calculate_var(portfolio_returns, confidence_level)
    cvar_value = calculate_cvar(portfolio_returns, confidence_level)
    volatility = portfolio_returns.std(ddof=1)
    breaches = check_limits(scaled_weights, weight_limit, leverage_limit)

    return {
        "weights": scaled_weights,
        "var": var_value,
        "cvar": cvar_value,
        "volatility": volatility,
        "limit_breaches": breaches,
    }


__all__ = [
    "calculate_var",
    "calculate_cvar",
    "apply_volatility_targeting",
    "check_limits",
    "evaluate_risk",
]
