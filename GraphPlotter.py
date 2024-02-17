import matplotlib.pyplot as plt

class Plotter:
    def plot_nulls_before_after(self, before, after):
        """creates two barcharts of the columns in the dataframe, before and after they have been cleaned of all null values. shows them side by side"""
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)
        before.plot.bar(ax=ax[0], title="Null Values Before")
        after.plot.bar(ax=ax[1], title="Null Values After")
        plt.show()   
        
    def plot_skewed_graph(self, skewed_dataframe):
        """creates a barchart to show how skewed a column is"""
        plt.figure(figsize=(10, 6))
        skewed_dataframe.plot(kind='bar')
        plt.title('Skewness of Numeric Columns')
        plt.xlabel('Columns')
        plt.ylabel('Skewness Value')
        plt.axhline(y=0, color='r', linestyle='-')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--')
        plt.tight_layout()
        
        plt.show()