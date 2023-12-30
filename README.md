# Loan Data Analysis and Visualisation Toolkit

This toolkit provides a comprehensive solution for analysing and visualising loan payment data. It is designed to streamline the process of data cleaning, transformation, and visualisation for loan payment datasets.

## Features

- **Data Loading and Saving**: Easy loading of data from a CSV file and saving processed data back to CSV.
- **Data Transformation**: Robust methods for cleaning and transforming loan payment data for analysis.
- **Null Value Analysis**: Tools for identifying and handling null values in the dataset.
- **Categorical Data Handling**: Specialised methods for managing categorical data types.
- **Data Visualisation**: Integrated plotting tools for visualising data cleaning results.

## Classes and Methods

1. **RDSDatabaseConnector**: Connects to an online database and downloads data as a pandas DataFrame.
2. **DataTransform**: Performs various data transformation tasks like setting data types, cleaning columns, and renaming.
3. **DataFrameInfo**: Provides descriptive statistics and visualisations for the DataFrame.
4. **Plotter**: Visualises the changes in null values before and after data cleaning.
5. **DataFrameTransform**: Contains methods for counting nulls, dropping columns, and imputing missing values.

## Usage

1. **Database Connection and Data Retrieval**: Use `RDSDatabaseConnector` with your database credentials to download data.
2. **Data Cleaning and Transformation**: Apply `DataTransform` and `DataFrameTransform` methods to clean and prepare your data.
3. **Data Analysis**: Use `DataFrameInfo` to get insights into your data.
4. **Visualisation**: Utilise `Plotter` to visualise the impact of your data cleaning process.


## Installation

Ensure you have the required libraries installed. You can install these using pip:

```bash
pip install -r requirements.txt
```

Ensure you have a file called ```credentials.yaml``` with the correct credential details to the online database you wish to connect to.
You will need a few variables, called:

1. ```RDS_HOST``` with the host URL asigned.
2. ```RDS_PASSWORD``` with the login user password asigned.
3. ```RDS_USER``` with the login username.
4. ```RDS_DATABASE``` with the desired database you wish to connect to.
5. ```RDS_PORT``` with the correct port number to use to connect to.

## Example

```python
# Connect to the database and load data
rdsdbc = RDSDatabaseConnector(load_credentials())
dataframe = rdsdbc.database_to_pandas_dataframe()

# Perform data transformations
dtransformer = DataTransform()
dataframe = dtransformer.call_all_cleaners(dataframe)

# Analyse and visualise data
dfinfo = DataFrameInfo()
dfinfo.call_all_information(dataframe)

# Plot null values before and after cleaning
dftransformer = DataFrameTransform()
plotter = Plotter()
nulls_before = dftransformer.count_nulls(dataframe)
dataframe = dftransformer.drop_columns(dataframe)
dataframe = dftransformer.impute_columns(dataframe)
nulls_after = dftransformer.count_nulls(dataframe)
plotter.plot_nulls_before_after(nulls_before, nulls_after)
```
