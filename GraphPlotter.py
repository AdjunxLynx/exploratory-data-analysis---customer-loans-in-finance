import matplotlib.pyplot as plt
import seaborn as sns
from pandasgui import show


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
        print("Setting up plots")
        skewed_dataframe.plot.bar(ax=ax[0], title="Skewness Before")
        unskewed_dataframe.plot.bar(ax=ax[1], title="Skewness After")
        print("Showing plots")
        plt.show()
        plt.close(fig)
        
    def plot_outliers_before_after(self, before, after):
        """creates two barcharts of the columns in the dataframe, before and after they have been cleaned of all outlier values. shows them side by side"""
        
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        before.plot.bar(ax=ax[0], title="Amount of outliers before")
        after.plot.bar(ax=ax[1], title="Amount of outliers after")
        plt.show()
        plt.close(fig)
        
    def visualise_outliers(self, dataframe, outlier_columns, show = True):
                #columns where I deemed the outliers to be irrelevent to analysing and viewing the dataset as a whole
        for column in dataframe.columns:
            if column in outlier_columns:
                if show:
                    plt.figure()  # new figure for each plot
                    sns.boxplot(data=dataframe[column])
                    plt.title(f"Box Plot of {column}")
                    plt.show()
                    plt.close()
            
    def plot_correlation(self, matrix):
        plt.figure(figsize=(12, 8))
        plt.title(f"HeatMap for correlation")
        sns.heatmap(matrix, annot=True, fmt=".2f", cmap='coolwarm', annot_kws={"size": 7})
        plt.show()
        plt.close()
                
    def plot_correlation_before_after(self, before_matrix, after_matrix):
        # Create a figure with 2 subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 8))

        sns.heatmap(before_matrix, ax=ax1, cmap="coolwarm", annot=True)
        ax1.set_title('Correlation heatmap for Before')
        sns.heatmap(after_matrix, ax=ax2, cmap="coolwarm", annot=True)
        ax2.set_title('Correlation heatmap for After')

        plt.show()
        plt.close(fig)