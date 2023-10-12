import yaml
import psycopg2
import pandas as pd
from sqlalchemy import create_engine


def load_credentials():
        with open('credentials.yaml', 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials


class RDSDatabaseConnector():
    def __init__(self, credentials):
        url = ("postgresql+psycopg2" + "://" + str(credentials['RDS_USER']) + ":" + str(credentials['RDS_PASSWORD']) + "@" + str(credentials['RDS_HOST']) + "/" + str(credentials['RDS_DATABASE']))
        print(url)
        engine = create_engine(url)


    
rds = RDSDatabaseConnector(load_credentials())