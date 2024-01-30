from sqlalchemy import create_engine, text
import pandas as pd

class RDSDatabaseConnector():
    def __init__(self, credentials):
        url = ("postgresql+psycopg2://" + str(credentials["RDS_USER"]) + ":" + str(credentials["RDS_PASSWORD"]) + "@" + str(credentials["RDS_HOST"]) + "/" + str(credentials["RDS_DATABASE"]))
        self.engine = create_engine(url)

    def database_to_pandas_dataframe(self):
        """uses SQLAlchemy engine to connect to online database, download all data in the table and to return as a pandas dataframe"""
        with self.engine.connect() as conn:
            database = conn.execute(text("SELECT * FROM loan_payments"))
            dataframe = pd.DataFrame(data = database)
            return dataframe


