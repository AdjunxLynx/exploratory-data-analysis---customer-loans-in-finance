from pandasgui import show
import yaml
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

from DFInfo import DataFrameInfo
from Connector import RDSDatabaseConnector
from GraphPlotter import Plotter
from DFTransform import DataFrameTransform
from DTransform import DataTransform

def load_credentials():
    """loads credentials from a file called 'credentials.yaml' and returns it as a dictionary"""
    with open("credentials.yaml", "r") as file:
        credentials = yaml.safe_load(file)
    return credentials

def save_pd_to_csv(dataframe):
    """takes input parameter and dumps into a file in directory called 'loan_payments.csv'"""
    dataframe.to_csv("loan_payments.csv")

def load_csv_to_pd(filename):
    """takes input filename as parameter and displays file as a large table"""
    dataframe = pd.read_csv(filename)
    return dataframe


if __name__ == "__main__":
    # to stop spam of deprecated feature
    warnings.simplefilter(action="ignore", category=FutureWarning) 

    #connects to online server, downloads the database, and stores in a file called loan_payments.csv
    rdsdbc = RDSDatabaseConnector(load_credentials())
    save_pd_to_csv(rdsdbc.database_to_pandas_dataframe())
    dataframe = load_csv_to_pd("loan_payments.csv")

    #creates all the classes
    dtransformer = DataTransform()
    dtinfo = DataFrameInfo()
    dftransformer = DataFrameTransform()
    plotter = Plotter()


    #calls the main function in each data analysis class
    dataframe = dtransformer.call_all_cleaners(dataframe)
    dataframe = dtinfo.call_all_information(dataframe)

    #calls the plotter and visualises the null value removal
    nulls_before = dftransformer.count_nulls(dataframe)

    dataframe = dftransformer.drop_columns(dataframe)
    dataframe = dftransformer.impute_columns(dataframe)

    nulls_after = dftransformer.count_nulls(dataframe)

    plotter.plot_nulls_before_after(nulls_before, nulls_after)


