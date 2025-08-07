"""Asset allocation using simple machine learning predicted returns.

This script loads historical asset returns and factor features from the
``input/`` directory, fits a linear model to predict next period returns
for each asset, and performs a mean-variance optimisation to allocate
capital across assets. The optimisation here is the classic closed-form
solution using the inverse covariance matrix.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

CAPITAL = 3000  # euros to allocate


def load_data(input_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load returns and factor features from ``input_dir``.

    Parameters
    ----------
    input_dir: Path
        Directory containing ``returns.csv`` and ``factors.csv``.

    Returns
    -------
    Tuple of returns (DataFrame) and factors (DataFrame) indexed by date.
    """
    returns = pd.read_csv(
        input_dir / "returns.csv", parse_dates=["date"]
    ).set_index("date")
    factors = pd.read_csv(
        input_dir / "factors.csv", parse_dates=["date"]
    ).set_index("date")
    return returns, factors


def predict_returns(
    returns: pd.DataFrame, factors: pd.DataFrame
) -> tuple[pd.Series, np.ndarray]:
    """Predict next-period returns using a linear regression model.

    Uses all but the last observation for training and the final row of
    factor values for prediction.

    Returns
    -------
    predicted_returns: pd.Series
        Predicted return for each asset.
    cov_matrix: np.ndarray
        Sample covariance matrix of training returns.
    """
    if not returns.index.equals(factors.index):
        raise ValueError("Returns and factors must share the same dates")

    X_train = factors.iloc[:-1].values
    X_pred = factors.iloc[-1].values
    X = np.column_stack([np.ones(len(X_train)), X_train])

    predicted = {}
    for asset in returns.columns:
        y = returns.iloc[:-1][asset].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        predicted[asset] = float(np.dot(np.r_[1, X_pred], beta))

    cov_matrix = returns.iloc[:-1].cov().values
    return pd.Series(predicted), cov_matrix


def mean_variance_weights(mu: pd.Series, cov: np.ndarray) -> pd.Series:
    """Compute mean-variance optimal weights.

    We use the classical solution ``w = Σ⁻¹ μ`` normalised to sum to one.
    """
    inv_cov = np.linalg.inv(cov)
    raw = inv_cov @ mu.values
    weights = raw / raw.sum()
    return pd.Series(weights, index=mu.index)


def main() -> None:
    input_dir = Path(__file__).resolve().parents[2] / "input"
    returns, factors = load_data(input_dir)
    mu, cov = predict_returns(returns, factors)
    weights = mean_variance_weights(mu, cov)

    allocation = weights * CAPITAL
    expected_return = float(weights @ mu)
    expected_risk = float(np.sqrt(weights.values @ cov @ weights.values))

    print("Predicted returns:")
    print(mu)
    print("\nPortfolio weights:")
    print(weights)
    print("\nCapital allocation (EUR):")
    print(allocation)
    print(
        f"\nExpected portfolio return: {expected_return:.4f}\n"
        f"Expected portfolio risk (stdev): {expected_risk:.4f}"
    )


if __name__ == "__main__":
    main()
