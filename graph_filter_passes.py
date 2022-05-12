import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# graph the number of filters passed per % above/below
filters = pd.read_excel('outputs/howManyFilters.xlsx') 

# first plot
# ax = sns.relplot(data=filters, x="perc", y="passed_filters", size="weight", palette="muted", sizes=(10,100), alpha=0.5)
# plt.title("Percentage of filters passed by the top 1% of runs, per % above/below parameter outputs")
# plt.xlabel("Percentage above/below optimizer parameters")
# plt.ylabel("Percentage of filters passed")
# plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/perc_filters_passed.png')
# plt.show()

# second plot of histograms
d = np.diff(np.unique(filters[['passed_filters']])).min()
left_of_first_bin = np.unique(filters[['passed_filters']]).min() - float(d)/2
right_of_last_bin = np.unique(filters[['passed_filters']]).max() + float(d)/2

fig, ax = plt.subplots()
sns.histplot(
    data=filters, x='passed_filters', hue='perc', multiple='dodge',
    ax=ax, palette="mako", bins=np.arange(left_of_first_bin, right_of_last_bin + d, d)
)
plt.xlabel("Percentage of filters passed")
plt.ylabel("Count")
plt.title("Percentage of filters passed by the top 1% of runs")
plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/perc_filters_passed_histogram.png')

plt.show()