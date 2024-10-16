import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
# Load the data
def change_to_inputFolder():
    # Get the directory of the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate up two levels
    grandparent_dir = os.path.dirname(os.path.dirname(script_dir))
    # Specify the target folder in the grandparent directory
    target_folder = os.path.join(grandparent_dir, 'input')
    print(os.listdir(target_folder))
    return target_folder
    # current_path = os.getcwd()
    # input_path = os.path.join(current_path, 'input')
    # os.chdir()

def load_data():
    target_folder = change_to_inputFolder()
    
    # data = pd.read_csv(os.path.join(target_folder)) 
    # for file in os.listdir(target_folder)
    
    return data

change_to_inputFolder()

