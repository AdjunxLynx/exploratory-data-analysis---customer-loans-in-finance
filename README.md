# Loan Data Analysis and Visualisation Toolkit

This project comprises a suite of Python scripts and a Jupyter Notebook designed to streamline data analysis and visualization processes. The collection includes tools for data connection, transformation, in-depth analysis, and sophisticated graph plotting.

## Features

- **Data Loading and Saving**: Easy loading of data from a CSV file and saving processed data back to CSV.
- **Data Transformation**: Robust methods for cleaning and transforming loan payment data for analysis.
- **Null Value Analysis**: Tools for identifying and handling null values in the dataset.
- **Categorical Data Handling**: Specialised methods for managing categorical data types.
- **Data Visualisation**: Integrated plotting tools for visualising data cleaning results.
- **Outlier Removal**: Methods for removing any outliers that may make analysis harder to visualise

## Classes and Methods

1. **RDSDatabaseConnector**: Connects to an online database and downloads data as a pandas DataFrame.
2. **DataTransform**: Performs various data transformation tasks like setting data types, cleaning columns, and renaming.
3. **DataFrameInfo**: Provides descriptive statistics and information for the DataFrame.
4. **Plotter**: Visualises the changes that occur for each transformation method.
5. **DataFrameTransform**: Contains methods for counting nulls, dropping columns, remove skewness, find outliers and imputing missing values.

## Usage

1. **Database Connection and Data Retrieval**: Use `RDSDatabaseConnector` with the database credentials to download data.
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



## Components Overview

### `Connector.py`
A foundational script responsible for establishing connections, facilitating seamless data retrieval and database interactions.

### `db_util.ipynb`
An interactive Jupyter Notebook that documents the workflow of connecting to an online server, downloading a database, and saving it as `loan_payments.csv`. It demonstrates data manipulation techniques and visualization functions, providing a comprehensive guide for similar data analysis tasks.

### `DFInfo.py`
Implements functions to calculate and filter missing values in dataframes, offering a detailed overview of data quality by evaluating missing values' percentage across different columns.

### `DFTransform.py`
Provides robust functionalities for transforming dataframe columns based on specified criteria. This includes zipping lists, formatting, and updating dataframes with transformed data, ensuring data integrity and alignment for analysis.

### `DTransform.py`
Closely associated with `DFTransform.py`, this script specializes in specific data transformation processes, complementing the broader functionalities of its counterpart.

### `GraphPlotter.py`
Facilitates advanced graph plotting, particularly focusing on visualizing the effect of DFTransform and DTransform methods on a given dataframe. It supports creating intricate figures with subplots, enhancing the data analysis visual outcomes.

## Usage Guide

Execute the scripts based on your data analysis requirements. For the Jupyter Notebook, it can be opened and run using Jupyter Lab or Notebook interface by executing the following.

```bash
jupyter notebook db_util.ipynb
```

Or execute the following to run each script automatically.

```bash
python3 db_util.py
```

This project is structured to provide a comprehensive toolkit for data analysis and visualization tasks, embodying best practices in code organization and documentation.

## License

This github repo is licensed under MIT.