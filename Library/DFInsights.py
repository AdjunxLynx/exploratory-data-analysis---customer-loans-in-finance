from Library.GraphPlotter import Plotter 


class Insights:
    def __init__(self):
        self.plotter = Plotter
    
    def visualise_loss(self, dataframe):
        
        charged_off_loans = dataframe[dataframe["loan_status"] == "Charged Off"]
        charged_off_percentage = round((len(charged_off_loans) / len(dataframe) * 100), 3)
        total_payment_to_charged_off = round(charged_off_loans["total_payment"].sum(), 3)
        
        print("Percentage of Charged Off Loans: " + str(charged_off_percentage) + "%")
        print("Total amount paid towards charged off loans: £" + str(total_payment_to_charged_off))
        

        charged_off_loans["total_expected_payment"] = charged_off_loans["term"] * charged_off_loans["instalment"]
        charged_off_loans["expected_loss"] = charged_off_loans["total_expected_payment"] - charged_off_loans["total_payment"]
        charged_off_loans["remaining_term"] = charged_off_loans["term"] - (charged_off_loans["total_payment"] / charged_off_loans["instalment"])
        
        charged_off_loans["term_bucket"] = (charged_off_loans["remaining_term"] // 6) * 6
        loss_by_bucket = charged_off_loans.groupby("term_bucket")["expected_loss"].sum()
        self.plotter.plot_loss_from_charged_off(loss_by_bucket)
        
        
    def visualise_loss(self, dataframe):
        
        charged_off_loans = dataframe[dataframe["loan_status"] == "Charged Off"]
        charged_off_percentage = round((len(charged_off_loans) / len(dataframe) * 100), 3)
        total_payment_to_charged_off = round(charged_off_loans["total_payment"].sum(), 3)
        
        print("Percentage of Charged Off Loans: " + str(charged_off_percentage) + "%")
        print("Total amount paid towards charged off loans: £" + str(total_payment_to_charged_off))
        

        charged_off_loans["total_expected_payment"] = charged_off_loans["term"] * charged_off_loans["instalment"]
        charged_off_loans["expected_loss"] = charged_off_loans["total_expected_payment"] - charged_off_loans["total_payment"]
        charged_off_loans["remaining_term"] = charged_off_loans["term"] - (charged_off_loans["total_payment"] / charged_off_loans["instalment"])
        
        charged_off_loans["term_bucket"] = (charged_off_loans["remaining_term"] // 6) * 6
        loss_by_bucket = charged_off_loans.groupby("term_bucket")["expected_loss"].sum()
        self.plotter.plot_loss_from_charged_off(loss_by_bucket)
        


    def visualise_potential_loss(self, dataframe):

        #expected loss if all late customers were set to Charged Off
        dataframe["expected_payment_left"] = dataframe["loan_amount"] - dataframe["total_payment"]
        expected_loss = dataframe["expected_payment_left"].sum()
        
        
        dataframe["total_expected_payment"] = dataframe["term"] * dataframe["instalment"]
        dataframe["projected_loss"] = dataframe["total_expected_payment"] - dataframe["total_payment"]
        loss_if_term_finished = dataframe["projected_loss"].sum()
        
        
        #creates a df of only the late paying customers
        exclude_status = ["Fully Paid", "Current", "Charged Off", "In Grace Period", "Does not meet the credit policy. Status:Charged Off", "Does not meet the credit policy. Status:Fully Paid"]
        late_dataframe = dataframe[~dataframe["loan_status"].isin(exclude_status)]
        
        #calculates % of late payments
        amount_of_late_payments = len(late_dataframe)
        total_payments = len(dataframe)
        percentage_of_late_payments = (amount_of_late_payments/total_payments * 100)
        avg_expected_loss = expected_loss / amount_of_late_payments
            
        #finds % of late and defaulted revenue compared to total revenue
        total_expected_revenue = dataframe["total_expected_payment"].sum()
        total_expected_payment_for_late_people = late_dataframe["total_expected_payment"].sum()
        percentage_of_late_and_defaulted = total_expected_payment_for_late_people / total_expected_revenue
        
        
        print(f"{percentage_of_late_payments}% of all customers are late on their payments.")
        print(f"There are {amount_of_late_payments} people late on their payments. A total of £{expected_loss} would be lost if they were set to Charged Off")
        print(f"The average expected loss per person is £{avg_expected_loss}")
        print(f"If customers were to finish their term, the projected loss would be £{loss_if_term_finished}")
        print(f"Late and Defaulted payments represent {percentage_of_late_and_defaulted}% of all revenue")\
            
            
            
            
    def indicators_of_loss(self, dataframe):
        
        statuses = ["Charged Off", "Late (31-120 days)","Late (16-30 days)", "Default"]
        
        sub_dataframe = dataframe[dataframe["loan_status"].isin(statuses)]
        self.plotter.visualise_loan_grade(sub_dataframe)
        self.plotter.visualise_loan_subgrade(sub_dataframe)
        self.plotter.visualise_loan_home(sub_dataframe)
        self.plotter.visualise_loan_purpose(sub_dataframe)
        self.plotter.visualise_loan_term(sub_dataframe)
        
        print("Sub grades have a direct correlation with loans being Charged off, and this extends to all late payments, as the grades with high charged off rates, also have high late payment rates")
        print("The same goes with the home ownership status. If you rent or pay mortgage on your home, the loan is likely to end up Charged Off. ")
        print("The loan purpose also has a correlation, albeit less impactful. Home improvements, debt consolidation, credit cards or others seem to be a high risk loan, as these are likely to be charged off. Being late on the loans will likely end up being CHarged off too")
        print("Having a shorter term length will result in being more likely to be charged off, however the term length doesnt seem to be affected by wether you are late on the loan")