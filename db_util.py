from pandasgui import show
import yaml
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text




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

class RDSDatabaseConnector():
    def __init__(self, credentials):
        url = ("postgresql+psycopg2://" + str(credentials["RDS_USER"]) + ":" + str(credentials["RDS_PASSWORD"]) + "@" + str(credentials["RDS_HOST"]) + "/" + str(credentials["RDS_DATABASE"]))
        self.engine = create_engine(url)

    def database_to_pandas_dataframe(self):
        """uses SQLAlchemy engine to connect to online database, download all data in the table and to return as a pandas dataframe"""
        with self.engine.connect() as conn:
            database = conn.execute(text("SELECT * FROM loan_payments"))
            dataframe = pd.DataFrame(data = database)
            return dataframe

class DataTransform():
    def __init__(self):
        pass

    def call_all_cleaners(self, dataframe):
        """puts all the dataframe cleaning function into one callable function"""
        numeric_list = ["id", "member_id", "loan_amount", "funded_amount", "funded_amount_inv", "term",  "int_rate", "instalment", "employment_length", "annual_inc", "dti", "delinq_2yrs", "inq_last_6mths", "mths_since_last_delinq",  "open_accounts", "total_accounts", "out_prncp", "out_prncp_inv", "total_payment", "total_payment_inv", "total_rec_prncp", "total_rec_int", "total_rec_late_fee", "recoveries", "collection_recovery_fee", "last_payment_amount", "collections_12_mths_ex_med", "mths_since_last_major_derog"]
        date_list = ["issue_date", "earliest_credit_line", "last_payment_date", "next_payment_date", "last_credit_pull_date"]
        
        dataframe = self.set_column_to_custom(dataframe)
        dataframe = self.set_column_to_date(dataframe, date_list)

        dataframe = self.set_numeric(dataframe, numeric_list)
        dataframe = self.set_qualitative(dataframe)
        dataframe = dataframe.rename(columns = {"Unnamed: 0": "Index"})
        dataframe = dataframe.set_index("Index")

        #print(dataframe.info())

        return(dataframe)

    def set_numeric(self, dataframe, numeric_list):
        """turns all columns listed in numeric_list in the dataframe given to a numeric dtype"""
        for column in numeric_list:
            
            dataframe[column] = pd.to_numeric(dataframe[column], errors = "coerce", downcast = "integer")
            dataframe[column] = dataframe[column].round()
            dataframe[column] = dataframe[column].apply(lambda x: round(x) if not pd.isnull(x) else x).astype("Int64")

        return(dataframe)
    
    def set_qualitative(self, dataframe):
            """creates new catagorical dtypes of each qualitative column, and sets that column as the new dtype to save space.
            some dtypes are also ordered"""

            A_to_G = ["A", "B", "C", "D", "E", "F", "G"]

            sub_grade = [] 
            for letter in A_to_G:
                for number in range(1,6):
                    sub_grade.append((letter + str(number)))

            home_ownership_list = ["OWN", "RENT", "MORTGAGE", "OTHER", "NOT GIVEN"]
            verification_status = ["Verified", "Source Verified", "Not Verified"]
            payment_plan_list = ["y", "n"]
            application_list = ["INDIVIDUAL"]
            employment_length_list = ["<1", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", ">10"]
            loan_status_list = ["Fully Paid", "In Grace Period", "Charged Off", "Current", "Default", "Late (16-30 days)", "Late (31-120 days)", "Does not meet the credit policy. Status:Fully Paid", "Does not meet the credit policy. Status:Charged Off"]
            purpose_list = ["car", "credit_card", "debt_consolidation", "educational", "home_improvement", "house", "major_purchase", "medical", "moving", "other", "renewable_energy", "small_business", "vacation", "wedding"]

            grade_dtype = pd.CategoricalDtype(categories = A_to_G, ordered = True)
            sub_grade_dtype = pd.CategoricalDtype(categories = sub_grade, ordered = True)
            home_ownership_dtype = pd.CategoricalDtype(categories = home_ownership_list)
            verification_dtype = pd.CategoricalDtype(categories = verification_status)
            loan_status_dtype = pd.CategoricalDtype(categories = loan_status_list)
            payment_plan_dtype = pd.CategoricalDtype(categories = payment_plan_list)
            purpose_dtype = pd.CategoricalDtype(categories = purpose_list)
            application_dtype = pd.CategoricalDtype(categories = application_list)
            employ_length_dtype = pd.CategoricalDtype(categories = employment_length_list, ordered = True)


            dataframe["grade"] = dataframe["grade"].astype(grade_dtype)
            dataframe["sub_grade"] = dataframe["sub_grade"].astype(sub_grade_dtype)
            dataframe["home_ownership"] = dataframe["home_ownership"].astype(home_ownership_dtype)
            dataframe["verification_status"] = dataframe["verification_status"].astype(verification_dtype)
            dataframe["loan_status"] = dataframe["loan_status"].astype(loan_status_dtype)
            dataframe["payment_plan"] = dataframe["payment_plan"].astype(payment_plan_dtype)
            dataframe["purpose"] = dataframe["purpose"].astype(purpose_dtype)
            dataframe["application_type"] = dataframe["application_type"].astype(application_dtype)
            dataframe["employment_length"] = dataframe["employment_length"].astype(employ_length_dtype)

            

            return(dataframe)

    def set_column_to_date(self, dataframe, date_list):
        """sets a list of column names to dtype datetime in the dataframe given"""
        for column in date_list:
            dataframe[column] = pd.to_datetime(dataframe[column], errors = "coerce", format="%Y-%m-%d").dt.date
        return(dataframe)

    def set_column_to_custom(self, dataframe):
        """sets seperate columns to appropriate dtypes and cleans them using the dataframe given"""

        dataframe["term"] = dataframe["term"].str.replace("\D", "", regex = True)
        dataframe["employment_length"] = dataframe["employment_length"].apply(self.clean_employment_length)
        dataframe["employment_length"] = dataframe["employment_length"].str.replace("[^0-9<>]", "", regex = True)
        dataframe["policy_code"] = dataframe["policy_code"].astype(str)
        dataframe["policy_code"] = dataframe["policy_code"].str.replace("1", "Available")
        dataframe["policy_code"] = dataframe["policy_code"].str.replace("0", "Not Available")

        return(dataframe)

    def clean_employment_length(self, length):
        """this function is a quick filter to replace the value in employment_length to the correct value, shortening the value and making it ready for categorising"""
        if length == "< 1 year":
            return ("<1")
        elif length == "10+ years":
            return (">10")
        else:
            return length


class DataFrameInfo():
    def __init__(self):
        pass
    
    def call_all_information(self, dataframe):
        """Calls all functions that analyses dataframe, and shows that as a smaller dataframe"""
        self.describe_all_columns(dataframe)
        statistics_dataframe = self.get_statistics(dataframe)
        show(statistics_dataframe)
        self.get_shape(dataframe)
        self.show_null_barchart(dataframe)

        return dataframe

    def describe_all_columns(self, dataframe):
        """prints analysis on the dataframe, giving quick information on the dataframe"""
        print(dataframe.describe(percentiles = [.5]))
    
    def get_distinct_categories(self, dataframe):
        """Gets a list of all columns in the current dataframe with dtype of category
        then counts the distinct values in these columns. 
        returns a DataFrame with NaN values where the column dtype is not of category,
        and then the distinct count when the column dtype is"""
        headers = self.get_column_headers(dataframe)
        categorical_columns = dataframe.select_dtypes(include=["category"]).columns.tolist()
        distinct_values_count = {}

        for column in dataframe.columns:
            if column in categorical_columns:
                distinct_values_count[column] = dataframe[column].nunique()
            else:
                distinct_values_count[column] = np.nan

        distinct_values_df = pd.DataFrame.from_dict(distinct_values_count, orient="index", columns=["Distinct_Values_Count"])
        distinct_values_df.index.name = "Column_Name"

        return distinct_values_df

    def get_statistics(self, dataframe):
        """returns a Dataframe from the inputted Dataframe, giving statistical data on the Dataframe such as
        non-null count, mean value of all the data in a column, minimum value, maximum value, standard deviation of the column
        median value of column, percentage of value that is Null (np.NaN), amount of distinct values in categorical columns, most frequent value"""

        count = dataframe.count()
        mode = self.get_mode(dataframe)
        mean = dataframe.select_dtypes(include=["int64", "float64"]).mean()
        min = dataframe.select_dtypes(include=["int64", "float64"]).min()
        max = dataframe.select_dtypes(include=["int64", "float64"]).max()
        std = dataframe.select_dtypes(include=["int64", "float64"]).std()
        med = dataframe.select_dtypes(include=["int64", "float64"]).median()
        null_percentage_df = self.get_null_percentage(dataframe)
        distinct_df = self.get_distinct_categories(dataframe)

        dataframes = [count, mean, min, max, std, med, mode, null_percentage_df, distinct_df]
        statistical_df = pd.concat(dataframes, axis = 1)
        statistical_df = statistical_df.rename(columns={0: "Count", 1: "Mean", 2: "Min", 3: "Max", 4: "Standard Deviation", 5: "Median"}, errors = "raise")
        return statistical_df
    
    def get_mode(self, dataframe):
        """returns the most frequent value for each column in the given dataframe"""
        mode_series = dataframe.mode().iloc[0]
        mode_df = pd.DataFrame({"Mode": mode_series})
        return mode_df

    def show_null_barchart(self, dataframe):
        """shows a barchart of all the columns and their percentage of values that are null"""
        plt.figure(figsize=(10, 6))

        # Calculate the percentage of missing values for each column
        missing_percentage = dataframe.isnull().mean() * 100  
        # Filter columns with missing values
        missing_percentage = missing_percentage[missing_percentage > 0]  

        missing_percentage.plot(kind="bar")
        plt.xlabel("Columns")
        plt.ylabel("Percentage of Missing Values")
        plt.title("Percentage of Missing Values in Columns")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def get_null_percentage(self, dataframe):
        """returns the percentage of null values in the column"""
        headers = self.get_column_headers(dataframe)
        percentage_list = []

        for column_name in headers:
            null_count = dataframe[column_name].isnull().sum()
            total_count = len(dataframe[column_name]) 
            percentage = ((null_count / total_count) * 100)
            percentage_list.append(percentage)

        null_percentage_series = pd.Series(percentage_list, index=headers)
        null_percentage_df = pd.DataFrame(null_percentage_series, columns=["Null Percentages"])
        return null_percentage_df

    def get_column_headers(self, dataframe):
        """returns a list of the column titles from the dataframe given"""
        column_names = dataframe.columns.tolist()

        return column_names

    def get_shape(self, dataframe):
        """prints the shape (dimension) of the dataframe given"""
        print("The Dataframe Shape is: " , dataframe.shape)



class Plotter:
    
    def __init__(self):
        pass



    def plot_nulls_before_after(self, before, after):
        """creates two barcharts of the columns in the dataframe, before and after they have been cleaned of all null values. shows them side by side"""
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        before.plot.bar(ax=ax[0], title="Null Values Before")
        after.plot.bar(ax=ax[1], title="Null Values After")
        plt.show()   



class DataFrameTransform:
    def __init__(self):
        pass
    
    def count_nulls(self, dataframe):
        return dataframe.isnull().sum()

    def drop_columns(self, dataframe, threshold=0.5):
        """this function drops all columns where the null value percentage is above a given %, default being 50%"""
        columns_to_drop = [column for column in dataframe.columns if dataframe[column].isnull().mean() > threshold]
        return dataframe.drop(columns=columns_to_drop, axis=1)

    def impute_columns(self, dataframe):
        """For quantative data, imputes data into columns by the column mean, for qualitative, imputes by the most frequent"""
        for column in dataframe.columns:
            if dataframe[column].dtype == 'float64' or dataframe[column].dtype == 'int64':
                dataframe[column].fillna(dataframe[column].mean(), inplace=True)
            else:
                dataframe[column].fillna(dataframe[column].mode()[0], inplace=True)
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


