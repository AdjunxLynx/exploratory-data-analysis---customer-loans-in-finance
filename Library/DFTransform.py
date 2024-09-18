from scipy.stats import boxcox, yeojohnson

import numpy as np
import pandas as pd
import json
import os

#impute values if null values are less than a certain %. dont wanna skew dataset to avg or mode.

class DataFrameTransform:
    def count_nulls(self, dataframe):
        """returns the total amount of nulls in a dataframe"""
        
        return dataframe.isnull().sum()

    def drop_columns(self, dataframe, threshold=0.5):
        """this function drops all columns where the null value percentage is above a given %, default being 50%"""
        
        columns_to_drop = [column for column in dataframe.columns if dataframe[column].isnull().mean() > threshold]
        print(f"Dropping columns as the amount of nulls in the column is above {threshold*100}%: \n {columns_to_drop}")
        return dataframe.drop(columns=columns_to_drop, axis=1)

    def impute_columns(self, dataframe):
        """For quantative data, imputes data into columns by the column mean, for qualitative, imputes by the most frequent"""
        
        for column in dataframe.columns:
            if dataframe[column].dtype == 'float64' or dataframe[column].dtype == 'int64':

                dataframe.fillna({column: dataframe[column].mean()}, inplace = True)
            else:

                dataframe.fillna({column: dataframe[column].mode()[0]}, inplace = True)
        return dataframe
    
    def drop_columns_in_series(self, series, columns):
        """Drops all indexs where the index name is in columns list to drop"""
        
        for column in columns:
            try:
                series = series.drop(column)
            except:
                pass
        return series
    
    def transform_header(self, list1, list2, list3):
        """creates a new header in the format of 'item1(item2|item3)', where item1 should be column name, item2 should be transformation type used to reduce skewness
        and item3 should be lambda used to transform and unskew data (where applicable)"""
        
        transformed_header = [f"{item1}({item2}|{item3})" for item1, item2, item3 in zip(list1, list2, list3)]
        return transformed_header
    
    def remove_skewness(self, dataframe, qualitative_list):
        """Transforms each column to reduce skewness. chooses best method to reduce skewness by applying all of them (logarithmic, square root, cube root, boxcox and yeo)
        ,then finding out which one has the largest affect. Writes to a file on the transformation method used for each column, incase of future use."""
        
        unskewed_dataframe = pd.DataFrame()
        transformation_details = {}
        
        columns = dataframe.select_dtypes(include=['number']).columns
        columns = self.drop_columns_in_series(columns, qualitative_list)

        transformation_list = []
        transformed_methods = []
        lambda_list = []
        
        for column in columns:
            compare_value = dataframe[column].skew() #original skewed value to compare against

            if (dataframe[column] > 0).all():
                temp = np.log(dataframe[column])
                fitted_lambda = ""
                new_skewness = float(temp.skew())
                if abs(new_skewness) < abs(compare_value):
                    transformation_method = "log"
                    compare_value = temp.skew()
                    
            if (dataframe[column] >= 0).all():
                temp = np.sqrt(dataframe[column])
                fitted_lambda = ""
                new_skewness = float(temp.skew())
                if abs(new_skewness) < abs(compare_value):
                    transformation_method = "sqrt"
                    compare_value = temp.skew()
            
            if True: #both positive and negative skewness allowed
                temp = np.cbrt(dataframe[column])
                fitted_lambda = ""
                new_skewness = float(temp.skew())
                if abs(new_skewness) < abs(compare_value):
                    transformation_method = "cbrt"
                    compare_value = temp.skew()
                    
            
               
            transformed_methods.append(f"Transformed column '{column}'using transformation method: {transformation_method}, {lambda_list} \n")
            
            unskewed_dataframe = pd.concat([unskewed_dataframe, temp], axis = 1)
            lambda_list.append(fitted_lambda)
            transformation_list.append(transformation_method)
            transformation_details[column] = [transformation_method, fitted_lambda]
            
        transformation_method = self.transform_header(columns, transformation_list, lambda_list)
        unskewed_dataframe.columns = columns

        return unskewed_dataframe, transformed_methods
    
        if (dataframe[column] > 0).all():
                print(dataframe[column].min())
                temp, fitted_lambda = boxcox(dataframe[column])
                temp = pd.Series(temp)
                new_skewness = float(temp.skew())
                if abs(new_skewness) < abs(compare_value):
                    transformation_method = "boxcox"
                    compare_value = temp.skew()
            
        if True: #both positive and negative skewness allowed
            temp, fitted_lambda = yeojohnson(dataframe[column])
            temp = pd.Series(temp)
            new_skewness = float(temp.skew())
            if abs(new_skewness) < abs(compare_value):
                transformation_method = "yeo"
                compare_value = temp.skew()
    
    def merge_dataframes(self, full_df, transformed_df):
        """Merges two DataFrames, prioritizing data from transformed_df for overlapping columns.
        The resulting DataFrame retains the column order from full_df"""
        
        # Ensure the index aligns for proper updating
        full_df = full_df.copy()
        transformed_df = transformed_df.set_index(full_df.index)

        # Update the full DataFrame with the transformed data
        for column in transformed_df.columns:
            if column in full_df.columns:
                full_df[column] = transformed_df[column]
        
        # Return the full DataFrame with updated data
        return full_df
    
    def find_closest_outliers(self,dataframe, outlier_columns):
        """creates a dictionary of each column chosen to remove outliers, with a list of 2 variables to determine how to remove outlier values."""
        
        bounds = {}
        # Select only numerical columns for outlier bounds calculation
        numeric_cols = dataframe.select_dtypes(include=['number']).columns

        for column in numeric_cols:
            if column in outlier_columns:
                Q1 = dataframe[column].quantile(0.25)
                Q3 = dataframe[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                bounds[column] = [lower_bound, upper_bound]
        print(bounds)
        return bounds




    def calculate_outlier_counts(self, dataframe, outlier_columns):
        """Calculates the count of outliers in each column of the dataframe."""
        
        outlier_counts = {}
        for column in dataframe.select_dtypes(include=['number']).columns:
            if column in outlier_columns:
                Q1 = dataframe[column].quantile(0.25)
                Q3 = dataframe[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Count outliers
                outlier_counts[column] = ((dataframe[column] < lower_bound) | (dataframe[column] > upper_bound)).sum()
        return outlier_counts
    
    
    def drop_outside_bounds(self, dataframe, bounds_dict):
        """Drops rows where column values are outside the specified bounds"""
        
        for column, bounds in bounds_dict.items():
            lower_bound, upper_bound = bounds
            # Drop rows where column value is below the lower bound or above the upper bound
            dataframe = dataframe[(dataframe[column] >= lower_bound) & 
                                            (dataframe[column] <= upper_bound)]
        return dataframe
    
    def get_correlation_matrix(self, dataframe):
        numeric_df = dataframe.select_dtypes(include=['number'])
        matrix = numeric_df.corr().abs()
        return matrix
    
    def drop_overcorrelated(self, dataframe, matrix, ignore_list = [], threshold=0.7):
        """drops all columns where there is a correlation value above a certain threshold(default is 0.7). Will only drop one of the columns that are overly correlated"""
        
        # Compute the absolute correlation matrix from the dataframe directly
        
        abs_matrix = matrix.abs()
        # columns to drop
        drop_list = []
        # if columns has already been considered for dropping
        considered = set(ignore_list)

        # Iterate over the columns of the correlation matrix
        for i, column in enumerate(abs_matrix.columns):
            if column not in considered:
                for j, other_column in enumerate(abs_matrix.columns[i + 1:], i + 1):
                    
                    if abs_matrix.iloc[i, j] > threshold and other_column not in considered:
                        drop_list.append(other_column)
                        considered.add(other_column)
                        
                        

        # Drop the identified columns from the original DataFrame, and any null columns
        dataframe = dataframe.drop(columns=drop_list)
        print(f"Columns dropped:{drop_list}")
        return dataframe
