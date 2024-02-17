# modules
import warnings
from pandasgui import show

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
    #creates all the classes
    rdsdbc = RDSDatabaseConnector()
    dtransformer = DataTransform()
    dtinfo = DataFrameInfo()
    dftransformer = DataFrameTransform()
    plotter = Plotter()
    
    dataframe = rdsdbc.download_df()
    show(dataframe)
    
    #calls the main function in each data analysis class
    dtransformer.set_available_list(["policy_code"])
    dtransformer.set_string_list(["policy_code", "term"])
    dtransformer.set_strip_list(["term"])
    dtransformer.set_qualitative_list(["purpose", "grade", "sub_grade","home_ownership", "verification_status", "loan_status", "payment_plan", "application_type", "employment_length"])

    
    dataframe = dtransformer.call_all_cleaners(dataframe)
    dataframe = dtinfo.call_all_information(dataframe)

    #calls the plotter and visualises the null value removal
    nulls_before = dftransformer.count_nulls(dataframe)
    dataframe = dftransformer.drop_columns(dataframe)
    dataframe = dftransformer.impute_columns(dataframe)
    nulls_after = dftransformer.count_nulls(dataframe)

    plotter.plot_nulls_before_after(nulls_before, nulls_after)
    
    skewed_dataframe = dtransformer.get_skewed_columns(dataframe)
    plotter.plot_skewed_graph(skewed_dataframe)
    show(dataframe)