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