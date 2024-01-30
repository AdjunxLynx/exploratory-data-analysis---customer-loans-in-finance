import pandas as pd

class DataTransform():
    def __init__(self):
        pass

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

        #print(dataframe.info())

        return(dataframe)

    def set_numeric(self, dataframe, numeric_list):
        """turns all columns listed in numeric_list in the dataframe given to a numeric dtype"""
        for column in numeric_list:
            
            dataframe[column] = pd.to_numeric(dataframe[column], errors = "coerce", downcast = "integer")
            dataframe[column] = dataframe[column].round()
            dataframe[column] = dataframe[column].apply(lambda x: round(x) if not pd.isnull(x) else x).astype("Int64")

        return(dataframe)
    
    def set_qualitative(self, dataframe):
            """creates new catagorical dtypes of each qualitative column, and sets that column as the new dtype to save space.
            some dtypes are also ordered"""

            A_to_G = ["A", "B", "C", "D", "E", "F", "G"]

            sub_grade = [] 
            for letter in A_to_G:
                for number in range(1,6):
                    sub_grade.append((letter + str(number)))

            home_ownership_list = ["OWN", "RENT", "MORTGAGE", "OTHER", "NOT GIVEN"]
            verification_status = ["Verified", "Source Verified", "Not Verified"]
            payment_plan_list = ["y", "n"]
            application_list = ["INDIVIDUAL"]
            employment_length_list = ["<1", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", ">10"]
            loan_status_list = ["Fully Paid", "In Grace Period", "Charged Off", "Current", "Default", "Late (16-30 days)", "Late (31-120 days)", "Does not meet the credit policy. Status:Fully Paid", "Does not meet the credit policy. Status:Charged Off"]
            purpose_list = ["car", "credit_card", "debt_consolidation", "educational", "home_improvement", "house", "major_purchase", "medical", "moving", "other", "renewable_energy", "small_business", "vacation", "wedding"]

            grade_dtype = pd.CategoricalDtype(categories = A_to_G, ordered = True)
            sub_grade_dtype = pd.CategoricalDtype(categories = sub_grade, ordered = True)
            home_ownership_dtype = pd.CategoricalDtype(categories = home_ownership_list)
            verification_dtype = pd.CategoricalDtype(categories = verification_status)
            loan_status_dtype = pd.CategoricalDtype(categories = loan_status_list)
            payment_plan_dtype = pd.CategoricalDtype(categories = payment_plan_list)
            purpose_dtype = pd.CategoricalDtype(categories = purpose_list)
            application_dtype = pd.CategoricalDtype(categories = application_list)
            employ_length_dtype = pd.CategoricalDtype(categories = employment_length_list, ordered = True)


            dataframe["grade"] = dataframe["grade"].astype(grade_dtype)
            dataframe["sub_grade"] = dataframe["sub_grade"].astype(sub_grade_dtype)
            dataframe["home_ownership"] = dataframe["home_ownership"].astype(home_ownership_dtype)
            dataframe["verification_status"] = dataframe["verification_status"].astype(verification_dtype)
            dataframe["loan_status"] = dataframe["loan_status"].astype(loan_status_dtype)
            dataframe["payment_plan"] = dataframe["payment_plan"].astype(payment_plan_dtype)
            dataframe["purpose"] = dataframe["purpose"].astype(purpose_dtype)
            dataframe["application_type"] = dataframe["application_type"].astype(application_dtype)
            dataframe["employment_length"] = dataframe["employment_length"].astype(employ_length_dtype)

            

            return(dataframe)

    def set_column_to_date(self, dataframe, date_list):
        """sets a list of column names to dtype datetime in the dataframe given"""
        for column in date_list:
            dataframe[column] = pd.to_datetime(dataframe[column], errors = "coerce", format="%Y-%m-%d").dt.date
        return(dataframe)

    def set_column_to_custom(self, dataframe):
        """sets seperate columns to appropriate dtypes and cleans them using the dataframe given"""

        dataframe["term"] = dataframe["term"].str.replace("\D", "", regex = True)
        dataframe["employment_length"] = dataframe["employment_length"].apply(self.clean_employment_length)
        dataframe["employment_length"] = dataframe["employment_length"].str.replace("[^0-9<>]", "", regex = True)
        dataframe["policy_code"] = dataframe["policy_code"].astype(str)
        dataframe["policy_code"] = dataframe["policy_code"].str.replace("1", "Available")
        dataframe["policy_code"] = dataframe["policy_code"].str.replace("0", "Not Available")

        return(dataframe)

    def clean_employment_length(self, length):
        """this function is a quick filter to replace the value in employment_length to the correct value, shortening the value and making it ready for categorising"""
        if length == "< 1 year":
            return ("<1")
        elif length == "10+ years":
            return (">10")
        else:
            return length