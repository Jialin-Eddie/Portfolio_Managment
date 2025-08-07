"""Fixed income selection utilities.

This module implements a minimal example of a fixed income selection
model using yield‑curve changes and credit spread information.  The
interface returns a list of selected bonds based on a simple scoring
metric that combines carry and spread momentum.
"""

from __future__ import annotations

from typing import List

import pandas as pd


def select_fixed_income(
    yields: pd.DataFrame,
    credit_spreads: pd.DataFrame,
    top_n: int = 10,
) -> List[str]:
    """Select bonds using yield‑curve and credit spread signals.

    Parameters
    ----------
    yields : pandas.DataFrame
        Bond yields with assets in columns and time in rows.
    credit_spreads : pandas.DataFrame
        Credit spread data aligned with ``yields``.
    top_n : int, optional
        Number of assets to return, by default 10.

    Returns
    -------
    list of str
        The ``top_n`` bonds with the most attractive combined score.
    """

    # Carry: prefer higher current yield.
    carry = yields.iloc[-1]
    # Spread momentum: improving (decreasing) spreads are positive.
    spread_mom = -credit_spreads.diff().iloc[-1]
    score = carry + spread_mom
    return list(score.nlargest(top_n).index)
