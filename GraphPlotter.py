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
        skewed_dataframe.plot.bar(ax=ax[0], title="Skewed Values Before")
        unskewed_dataframe.plot.bar(ax=ax[1], title="Unskewed Values After")
        print("Showing plots")
        plt.show()
        plt.close(fig)
        
    def plot_outliers_before_after(self, before, after):
        """creates two barcharts of the columns in the dataframe, before and after they have been cleaned of all outlier values. shows them side by side"""
        
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        before.plot.bar(ax=ax[0], title="Outlier Values Before")
        after.plot.bar(ax=ax[1], title="Outlier Values After")
        plt.show()
        plt.close(fig)
        
    def visualise_outliers(self, dataframe):
        for column in dataframe.columns:
            plt.figure()  # This ensures a new figure for each plot
            sns.boxplot(data=dataframe[column])
            plt.title(f"Box Plot of {column}")
            plt.show()
        