"""Selection utilities for alternative assets.

This module provides a basic momentum‑based strategy which can be used
for alternative asset classes such as commodities or currencies.  The
interface returns a list of assets with the strongest positive momentum.
"""

from __future__ import annotations

from typing import List

import pandas as pd


def select_alternatives(
    prices: pd.DataFrame, window: int = 60, top_n: int = 5
) -> List[str]:
    """Select alternative assets using a simple momentum signal.

    Parameters
    ----------
    prices : pandas.DataFrame
        Price series with assets in columns and time in rows.
    window : int, optional
        Look‑back window for momentum calculation, by default 60.
    top_n : int, optional
        Number of assets to return, by default 5.

    Returns
    -------
    list of str
        The ``top_n`` assets with the highest momentum.
    """

    momentum = prices.pct_change(window).iloc[-1]
    return list(momentum.nlargest(top_n).index)
