import pandas as pd 


class HedgeFund:
    def __init__(self, name: str, *args, **kwargs):
        self.name = name
        self.beta = None
        self.alpha = None
        self.R_squared = None
        self.t_stat = None


    def __str__(self):
        return ' (HF)' + self.name 
    
    def calculate_CAPM(self, HF_returns: pd.DataFrame, M_ER_country: pd.DataFrame):
        pass
    
    def calculate_FF4(self, HF_returns: pd.DataFrame, Emp_factors: pd.DataFrame):
        pass    

    def calculate_FF5(self, HF_returns: pd.DataFrame, Emp_factors: pd.DataFrame):
        pass


