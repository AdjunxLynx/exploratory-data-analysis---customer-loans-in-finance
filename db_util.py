# modules
import warnings

# Custom classes
from DFInfo import DataFrameInfo
from Connector import RDSDatabaseConnector
from GraphPlotter import Plotter
from DFTransform import DataFrameTransform
from DTransform import DataTransform


if __name__ == "__main__":
    # to stop spam of deprecated feature
    warnings.simplefilter(action="ignore", category=FutureWarning) 
    #connects to online server, downloads the database, and stores in a file called loan_payments.csv
    rdsdbc = RDSDatabaseConnector()
    dataframe = rdsdbc.download_df()

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


