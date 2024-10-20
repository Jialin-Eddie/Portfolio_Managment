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
    print("in the test")
    print(os.listdir(target_folder))
    return target_folder
    # current_path = os.getcwd()
    # input_path = os.path.join(current_path, 'input')
    # os.chdir()


# src/.helper/test.py
def greet():
    return "Hello from test.py!"

if __name__ == "__main__":
    print(greet())

