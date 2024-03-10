import pandas as pd
from pandasgui import show

class DataTransform():
    def __init__(self):
        self.available_list = []
        self.string_list = []
        self.strip_list = []
        self.qualitative_list = []
    
    def call_all_cleaners(self, dataframe):
        """puts all the dataframe cleaning function into one callable function"""
        
        numeric_list = self.get_numeric_list(dataframe)
        date_list = self.get_date_list(dataframe)
        
        dataframe = self.set_column_to_custom(dataframe)
        dataframe = self.set_column_to_date(dataframe, date_list)

        dataframe = self.set_numeric(dataframe, numeric_list)
        dataframe = self.set_qualitative(dataframe,self.qualitative_list)
        dataframe = dataframe.rename(columns = {"Unnamed: 0": "Index"})

        return(dataframe)
    
    def drop_columns_in_series(self, series, columns):
        """Drops all indexs where the index name is in columns list to drop"""
        
        for column in columns:
            try:
                series = series.drop(column)
            except:
                print(f"Error Dropping {column}, Moving On")
        return series
    
    def get_skewed_columns(self, dataframe, qualitative_list, threshold=0.5):
        """Inputs the current dataframe and returns all the columns where the columns are skewed by more than 0.5 (moderately skewed), considering only numeric columns."""
        
        numeric_cols = dataframe.select_dtypes(include=['number'])
        skewed_columns = numeric_cols.skew().where(lambda x: abs(x) > threshold).dropna()
        skewed_columns = skewed_columns.drop(labels=qualitative_list, errors='ignore')
        skewed_columns = skewed_columns.index.tolist()
        return skewed_columns
    
    def get_skewed_dataframe(self, dataframe, skewed_columns):
        """returns the sub frame of dataframe that only includes the columns inputted"""
        
        skewed_dataframe = dataframe[skewed_columns]
        return skewed_dataframe
        
    
    def get_numeric_list(self, dataframe):
        """returns a list of the column names that are numeric"""
        
        numeric_list = ["id", "member_id", "loan_amount", "funded_amount", "funded_amount_inv", "term",  "int_rate", "instalment", "employment_length", "annual_inc", "dti", "delinq_2yrs", "inq_last_6mths", "mths_since_last_delinq",  "open_accounts", "total_accounts", "out_prncp", "out_prncp_inv", "total_payment", "total_payment_inv", "total_rec_prncp", "total_rec_int", "total_rec_late_fee", "recoveries", "collection_recovery_fee", "last_payment_amount", "collections_12_mths_ex_med", "mths_since_last_major_derog"]
        return numeric_list
    
    def get_date_list(self, dataframe):
        """returns a list of the column names that are dates"""
        
        date_list = ["issue_date", "earliest_credit_line", "last_payment_date", "next_payment_date", "last_credit_pull_date"]
        return date_list

    def set_numeric(self, dataframe, numeric_list):
        """turns all columns listed in numeric_list in the dataframe given to a numeric dtype"""
        
        for column in numeric_list:
            
            dataframe[column] = pd.to_numeric(dataframe[column], errors = "coerce", downcast = "integer")
            dataframe[column] = dataframe[column].round()
            dataframe[column] = dataframe[column].apply(lambda x: round(x) if not pd.isnull(x) else x).astype("Int64")

        return(dataframe)

    def set_column_to_date(self, dataframe, date_list):
        """sets a list of column names to dtype datetime in the dataframe given"""
        
        for column in date_list:
            dataframe[column] = pd.to_datetime(dataframe[column], errors = "coerce", format="%Y-%m-%d").dt.date
        return(dataframe)

    def set_column_to_custom(self, dataframe):
        """sets seperate columns to appropriate dtypes and cleans them using the dataframe given"""
        
        dataframe = self.set_column_to_string(dataframe, self.string_list)
        dataframe = self.set_column_to_available_or_not(dataframe, self.available_list)
        dataframe = self.strip_column_to_int(dataframe, self.strip_list)
        dataframe = self.set_qualitative(dataframe, self.qualitative_list)

        return(dataframe)
    
    def strip_column_to_int(self, dataframe, columns):
        """sets all the columns thats match the given columns list, and strips of all characters except integers"""
        
        for column in columns:
            dataframe[column] = dataframe[column].str.replace(r"\D", "", regex=True)
        return dataframe
             
    
    def set_qualitative(self, dataframe, categorical_list):
        """creates new catagorical dtypes of each qualitative column, and sets that column as the new dtype to save space.
        some dtypes are also ordered"""
        
        for column in categorical_list:
            dataframe[column] = pd.Categorical(dataframe[column]).codes
            
        return(dataframe)
    
    
    
    
    def set_column_to_string(self, dataframe, columns):
        """sets all the columns thats match the given columns list to string"""
        
        for column in columns:
            dataframe[column] = dataframe[column].astype(str)
            dataframe[column] = dataframe[column].str.replace(r"\D", "", regex=True)
            
        return dataframe
    
    def set_column_to_available_or_not(self, dataframe, columns):
        """sets all the columns thats match the given columns list to Available or Not Available"""
        
        for column in columns:
            dataframe[column] = dataframe[column].str.replace("1", "Available")
            dataframe[column] = dataframe[column].str.replace("0", "Not Available")
            dataframe[column] = dataframe[column].astype(str)
        return dataframe
    
    def set_available_list(self, list):
        """setter method for class list available_list"""
        
        self.available_list = list
        
    def set_qualitative_list(self, list):
        """setter method for class list available_list"""
        
        self.qualitative_list = list
        
    def set_string_list(self, list):
        """setter method for class list available_list"""
        
        self.string_list = list
    
    def set_strip_list(self, list):
        """setter method for class list available_list"""
        
        self.strip_list = list