import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.ticker import ScalarFormatter, FuncFormatter



class Plotter:
    def plot_nulls_before_after(self, before, after):
        """creates two barcharts of the columns in the dataframe, before and after they have been cleaned of all null values. shows them side by side"""
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        before.plot.bar(ax=ax[0], title="Null Values Before")
        after.plot.bar(ax=ax[1], title="Null Values After")
        plt.show()
        plt.close(fig)
        
    def plot_skewed_vs_unskewed_graph(self, skewed_dataframe, unskewed_dataframe):
        """creates two barcharts of the skewness of columns in the dataframe, before and after they have been transformed. shows them side by side"""

        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        skewed_dataframe.plot.bar(ax=ax[0], title="Skewness Before")
        unskewed_dataframe.plot.bar(ax=ax[1], title="Skewness After")
        plt.show()
        plt.close(fig)
        
    def plot_outliers_before_after(self, before, after):
        """creates two barcharts of the columns in the dataframe, before and after they have been cleaned of all outlier values. shows them side by side"""
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        before.plot.bar(ax=ax[0], title="Amount of outliers before")
        after.plot.bar(ax=ax[1], title="Amount of outliers after")
        
        ax[0].tick_params(axis='x', rotation=45)
        ax[1].tick_params(axis='x', rotation=45) 
        plt.setp(ax[0].get_xticklabels(), ha="right")
        plt.setp(ax[1].get_xticklabels(), ha="right")
        
        plt.show()
        plt.close(fig)
        
    def visualise_outliers(self, dataframe, outlier_columns, show = True):
        """creates a boxplot of each column in input to visualise outliers in the dataset"""
        
        for column in dataframe.columns:
            if column in outlier_columns:
                if show:
                    plt.figure()  # new figure for each plot
                    sns.boxplot(data=dataframe[column])
                    plt.title(f"Box Plot of {column}")
                    plt.show()
                    plt.close()
            
    def plot_correlation(self, matrix):
        """creates a heatmap given a correlation matrix to help visualise correlations between columns"""
        
        plt.figure(figsize=(12, 8))
        plt.title(f"HeatMap for correlation")
        sns.heatmap(matrix, annot=True, fmt=".2f", cmap='coolwarm', annot_kws={"size": 7})
        plt.show()
        plt.close()
                
    def plot_correlation_before_after(self, before_matrix, after_matrix):
        """creates two heatmaps, one visualising the dataframe before, and after removing columns"""
        
        # Create a figure with 2 subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 8))

        sns.heatmap(before_matrix, ax=ax1, cmap="coolwarm", annot=True)
        ax1.set_title('Correlation heatmap for Before')
        sns.heatmap(after_matrix, ax=ax2, cmap="coolwarm", annot=True)
        ax2.set_title('Correlation heatmap for After')

        plt.show()
        plt.close(fig)
        
    def plot_recovery_rate(self, recovery_percentage):
        plt.figure(figsize=(10, 6))
        plt.hist(recovery_percentage, bins=10, color='blue', edgecolor='black')
        plt.xlabel('Recovery Percentage (%)')
        plt.ylabel('Number of Loans')
        plt.title('Distribution of Loan Recovery Percentages')
        plt.show()
        
    def plot_loan_to_pay(self, loans_percentage_to_pay):
        plt.figure(figsize=(10, 6))
        plt.hist(loans_percentage_to_pay, bins=10, color='blue', edgecolor='black')
        plt.xlabel('Percentage left to pay (%)')
        plt.ylabel('Number of Loans')
        plt.title('Distribution of Loan left to pay Percentages')
        plt.show()
        
    def plot_amount_payed_6mths(self, amount_payed_6mths):
        plt.figure(figsize=(10, 6))
        plt.hist(amount_payed_6mths, bins=10, color='blue', edgecolor='black')
        plt.xlabel('Projected total payment for 6 months (£)')
        plt.ylabel('Number of Loans')
        plt.title('Distribution of projected total payments for 6 months')
        plt.show()
        
    
        
    def plot_loss_from_charged_off(self, loss_by_bucket):
        def format_y_axis(value, tick_number):
            return f"{int(value):,}"
    
        plt.figure(figsize = (10,6))
        loss_by_bucket.plot(kind = "bar", color = "red")
        

        plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_y_axis))
        
        
        plt.xlabel("Remaining Term (Months)")
        plt.ylabel("Total expected loss (£)")
        plt.title("Expected loss aggregated by remaining term")
        plt.show()
        
    def visualise_loan_grade(self, dataframe):
        plt.figure(figsize=(10, 6))
        sns.countplot(data=dataframe, x="grade", hue="loan_status")
        plt.title("Distribution of Loan Sub Grades by Loan Status")
        plt.xlabel("Loan Grade")
        plt.ylabel("Number of Loans")
        plt.show()
        
    def visualise_loan_subgrade(self, dataframe):
        plt.figure(figsize=(10, 6))
        dataframe = dataframe.sort_values(by="sub_grade")
        sns.countplot(data=dataframe, x="sub_grade", hue="loan_status")
        plt.title("Distribution of Loan Grades by Loan Status")
        plt.xlabel("Loan Grade")
        plt.ylabel("Number of Loans")
        plt.show()
        
    def visualise_loan_purpose(self, dataframe):
        plt.figure(figsize=(12, 8))
        sns.countplot(data=dataframe, y="purpose", hue="loan_status", order=dataframe["purpose"].value_counts().index)
        plt.title("Distribution of Loan Purposes by Loan Status")
        plt.xlabel("Number of Loans")
        plt.ylabel("Loan Purpose")
        plt.show()
        
    def visualise_loan_home(self, dataframe):
        plt.figure(figsize=(10, 6))
        sns.countplot(data=dataframe, x="home_ownership", hue="loan_status")
        plt.title("Distribution of Home Ownership by Loan Status")
        plt.xlabel("Home Ownership Status")
        plt.ylabel("Number of Loans")
        plt.show()
        
    def visualise_loan_term(self, dataframe):
        plt.figure(figsize=(10, 6))
        sns.countplot(data=dataframe, x="term", hue="loan_status")
        plt.title("Distribution of Loan Terms by Loan Status")
        plt.xlabel("Term Length")
        plt.ylabel("Number of Loans")
        plt.show()
