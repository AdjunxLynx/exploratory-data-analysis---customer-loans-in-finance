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
        self.call_all_cleaners(dataframe)

    def call_all_cleaners(self, dataframe):
        """puts all the dataframe cleaning function into one callable function"""
        numeric_list = ["id", "member_id", "loan_amount", "funded_amount", "funded_amount_inv", "term",  "int_rate", "instalment", "employment_length", "annual_inc", "dti", "delinq_2yrs", "inq_last_6mths", "mths_since_last_delinq",  "open_accounts", "total_accounts", "out_prncp", "out_prncp_inv", "total_payment", "total_payment_inv", "total_rec_prncp", "total_rec_int", "total_rec_late_fee", "recoveries", "collection_recovery_fee", "last_payment_amount", "collections_12_mths_ex_med", "mths_since_last_major_derog"]
        date_list = ["issue_date", "earliest_credit_line", "last_payment_date", "next_payment_date", "last_credit_pull_date"]
        
        dataframe = self.set_column_to_custom(dataframe)
        dataframe = self.set_column_to_date(dataframe, date_list)
        dataframe = self.set_numeric(dataframe, numeric_list)
        dataframe = self.set_qualitative(dataframe)
        dataframe = dataframe.rename(columns = {"Unnamed: 0": "Index"})
        dataframe = dataframe.set_index("Index")

        print(dataframe.info())
        show(dataframe)

        return(dataframe)

    def set_numeric(self, dataframe, numeric_list):
        for column in numeric_list:
            dataframe[column] = pd.to_numeric(dataframe[column], errors = "raise")
        return(dataframe)
    
    def set_qualitative(self, dataframe):

            A_to_G = ["A", "B", "C", "D", "E", "F", "G"]

            sub_grade = [] 
            for letter in A_to_G:
                for number in range(1,6):
                    sub_grade.append((letter + str(number)))

            home_ownership_list = ["OWN", "RENT", "MORTGAGE", "OTHER"]
            verification_status = ["Verified", "Source Verified", "Not Verified"]
            payment_plan_list = ["y", "n"]
            application_list = ["INDIVIDUAL"]

            loan_status_list = ["Fully Paid", "In Grace Period", "Charged Off", "Current", "Default", "Late (16-30 days)", "Late (31-120 days)", "Does not meet the credit policy. Status:Fully Paid", "Does not meet the credit policy. Status:Charged Off"]

            purpose_list = ["car", "credit_card", "debt_consolidation", "educational", "home_improvement", "house", "major_purchase", "medical", "moving", "other", "renewable_energy", "small_business", "vacation", "wedding"]

            grade_dtype = pd.CategoricalDtype(categories = A_to_G)
            sub_grade_dtype = pd.CategoricalDtype(categories = sub_grade)
            home_ownership_dtype = pd.CategoricalDtype(categories = home_ownership_list)
            verification_dtype = pd.CategoricalDtype(categories = verification_status)
            loan_status_dtype = pd.CategoricalDtype(categories = loan_status_list)
            payment_plan_dtype = pd.CategoricalDtype(categories = payment_plan_list)
            purpose_dtype = pd.CategoricalDtype(categories = purpose_list)
            application_dtype = pd.CategoricalDtype(categories = application_list)


            dataframe["grade"] = dataframe["grade"].astype(grade_dtype)
            dataframe["sub_grade"] = dataframe["sub_grade"].astype(sub_grade_dtype)
            dataframe["home_ownership"] = dataframe["home_ownership"].astype(home_ownership_dtype)
            dataframe["verification_status"] = dataframe["verification_status"].astype(verification_dtype)
            dataframe["loan_status"] = dataframe["loan_status"].astype(loan_status_dtype)
            dataframe["payment_plan"] = dataframe["payment_plan"].astype(payment_plan_dtype)
            dataframe["purpose"] = dataframe["purpose"].astype(purpose_dtype)
            dataframe["application_type"] = dataframe["application_type"].astype(application_dtype)

            

            return(dataframe)

    def set_column_to_date(self, dataframe, date_list):
        """sets a list of column names to dtype datetime in the dataframe given"""
        
        for column in date_list:
            dataframe[column] = pd.to_datetime(dataframe[column]).dt.date
        return(dataframe)

    def set_column_to_custom(self, dataframe):
        """sets seperate columns to appropriate dtypes and cleans them using the dataframe given"""

        dataframe["term"] = dataframe["term"].str.replace('\D', '', regex = True)
        dataframe["employment_length"] = dataframe["employment_length"].apply(self.clean_employment_length)
        dataframe["employment_length"] = dataframe["employment_length"].str.replace('\D', '', regex = True)
        dataframe["policy_code"] = dataframe["policy_code"].astype(str)
        dataframe["policy_code"] = dataframe["policy_code"].str.replace("1", "Available")
        dataframe["policy_code"] = dataframe["policy_code"].str.replace("0", "Not Available")

        return(dataframe)

    def clean_employment_length(self, length):
        if length == "< 1 year":
            return ("0")
        elif length == "10+ years":
            return ("11")
        else:
            return length


if __name__ == "__main__":
    rdsdbc = RDSDatabaseConnector(load_credentials())
    save_pd_to_csv(rdsdbc.database_to_pandas_dataframe())
    dt = DataTransform(load_csv_to_pd("loan_payments.csv"))
