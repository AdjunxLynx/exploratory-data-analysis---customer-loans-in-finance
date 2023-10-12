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


    def set_column_to_int(self):
        """sets a list of column names to dtype integer in the dataframe given"""
        set_list = ["id", "member_id", "loan_amount", "funded_amount", "funded_amount_inv","annual_inc", "inq_last_tmths","mths_since_last_record", "open_accounts", "total_accounts", "collections_12_mths_ex_med", "mths_since_last_major_derog"]
        int32_list = []
        for i in range(len(set_list)):
            int32_list.append("int32")
        to_integer_list = dict(zip(set_list, int32_list))
        self.dataframe.astype(to_integer_list)
        show(self.dataframe)

    

if __name__ == "__main__":
    #rdsdbc = RDSDatabaseConnector(load_credentials())
    #save_pd_to_csv(rdsdbc.database_to_pandas_dataframe())
    dt = DataTransform(load_csv_to_pd("loan_payments.csv"))
    dt.set_column_to_int()
    
