import numpy as np
import pandas as pd
import warnings

class DataFrameInfo():
    def call_all_information(self, dataframe):
        """Calls all functions that analyses dataframe, and shows that as a smaller dataframe"""
        
        try:
            dataframe = dataframe.drop(columns=["Unnamed: 0"])
        except:
            pass
        
        #self.describe_all_columns(dataframe)
        self.get_statistics(dataframe)
        self.get_shape(dataframe)


    def describe_all_columns(self, dataframe):
        """prints analysis on the dataframe, giving quick information on the dataframe"""
        
        print(dataframe.describe(percentiles = [.5]))
    
    def get_distinct_categories(self, dataframe):
        """Gets a list of all columns in the current dataframe with dtype of category
        then counts the distinct values in these columns. 
        returns a DataFrame with NaN values where the column dtype is not of category,
        and then the distinct count when the column dtype is"""
        
        distinct_values_count = {}

        for column in dataframe.columns:
            distinct_values_count[column] = dataframe[column].nunique()

        distinct_values_df = pd.DataFrame.from_dict(distinct_values_count, orient="index", columns=["Distinct_Values_Count"])
        distinct_values_df.index.name = "Column_Name"

        return distinct_values_df

    def get_statistics(self, dataframe):
        """Prints a Dataframe from the inputted Dataframe, giving statistical data on the Dataframe such as
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
        print(statistical_df)
    
    def get_mode(self, dataframe):
        """returns the most frequent value for each column in the given dataframe"""
        
        mode_series = dataframe.mode().iloc[0]
        mode_df = pd.DataFrame({"Mode": mode_series})
        return mode_df

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