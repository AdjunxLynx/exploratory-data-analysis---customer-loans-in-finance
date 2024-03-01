import numpy as np
import pandas as pd
from scipy.stats import boxcox, yeojohnson

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
        print("Done Transformations")
        columns = self.transform_header(columns, transformation_list, lambda_list)
        unskewed_dataframe.columns = columns
        return unskewed_dataframe
        
                    

                    
                    
            