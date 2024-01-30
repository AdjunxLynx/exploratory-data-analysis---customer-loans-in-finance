from sqlalchemy import create_engine, text
import pandas as pd
import yaml
import sys

class RDSDatabaseConnector():
    def load_credentials():
        """loads credentials from a file called 'credentials.yaml' and returns it as a dictionary"""
        
    
    def __init__(self, credentials_location = "credentials.yaml"):
        try:
            with open(credentials_location, "r") as file:
                credentials = yaml.safe_load(file)
                
            url = ("postgresql+psycopg2://" + str(credentials["RDS_USER"]) + ":" + str(credentials["RDS_PASSWORD"]) + "@" + str(credentials["RDS_HOST"]) + "/" + str(credentials["RDS_DATABASE"]))
            self.engine = create_engine(url)
        
        except:
            raise Exception("Incorrect file location provided for credentials, You can set location in the constructor for the class")


            

    def database_to_pandas_dataframe(self):
        """uses SQLAlchemy engine to connect to online database, download all data in the table and to return as a pandas dataframe"""
        with self.engine.connect() as conn:
            database = conn.execute(text("SELECT * FROM loan_payments"))
            dataframe = pd.DataFrame(data = database)
            return dataframe
        
    def download_df(self, filename = "loan_payments.csv"):
        dataframe = self.database_to_pandas_dataframe()
        dataframe.to_csv(filename)
        return dataframe
        


