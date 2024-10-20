import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import openpyxl
# Load the data
def change_to_inputFolder():
    # Get the directory of the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate up two levels
    grandparent_dir = os.path.dirname(os.path.dirname(script_dir))
    # Specify the target folder in the grandparent directory
    target_folder = os.path.join(grandparent_dir, 'input')
    # print(os.listdir(target_folder))
    return target_folder
    # current_path = os.getcwd()
    # input_path = os.path.join(current_path, 'input')
    # os.chdir()

def load_data(file_name: str, start_row: int = 0):
    target_folder = change_to_inputFolder()
    file_path = os.path.join(target_folder, file_name)
    
    if file_name.endswith('.xlsx'):
        # Use pd.read_excel() for Excel files
        data = pd.read_excel(file_path, skiprows=start_row)
    elif file_name.endswith('.csv'):
        # Use pd.read_csv() for CSV files, with error handling
        try:
            data = pd.read_csv(file_path, skiprows=start_row)
        except UnicodeDecodeError:
            # If UTF-8 fails, try 'latin-1' encoding
            data = pd.read_csv(file_path, encoding='latin-1', skiprows=start_row)
    else:
        raise ValueError(f"Unsupported file format: {file_name}")
    
    return data

def output_print():
    return "this is helper"

if __name__ == "__main__":
    print(" Hello World")



