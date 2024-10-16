import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

# Ensure the script's directory is the current working directory
script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)

# Define the relative path to the input directory
input_dir = Path(r'E:\zhaoj\download\workSpace\input')

# Define the Excel file names
djia_returns_file = 'HW_Hedge_Fund.xlsx'
sp500_prices_file = 'HW_World.xlsx'
sp500_returns_file = 'HW_Factors.xlsx'
djia_prices_file = 'HW_DJIA_Prices.xlsx'

# Function to read Excel file and return DataFrame
def read_excel_file(file_name):
    file_path = input_dir / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_name} does not exist in the input directory.")
    return pd.read_excel(file_path)

# Read all Excel files into separate DataFrames
try:
    djia_returns_df = read_excel_file(djia_returns_file)
    sp500_prices_df = read_excel_file(sp500_prices_file)
    sp500_returns_df = read_excel_file(sp500_returns_file)
    djia_prices_df = read_excel_file(djia_prices_file)
    print(djia_prices_df.head())
    print("All files have been successfully read.")

    # Set the style for all plots
    plt.style.available
    plt.style.use("seaborn-v0_8-whitegrid")

    # 1. Visualize HW_Factors.xls (sp500_returns_df)
    plt.figure(figsize=(12, 6))
    #sns.lineplot(data=sp500_returns_df[['Mkt-RF', 'SMB', 'HML', 'MOM','RF']])
    plt.title('Empirical Factors Monthly Returns')
    plt.xlabel('Date')
    plt.ylabel('Returns (%)')
    plt.legend(title='Factors')
    plt.savefig('empirical_factors_returns.png')
    plt.close()

    # 2. Visualize HW_Hedge Fund.xls (djia_returns_df)
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=djia_returns_df.iloc[:, 1:])  # Assuming the first column is the date
    plt.title('Hedge Fund Indexes Monthly Returns')
    plt.xlabel('Date')
    plt.ylabel('Returns (%)')
    plt.legend(title='Hedge Fund Indexes', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('hedge_fund_indexes_returns.png')
    plt.close()

    # 3. Visualize HW_World.xls (sp500_prices_df)
    countries = ['USA', 'JPN', 'GBR', 'FRA', 'DEU']
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sp500_prices_df[countries])
    plt.title('Monthly Equity Returns of Selected Developed Countries')
    plt.xlabel('Date')
    plt.ylabel('Returns (USD)')
    plt.legend(title='Countries', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('developed_countries_returns.png')
    plt.close()

    # 4. Visualize HW_DJIA Prices.xls (djia_prices_df)
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=djia_prices_df.iloc[:, 0], y=djia_prices_df.iloc[:, -1])
    plt.title('Dow Jones Industrial Average (DJIA) Index')
    plt.xlabel('Date')
    plt.ylabel('Index Value')
    plt.savefig('djia_index.png')
    plt.close()

    # Plot stock prices for a few selected companies
    selected_companies = ['AAPL', 'MSFT', 'JNJ', 'WMT', 'PG']
    plt.figure(figsize=(12, 6))
    for company in selected_companies:
        if company in djia_prices_df.columns:
            sns.lineplot(x=djia_prices_df.iloc[:, 0], y=djia_prices_df[company], label=company)
    plt.title('Stock Prices of Selected DJIA Companies')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')
    plt.legend(title='Companies', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('selected_djia_companies.png')
    plt.close()

    print("All visualizations have been saved as PNG files.")

except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please ensure all required files are in the 'input' directory relative to this script.")

