class DataFrameTransform:
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