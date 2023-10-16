from sqlalchemy import create_engine, text
from pandasgui import show
import yaml
import pandas as pd



def load_credentials():
    """loads credentials from a file called 'credentials.yaml' and returns it as a dictionary"""
    with open('credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

def save_pd_to_csv(dataframe):
    """takes input parameter and dumps into a file in directory called 'loan_payments.csv'"""
    dataframe.to_csv('loan_payments.csv')

def load_csv_to_pd(filename):
    """takes input filename as parameter and displays file as a large table"""
    dataframe = pd.read_csv(filename)
    return dataframe


class RDSDatabaseConnector():
    def __init__(self, credentials):
        url = ("postgresql+psycopg2://" + str(credentials['RDS_USER']) + ":" + str(credentials['RDS_PASSWORD']) + "@" + str(credentials['RDS_HOST']) + "/" + str(credentials['RDS_DATABASE']))
        self.engine = create_engine(url)

    def database_to_pandas_dataframe(self):
        """uses SQLAlchemy engine to connect to online database, download all data in the table and to return as a pandas dataframe"""
        with self.engine.connect() as conn:
            database = conn.execute(text("SELECT * FROM loan_payments"))
            dataframe = pd.DataFrame(data = database)
            return dataframe

    
class DataTransform():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def call_all_cleaners(self):
        """puts all the dataframe cleaning function into one callable function"""

        self.set_column_to_custom()
        self.set_column_to_date()
        #self.set_column_to_float()
        #self.set_column_to_int()
        self.set_numeric()
        show(self.dataframe)


    def set_column_to_int(self):
        """sets a list of column names to dtype integer in the dataframe given"""

        #creates list of all column names to set to dtype int

        
        #creates a list containing "int32" with len = to set_list
        int32_list = []
        for i in range(len(set_list)):
            int32_list.append("int32")
        to_integer_list = dict(zip(set_list, int32_list))

        self.dataframe.astype(to_integer_list)
        


    def set_numeric(self):
        numeric_list = ["id", "member_id", "loan_amount", "funded_amount", "funded_amount_inv", "term",  "int_rate", "employment_length", "annual_inc", "dti", "delinq_2yrs", "inq_last_6mths", "mths_since_last_delinq", "mths_since_last_delinq",  "open_accounts", "total_accounts", "out_prncp", "out_prncp_inv", "total_payment", "total_payment_inv", "total_rec_prncp", "total_rec_int", "total_rec_late_fee", "recoveries", "collection_recovery_fee", "last_payment_amount", "collections_12_mths_ex_med", "mths_since_last_major_derog"]
        numeric_dataframe = self.dataframe[numeric_list]
        qualitive_dataframe = self.dataframe.drop(columns = numeric_list)
        for column in numeric_list:
            self.dataframe[column] = pd.to_numeric(self.dataframe[column], errors = 'raise')
        



    def set_column_to_date(self):
        """sets a list of column names to dtype datetime in the dataframe given"""

        column_list = ["issue_date", "earliest_credit_line", "last_payment_date", "next_payment_date", "last_credit_pull_date"]

        for column in column_list:
            self.dataframe[column] = pd.to_datetime(self.dataframe[column]).dt.date

    def set_column_to_custom(self):
        """sets seperate columns to appropriate dtypes and cleans them using the dataframe given"""

        self.dataframe["term"] = self.dataframe["term"].str.replace('\D', '', regex = True)

        self.dataframe["employment_length"] = self.dataframe["employment_length"].apply(self.clean_employment_length)
        self.dataframe["employment_length"] = self.dataframe["employment_length"].str.replace('\D', '', regex = True)
        


    def clean_employment_length(self, length):
        if length == "< 1 year":
            return ("0")
        elif length == "10+ years":
            return ("11")
        else:
            return length


if __name__ == "__main__":
    #rdsdbc = RDSDatabaseConnector(load_credentials())
    #save_pd_to_csv(rdsdbc.database_to_pandas_dataframe())
    dt = DataTransform(load_csv_to_pd("loan_payments.csv"))
    dt.call_all_cleaners()