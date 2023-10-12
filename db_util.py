import yaml
import pandas as pd
from sqlalchemy import create_engine, text
from pandasgui import show


def load_credentials():
        with open('credentials.yaml', 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials

def save_pd_to_csv(df):
     df.to_csv('loan_payments.csv')

class RDSDatabaseConnector():
    def __init__(self, credentials):
        url = ("postgresql+psycopg2://" + str(credentials['RDS_USER']) + ":" + str(credentials['RDS_PASSWORD']) + "@" + str(credentials['RDS_HOST']) + "/" + str(credentials['RDS_DATABASE']))
        self.engine = create_engine(url)

    def to_pandas_df(self):
         with self.engine.connect() as conn:
            db = conn.execute(text("SELECT * FROM loan_payments"))
            df = pd.DataFrame(data = db)
            return df

    
rds = RDSDatabaseConnector(load_credentials())
save_pd_to_csv(rds.to_pandas_df())
