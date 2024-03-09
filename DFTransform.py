import numpy as np
import pandas as pd
from scipy.stats import boxcox, yeojohnson
import json
import os

class DataFrameTransform:
    def count_nulls(self, dataframe):
        """returns the total amount of nulls in a dataframe"""
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
    
    def drop_columns_in_series(self, series, columns):
        for column in columns:
            try:
                series = series.drop(column)
            except:
                print(f"Error Dropping {column}, Moving On")
        return series
    
    def transform_header(self, list1, list2, list3):
        # Zip the two lists together and format each pair as "item1(item2)"
        transformed_header = [f"{item1}({item2}|{item3})" for item1, item2, item3 in zip(list1, list2, list3)]
        return transformed_header
    
    def remove_skewness(self, dataframe, qualitative_list):
        unskewed_dataframe = pd.DataFrame()
        transformation_details = {}
        
        columns = dataframe.select_dtypes(include=['number']).columns
        columns = self.drop_columns_in_series(columns, qualitative_list)

        transformation_list = []
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
                    
            if (dataframe[column] > 0).all():
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
                    
            #print(f"Transformed column '{column}'using transformation method: {transformation_method}")
            
            unskewed_dataframe = pd.concat([unskewed_dataframe, temp], axis = 1)
            lambda_list.append(fitted_lambda)
            transformation_list.append(transformation_method)
            transformation_details[column] = [transformation_method, fitted_lambda]

        print("Done Transformations")
        transformation_method = self.transform_header(columns, transformation_list, lambda_list)
        unskewed_dataframe.columns = columns
        
        with open(os.path.join("script_data", "transformation_details.json"), "w") as json_file:
            json.dump(transformation_details, json_file, indent=4)


        return unskewed_dataframe
    
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
    
    def find_closest_outliers(self, dataframe, outlier_columns):
        outlier_bounds = {}
        
        for column in dataframe.select_dtypes(include=['number']).columns:
            if column in outlier_columns:
                Q1 = dataframe[column].quantile(0.25)
                Q3 = dataframe[column].quantile(0.75)
                IQR = Q3 - Q1
                
                # Define bounds for outliers
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Find outliers
                outliers = dataframe[(dataframe[column] < lower_bound) | (dataframe[column] > upper_bound)][column]
                
                # Find the closest outlier to the max/min within the outlier range if outliers exist
                if not outliers.empty:
                    min_outlier = outliers[outliers > lower_bound].min()  # Closest to lower bound
                    max_outlier = outliers[outliers < upper_bound].max()  # Closest to upper bound
                    outlier_bounds[column] = [min_outlier, max_outlier]
            
        return outlier_bounds


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
        
        # {column_name} : {a,b}  to include a to b and remove everything else

        
        for column, bounds in bounds_dict.items():
            lower_bound, upper_bound = bounds
            # Drop rows where column value is below the lower bound or above the upper bound
            dataframe = dataframe[(dataframe[column] >= lower_bound) & 
                                            (dataframe[column] <= upper_bound)]
        return dataframe