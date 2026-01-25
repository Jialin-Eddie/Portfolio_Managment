# CLAUDE.md - AI Assistant Guide for Portfolio Management Project

## Project Overview

This is a **quantitative portfolio management framework** for financial analysis, portfolio construction, and backtesting. It implements multi-asset class selection strategies, risk management utilities, and performance evaluation tools.

**Contact:** jialin.zhao@fs-students.de

## Quick Start Commands

```bash
# Activate virtual environment (PowerShell/Windows)
.venv/Scripts/Activate

# Activate virtual environment (Unix/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirement.txt

# Run tests
pytest

# Check code style
flake8 src/
black --check src/
mypy src/
```

## Codebase Structure

```
Portfolio_Managment/
├── src/                              # Source code
│   ├── portfolioConstruction/        # Core portfolio algorithms (main module)
│   │   ├── __init__.py               # Exports: select_equities, select_fixed_income, select_alternatives
│   │   ├── asset_allocation_ml.py    # ML-based return prediction & mean-variance optimization
│   │   ├── barra_equity_selector.py  # BARRA factor model for equity selection
│   │   ├── fixed_income_selection.py # Bond selection (carry + credit momentum)
│   │   ├── alternatives_selection.py # Momentum-based alternatives selection
│   │   ├── risk_management.py        # VaR, CVaR, volatility targeting, limit checks
│   │   ├── Portfolio_Construct.ipynb # Main backtesting notebook
│   │   └── Portfolio_Construct_BT.ipynb
│   ├── helper/                       # Utility functions
│   │   ├── helper.py                 # Data loading, path utilities
│   │   ├── hedgeFund.py              # Hedge fund analysis class
│   │   └── visulize.py               # Visualization utilities
│   ├── hedgeFund/                    # Hedge fund analysis notebooks
│   │   └── hedgeFund.ipynb           # Hedge fund performance analysis
│   ├── international_ltm/            # International momentum strategies
│   │   └── Long_Momentum_Analysis.ipynb
│   └── chatGPT/                      # ChatGPT integration (minimal)
├── input/                            # Data files (gitignored)
├── output/                           # Results: pickle files, PNG visualizations
├── requirement.txt                   # Python dependencies
├── install.ps1                       # Windows setup script
└── README.md                         # Project documentation
```

## Key Modules & Functions

### portfolioConstruction/risk_management.py
The most comprehensive module with risk utilities:
- `calculate_var(portfolio_returns, confidence_level)` - Historical Value at Risk
- `calculate_cvar(portfolio_returns, confidence_level)` - Conditional VaR (Expected Shortfall)
- `apply_volatility_targeting(weights, returns, target_volatility)` - Scale weights to target vol
- `check_limits(weights, weight_limit, leverage_limit)` - Position/leverage limit checks
- `evaluate_risk(...)` - Combined risk evaluation returning VaR, CVaR, volatility, breaches

### portfolioConstruction/asset_allocation_ml.py
- `load_data(input_dir)` - Load returns.csv and factors.csv
- `predict_returns(returns, factors)` - Linear regression return prediction
- `mean_variance_weights(mu, cov)` - Classical Σ⁻¹μ optimization
- Default capital allocation: €3000

### portfolioConstruction/barra_equity_selector.py
- `compute_factor_exposures(returns, factors)` - OLS regression for factor betas
- `compute_idiosyncratic_risk(returns, factors, exposures)` - Residual variance
- `optimize_selection(returns, factors, n)` - Risk-adjusted ranking, returns top N equities

### portfolioConstruction/fixed_income_selection.py
- `select_fixed_income(carry_scores, momentum_scores, n)` - Combined carry + momentum ranking

### portfolioConstruction/alternatives_selection.py
- `select_alternatives(prices, n, lookback)` - Momentum-based selection (default: 60-day, top 5)

### helper/helper.py
- `change_to_inputFolder()` - Navigate to input directory
- `load_data(file_name, start_row)` - Load Excel/CSV with encoding fallback

## Technology Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.x |
| Data Analysis | pandas 1.3.3, numpy 1.21.2 |
| Visualization | matplotlib, seaborn |
| Testing | pytest 6.2.5 |
| Linting | flake8 3.9.2, black 21.9b0 |
| Type Checking | mypy 0.910 |
| Documentation | sphinx 4.2.0 |

## Code Style & Conventions

### Docstrings
Use **NumPy-style docstrings** with Parameters, Returns sections:
```python
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
```

### Type Hints
Always include type hints for function parameters and return values:
```python
from typing import Optional, Dict
import pandas as pd
import numpy as np

def evaluate_risk(
    weights: np.ndarray,
    returns: pd.DataFrame,
    confidence_level: float = 0.95,
    target_volatility: Optional[float] = None,
) -> Dict[str, object]:
```

### Module Exports
Use `__all__` to explicitly define public API:
```python
__all__ = [
    "calculate_var",
    "calculate_cvar",
    "apply_volatility_targeting",
]
```

### Code Discipline (from README)
1. **Avoid deep nesting** - Use inversion, merge, extraction techniques
2. **Avoid code duplication** - Extract common functionality
3. **Name functions meaningfully** - Use descriptive, action-oriented names

### Data Handling
- Input data goes in `input/` directory (gitignored)
- Output artifacts go in `output/` directory
- Use `pd.DataFrame` for tabular data, `pd.Series` for single columns
- Use `np.ndarray` for numerical computations

## Git Workflow

### Branch Naming
Feature branches follow the pattern: `codex/<feature-description>` or `claude/<feature-description>`

### Commit Style
Concise, descriptive messages:
- `Add risk management utilities with VaR, CVaR and limit checks`
- `Add portfolio selection modules`

### Pull Request Process
1. Create feature branch from main
2. Implement changes
3. Submit PR for review
4. Merge via GitHub PR interface

## Testing

### Running Tests
```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest src/hedgeFund/     # Run specific directory
```

### Test Files
- Test files located alongside source: `src/hedgeFund/test.py`
- Jupyter notebooks serve as integration tests

## Common Tasks for AI Assistants

### Adding a New Portfolio Strategy
1. Create new module in `src/portfolioConstruction/`
2. Follow existing pattern (type hints, NumPy docstrings)
3. Add function to `__init__.py` exports
4. Consider adding risk evaluation via `risk_management.evaluate_risk()`

### Adding Risk Metrics
1. Add function to `src/portfolioConstruction/risk_management.py`
2. Include in `__all__` list
3. Optionally integrate into `evaluate_risk()` function

### Working with Jupyter Notebooks
- Main analysis: `src/portfolioConstruction/Portfolio_Construct.ipynb`
- Hedge funds: `src/hedgeFund/hedgeFund.ipynb`
- International momentum: `src/international_ltm/Long_Momentum_Analysis.ipynb`

### Data Loading Pattern
```python
from src.helper.helper import load_data, change_to_inputFolder

# Load Excel file
data = load_data("filename.xlsx")

# Load CSV with row skip
data = load_data("filename.csv", start_row=1)
```

## Key Files to Understand

| Priority | File | Purpose |
|----------|------|---------|
| High | `src/portfolioConstruction/risk_management.py` | Core risk utilities |
| High | `src/portfolioConstruction/asset_allocation_ml.py` | ML allocation model |
| High | `src/portfolioConstruction/Portfolio_Construct.ipynb` | Main backtesting |
| Medium | `src/portfolioConstruction/barra_equity_selector.py` | Factor-based selection |
| Medium | `src/helper/helper.py` | Data loading utilities |
| Low | `src/helper/visulize.py` | Visualization (has hardcoded paths) |

## Known Issues & Notes

1. **Hardcoded paths**: `src/helper/visulize.py` contains Windows-specific paths that need updating
2. **Unused dependencies**: `openai` package installed but not actively used
3. **Test coverage**: pytest configured but test suite is minimal
4. **Sphinx docs**: Not yet built (sphinx configured in requirements)

## Financial Concepts Reference

- **VaR (Value at Risk)**: Maximum expected loss at confidence level
- **CVaR (Conditional VaR)**: Average loss beyond VaR threshold
- **BARRA Model**: Multi-factor equity risk model
- **Mean-Variance Optimization**: Markowitz portfolio theory (Σ⁻¹μ)
- **Sharpe Ratio**: Risk-adjusted return metric
- **Volatility Targeting**: Scaling positions to achieve target risk level
