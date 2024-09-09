# Custom classes
from DFInfo import DataFrameInfo
from Connector import RDSDatabaseConnector
from GraphPlotter import Plotter
from DFTransform import DataFrameTransform
from DTransform import DataTransform

# modules
import warnings, os
import pandas as pd
from pandasgui import show

class DB_Util:
    def run(self, prnt):
        # to stop spam of deprecated feature 

        #creates all the classes
        rdsdbc = RDSDatabaseConnector()
        dtransformer = DataTransform()
        dfinfo = DataFrameInfo()
        dftransformer = DataFrameTransform()
        plotter = Plotter()

        available_list = ["policy_code"]
        string_list = ["policy_code", "term"]
        strip_list = ["term"]
        qualitative_list = ["purpose", "grade", "sub_grade","home_ownership", "verification_status", "loan_status", "payment_plan", "application_type", "employment_length"]
        outlier_columns = ["funded_amount", "funded_amount_inv", "installment", "open_accounts", "delinq_2yrs", "total_accounts", "total_payment", "total_payment_inv", "total_rec_prncp", "total_rec_int", "last_payment_amount"]
        ignore_list = ['recovery_rate_funded', 'recovery_rate_inv', 'total_payment', 'funded_amount', 'funded_amount_inv', 'instalment', 'last_payment_date', 'next_payment_date']

        dtransformer.set_available_list(available_list)
        dtransformer.set_string_list(string_list)
        dtransformer.set_strip_list(strip_list)
        dtransformer.set_qualitative_list(qualitative_list)

        dataframe = rdsdbc.download_df()
        #connects to online server, downloads the database, and stores in a file called loan_payments.csv

        dataframe = dtransformer.call_all_cleaners(dataframe)

        dataframe = dfinfo.call_all_information(dataframe, prnt)

        #calls the plotter and visualises the null value removal
        nulls_before = dftransformer.count_nulls(dataframe)
        dataframe = dftransformer.drop_columns(dataframe)
        dataframe = dftransformer.impute_columns(dataframe)
        nulls_after = dftransformer.count_nulls(dataframe)

        plotter.plot_nulls_before_after(nulls_before, nulls_after)
        original_dataframe = dataframe

        skewed_columns = dtransformer.get_skewed_columns(dataframe, qualitative_list, 0.5)
        skewed_dataframe = dtransformer.get_skewed_dataframe(dataframe, skewed_columns)
        unskewed_dataframe = dftransformer.remove_skewness(dataframe, qualitative_list, prnt)

        plotter.plot_skewed_vs_unskewed_graph(skewed_dataframe.skew(), unskewed_dataframe.skew(), prnt)

        combined_df = dftransformer.merge_dataframes(dataframe, unskewed_dataframe)
        combined_df.to_csv(os.path.join("script_data", "combined_dataframe.csv"), index=False)
        dataframe = combined_df


        plotter.visualise_outliers(dataframe, outlier_columns, False)
        before = dataframe
        drop_outlier_dictionary = dftransformer.find_closest_outliers(dataframe, outlier_columns, prnt)
        dataframe = dftransformer.drop_outside_bounds(dataframe, drop_outlier_dictionary)
        after = dataframe

        count_before = dftransformer.calculate_outlier_counts(before, outlier_columns)
        count_after = dftransformer.calculate_outlier_counts(after, outlier_columns)
        before_dataframe = pd.DataFrame(data = count_before, index = [0])
        after_dataframe = pd.DataFrame(data = count_after, index = [0])

        plotter.plot_outliers_before_after(before_dataframe, after_dataframe)
        

        matrix_before = dftransformer.get_correlation_matrix(dataframe)
        dataframe = dftransformer.drop_overcorrelated(dataframe, matrix_before, ignore_list)
        dataframe = dftransformer.drop_overcorrelated(dataframe, dftransformer.get_correlation_matrix(dataframe), ignore_list)

        matrix_after = dftransformer.get_correlation_matrix(dataframe)
        plotter.plot_correlation_before_after(matrix_before, matrix_after)

        return original_dataframe, dataframe
        



if __name__ =="__main__":
    #will print all information if True
    try:
        verbose = int(input("Please enter 0 for no output, or 1 for output in console "))
    except:
        pass
    while verbose != 0 and verbose != 1:
        try:
            verbose = int(input("Please enter 0 for no output, or 1 for output in console "))
        except:
            pass
    warnings.filterwarnings("ignore", category=FutureWarning, module="DFInfo")
    #mutes warnings from an error caused by the show() function

    database_util = DB_Util()
    database_util.run(verbose)