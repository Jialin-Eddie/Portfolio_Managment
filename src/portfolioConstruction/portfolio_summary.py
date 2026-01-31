"""Portfolio summary report.

This module loads precomputed allocation weights, performance metrics and
risk statistics from the ``output`` directory and produces a set of
summary tables and charts.  The resulting visualisations are written
back to the ``output`` directory and a brief textual interpretation is
printed to the console.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return allocation weights and performance metrics.

    The function expects pickle files produced by the existing notebooks:
    ``Part3_diff_strategy.pickle`` contains allocation weights for a set of
    portfolio construction strategies, while ``Part3_Af_perform.pickle``
    stores their associated performance and risk metrics.
    """

    allocation = pd.read_pickle(OUTPUT_DIR / "Part3_diff_strategy.pickle")
    performance = pd.read_pickle(OUTPUT_DIR / "Part3_Af_perform.pickle")
    return allocation, performance


def create_summary_table(allocation: pd.DataFrame, performance: pd.DataFrame) -> pd.DataFrame:
    """Combine allocation statistics with performance metrics.

    Parameters
    ----------
    allocation:
        DataFrame whose rows correspond to strategies and columns to asset
        tickers.  Values represent portfolio weights.
    performance:
        DataFrame whose columns correspond to strategies and rows contain
        metrics such as annual return and Sharpe ratio.

    Returns
    -------
    DataFrame
        Table indexed by strategy with performance metrics as well as
        simple allocation statistics (number of assets held and largest
        single weight).
    """

    perf = performance.T
    perf.index.name = "strategy"
    perf.reset_index(inplace=True)

    alloc_stats = (
        allocation.apply(
            lambda col: pd.Series({
                "Num Assets": (col != 0).sum(),
                "Largest Weight": col.max(),
            }),
            axis=1,
        )
        .reset_index()
        .rename(columns={"index": "strategy"})
    )

    summary = perf.merge(alloc_stats, on="strategy", how="left")
    return summary


def plot_performance(summary: pd.DataFrame) -> None:
    """Create bar charts for key performance and risk metrics."""

    metrics = ["Annu_return", "Volatility", "Sharpe Ratio", "Maximum drawdown"]
    for metric in metrics:
        ax = summary.plot.bar(x="strategy", y=metric, legend=False)
        ax.set_ylabel(metric.replace("_", " ").title())
        ax.set_title(f"{metric.replace('_', ' ').title()} by Strategy")
        fig = ax.get_figure()
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / f"{metric}_by_strategy.png")
        plt.close(fig)


def plot_allocation(allocation: pd.DataFrame) -> None:
    """Visualise portfolio weights across strategies as a heatmap."""

    plt.figure(figsize=(12, 6))
    sns.heatmap(allocation, cmap="viridis")
    plt.title("Asset Allocation by Strategy")
    plt.xlabel("Ticker")
    plt.ylabel("Strategy")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "allocation_heatmap.png")
    plt.close()


def generate_text_summary(summary: pd.DataFrame) -> str:
    """Return a short interpretation of strategy performance."""

    sharpe_row = summary.loc[summary["Sharpe Ratio"].idxmax()]
    drawdown_row = summary.loc[summary["Maximum drawdown"].idxmin()]
    return (
        f"Best risk-adjusted return: {sharpe_row['strategy']} "
        f"(Sharpe {sharpe_row['Sharpe Ratio']:.2f}).\n"
        f"Lowest drawdown: {drawdown_row['strategy']} "
        f"(Max drawdown {drawdown_row['Maximum drawdown']:.2%})."
    )


def main() -> None:
    """Entry point for generating the portfolio summary."""

    allocation, performance = load_data()
    summary = create_summary_table(allocation, performance)

    print("Summary table:\n", summary)
    summary.to_csv(OUTPUT_DIR / "portfolio_summary.csv", index=False)

    plot_performance(summary)
    plot_allocation(allocation)

    interpretation = generate_text_summary(summary)
    print("\nInterpretation:\n" + interpretation)


if __name__ == "__main__":
    main()
