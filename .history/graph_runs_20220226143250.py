# graph the runs
from run_experiments import run_counterfactual
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def graph_runs():

    number_simulations, final_results, counterfactual, accepted_parameters = run_counterfactual()

    final_results = final_results[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "accepted?", "run_number"]]
    counterfactual = counterfactual[["Time", "Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground", "accepted?", "run_number"]]

    # reshape final dataframe: accepted shape
    accepted_shape_finaldf = np.repeat(final_results['accepted?'], 10)
    accepted_shape_counterfactual = np.repeat(counterfactual['accepted?'], 10)
    accepted_shape = pd.concat([accepted_shape_finaldf, accepted_shape_counterfactual], axis=0)
    # grouping variable
    grouping_variable_finaldf = np.repeat(final_results['run_number'], 10)
    grouping_variable_counterfactual = np.repeat(counterfactual['run_number'], 10)
    grouping_variable = pd.concat([grouping_variable_finaldf, grouping_variable_counterfactual], axis=0)
    # y values
    y_values_finaldf = final_results.drop(['run_number', 'accepted?', 'Time'], axis=1).values.flatten()
    y_values_counterfactual = counterfactual.drop(['run_number', 'accepted?', 'Time'], axis=1).values.flatten()
    y_values = np.concatenate((y_values_finaldf, y_values_counterfactual), axis=0)
    # species list. this should be +1 the number of simulations
    species_list_finaldf = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185*number_simulations) 
    species_list_counterfactual = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 185*len(accepted_parameters))
    species_list = np.concatenate((species_list_finaldf, species_list_counterfactual), axis=0)
    # indices
    indices_finaldf = np.repeat(final_results['Time'], 10)
    indices_counterfactual = np.repeat(counterfactual['Time'], 10)
    indices = pd.concat([indices_finaldf, indices_counterfactual], axis=0)

    final_df = pd.DataFrame(
    {'Abundance %': y_values, 'runNumber': grouping_variable, 'Ecosystem Element': species_list, 'Time': indices, 'runType': accepted_shape})
    
    # calculate median 
    m = final_df.groupby(['Time', 'runType', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df = final_df.join(m, on=['Time', 'runType', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df.groupby(['Time', 'runType', 'Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df = final_df.join(perc1, on=['Time', 'runType', 'Ecosystem Element'])
    perc2 = final_df.groupby(['Time', 'runType', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    final_df = final_df.join(perc2, on=['Time','runType', 'Ecosystem Element'])
    colors = ["#6788ee", "#e26952", "#3F9E4D"]

    final_df.to_csv("/Users/emilyneil/Desktop/KneppABM/many_outputs/one_perc/combined_df.csv")


    # first graph: counterfactual & forecasting
    counterfactual_graph = final_df.loc[(final_df['runType'] == "Accepted") | (final_df['runType'] == "noReintro")]
    counterfactual_graph = counterfactual_graph.reset_index(drop=True)

    f = sns.FacetGrid(counterfactual_graph, col="Ecosystem Element", hue = "runType", palette = colors, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'fivePerc')
    f.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    for ax in f.axes.flat:
        ax.fill_between(ax.lines[2].get_xdata(),ax.lines[2].get_ydata(), ax.lines[4].get_ydata(), color = '#6788ee', alpha =0.2)
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[5].get_ydata(), color = '#e26952', alpha=0.2)
        ax.set_ylabel('Abundance')
    # add subplot titles
    axes = f.axes.flatten()
    # fill between the quantiles
    axes[0].set_title("Roe deer")
    axes[1].set_title("Exmoor pony")
    axes[2].set_title("Fallow deer")
    axes[3].set_title("Longhorn cattle")
    axes[4].set_title("Red deer")
    axes[5].set_title("Tamworth pigs")
    axes[6].set_title("Grassland")
    axes[7].set_title("Woodland")
    axes[8].set_title("Thorny scrub")
    axes[9].set_title("Bare ground")
    # add filter lines
    f.axes[1].vlines(x=123,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=123,ymin=104,ymax=127, color='r')
    f.axes[5].vlines(x=123,ymin=20,ymax=24, color='r')
    # May 2015
    f.axes[3].vlines(x=124,ymin=116,ymax=142, color='r')
    f.axes[5].vlines(x=124,ymin=13,ymax=15, color='r')
    f.axes[1].vlines(x=124,ymin=9,ymax=11, color='r')
    # June 2015
    f.axes[3].vlines(x=125,ymin=116,ymax=142, color='r')
    f.axes[1].vlines(x=125,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=125,ymin=13,ymax=15, color='r')
    # July 2015
    f.axes[3].vlines(x=126,ymin=116,ymax=142, color='r')
    f.axes[1].vlines(x=126,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=126,ymin=13,ymax=15, color='r')
    # Aug 2015
    f.axes[3].vlines(x=127,ymin=116,ymax=142, color='r')
    f.axes[1].vlines(x=127,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=127,ymin=13,ymax=15, color='r')
    # Sept 2015
    f.axes[3].vlines(x=128,ymin=117,ymax=143, color='r')
    f.axes[1].vlines(x=128,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=128,ymin=13,ymax=15, color='r')
    # Oct 2015
    f.axes[3].vlines(x=129,ymin=82,ymax=100, color='r')
    f.axes[1].vlines(x=129,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=129,ymin=13,ymax=15, color='r')
    # Nov 2015
    f.axes[3].vlines(x=130,ymin=82,ymax=100, color='r')
    f.axes[1].vlines(x=130,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=130,ymin=12,ymax=14, color='r')
    # Dec 2015
    f.axes[3].vlines(x=131,ymin=77,ymax=94, color='r')
    f.axes[1].vlines(x=131,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=131,ymin=12,ymax=14, color='r')
    # Jan 2016
    f.axes[3].vlines(x=132,ymin=77,ymax=94, color='r')
    f.axes[1].vlines(x=132,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=132,ymin=9,ymax=11, color='r')
    # Feb 2016
    f.axes[1].vlines(x=133,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=133,ymin=77,ymax=94, color='r')
    f.axes[5].vlines(x=133,ymin=7,ymax=9, color='r')
    # March 2016
    f.axes[1].vlines(x=134,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=134,ymin=77,ymax=94, color='r')
    f.axes[2].vlines(x=134,ymin=126,ymax=154, color='r')
    f.axes[4].vlines(x=134,ymin=23,ymax=29, color='r')
    f.axes[5].vlines(x=134,ymin=8,ymax=10, color='r')
    # April 2016
    f.axes[1].vlines(x=135,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=135,ymin=93,ymax=113, color='r')
    f.axes[5].vlines(x=135,ymin=8,ymax=10, color='r')
    # May 2016
    f.axes[1].vlines(x=136,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=136,ymin=97,ymax=119, color='r')
    f.axes[5].vlines(x=136,ymin=15,ymax=19, color='r')
    # June 2016
    f.axes[1].vlines(x=137,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=137,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=137,ymin=15,ymax=19, color='r')
    # July 2016
    f.axes[1].vlines(x=138,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=138,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=138,ymin=15,ymax=19, color='r')
    # Aug 2016
    f.axes[1].vlines(x=139,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=139,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=139,ymin=15,ymax=19, color='r')
    # Sept 2016
    f.axes[1].vlines(x=140,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=140,ymin=87,ymax=107, color='r')
    f.axes[5].vlines(x=140,ymin=15,ymax=19, color='r')
    # Oct 2016
    f.axes[1].vlines(x=141,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=141,ymin=87,ymax=107, color='r')
    f.axes[5].vlines(x=141,ymin=15,ymax=19, color='r')
    # Nov 2016
    f.axes[1].vlines(x=142,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=142,ymin=83,ymax=101, color='r')
    f.axes[5].vlines(x=142,ymin=15,ymax=19, color='r')
    # Dec 2016
    f.axes[1].vlines(x=143,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=143,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=143,ymin=12,ymax=14, color='r')
    # Jan 2017
    f.axes[1].vlines(x=144,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=144,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=144,ymin=8,ymax=10, color='r')
    # Feb 2017
    f.axes[1].vlines(x=145,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=145,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=145,ymin=6,ymax=8, color='r')
    # March 2017
    f.axes[1].vlines(x=146,ymin=9,ymax=11, color='r')
    f.axes[2].vlines(x=146,ymin=149,ymax=182, color='r')
    f.axes[3].vlines(x=146,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=146,ymin=6,ymax=8, color='r')
    # April 2017
    f.axes[1].vlines(x=147,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=147,ymin=90,ymax=110, color='r')
    f.axes[5].vlines(x=147,ymin=20,ymax=24, color='r')
    # May 2017
    f.axes[1].vlines(x=148,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=148,ymin=98,ymax=120, color='r')
    f.axes[5].vlines(x=148,ymin=20,ymax=24, color='r')
    # June 2017
    f.axes[1].vlines(x=149,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=149,ymin=85,ymax=103, color='r')
    f.axes[5].vlines(x=149,ymin=20,ymax=24, color='r')
    # July 2017
    f.axes[1].vlines(x=150,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=150,ymin=85,ymax=103, color='r')
    f.axes[5].vlines(x=150,ymin=20,ymax=24, color='r')
    # Aug 2017
    f.axes[1].vlines(x=151,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=151,ymin=85,ymax=103, color='r')
    f.axes[5].vlines(x=151,ymin=20,ymax=24, color='r')
    # Sept 2017
    f.axes[1].vlines(x=152,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=152,ymin=81,ymax=99, color='r')
    f.axes[5].vlines(x=152,ymin=20,ymax=24, color='r')
    # Oct 2017
    f.axes[1].vlines(x=153,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=153,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=153,ymin=20,ymax=24, color='r')
    # Nov 2017
    f.axes[1].vlines(x=154,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=154,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=154,ymin=20,ymax=24, color='r')
    # Dec 2017
    f.axes[1].vlines(x=155,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=155,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=155,ymin=16,ymax=20, color='r')
    # Jan 2018
    f.axes[1].vlines(x=156,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=156,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=156,ymin=10,ymax=12, color='r')
    # Feb 2018
    f.axes[1].vlines(x=157,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=157,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=157,ymin=14,ymax=18, color='r')
    # March 2018
    f.axes[1].vlines(x=158,ymin=8,ymax=10, color='r')
    f.axes[2].vlines(x=158,ymin=226,ymax=276, color='r')
    f.axes[3].vlines(x=158,ymin=79,ymax=97, color='r')
    f.axes[4].vlines(x=158,ymin=22,ymax=26, color='r')
    f.axes[5].vlines(x=158,ymin=14,ymax=18, color='r')
    # April 2018
    f.axes[1].vlines(x=159,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=159,ymin=91,ymax=111, color='r')
    f.axes[5].vlines(x=159,ymin=14,ymax=18, color='r')
    # May 2018
    f.axes[1].vlines(x=160,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=160,ymin=105,ymax=129, color='r')
    f.axes[5].vlines(x=160,ymin=21,ymax=25, color='r')
    # June 2018
    f.axes[1].vlines(x=161,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=161,ymin=93,ymax=113, color='r')
    f.axes[5].vlines(x=161,ymin=21,ymax=25, color='r')
    # July 2018
    f.axes[1].vlines(x=162,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=162,ymin=93,ymax=113, color='r')
    f.axes[5].vlines(x=162,ymin=20,ymax=24, color='r')
    # Aug 2018
    f.axes[3].vlines(x=163,ymin=92,ymax=112, color='r')
    f.axes[5].vlines(x=163,ymin=20,ymax=24, color='r')
    # Sept 2018
    f.axes[3].vlines(x=164,ymin=95,ymax=117, color='r')
    f.axes[5].vlines(x=164,ymin=20,ymax=24, color='r')
    # Oct 2018
    f.axes[3].vlines(x=165,ymin=91,ymax=111, color='r')
    f.axes[5].vlines(x=165,ymin=19,ymax=23, color='r')
    # Nov 2018
    f.axes[3].vlines(x=166,ymin=84,ymax=102, color='r')
    f.axes[5].vlines(x=166,ymin=8,ymax=10, color='r')
    # Dec 2018
    f.axes[3].vlines(x=167,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=167,ymin=8,ymax=10, color='r')
    # Jan 2019
    f.axes[3].vlines(x=168,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=168,ymin=8,ymax=10, color='r')
    # Feb 2019
    f.axes[3].vlines(x=169,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=169,ymin=9,ymax=11, color='r')
    # March 2019
    f.axes[2].vlines(x=170,ymin=250,ymax=306, color='r')
    f.axes[3].vlines(x=170,ymin=78,ymax=96, color='r')
    f.axes[4].vlines(x=170,ymin=33,ymax=41, color='r')
    f.axes[5].vlines(x=170,ymin=8,ymax=10, color='r')
    # April 2019
    f.axes[3].vlines(x=171,ymin=91,ymax=111, color='r')
    f.axes[5].vlines(x=171,ymin=7,ymax=9, color='r')
    # May 2019
    f.axes[3].vlines(x=172,ymin=99,ymax=121, color='r')
    f.axes[5].vlines(x=172,ymin=7,ymax=9, color='r')
    # June 2019
    f.axes[3].vlines(x=173,ymin=80,ymax=98, color='r')
    f.axes[5].vlines(x=173,ymin=7,ymax=9, color='r')
    # July 2019
    f.axes[3].vlines(x=174,ymin=82,ymax=100, color='r')
    f.axes[5].vlines(x=174,ymin=8,ymax=10, color='r')
    # Aug 2019
    f.axes[3].vlines(x=175,ymin=82,ymax=100, color='r')
    f.axes[5].vlines(x=175,ymin=8,ymax=10, color='r')  
    # Sept 2019
    f.axes[3].vlines(x=176,ymin=84,ymax=102, color='r')
    f.axes[5].vlines(x=176,ymin=8,ymax=10, color='r')
    # Oct 2019
    f.axes[3].vlines(x=177,ymin=79,ymax=97, color='r')
    f.axes[5].vlines(x=177,ymin=8,ymax=10, color='r')
    # Nov 2019
    f.axes[3].vlines(x=178,ymin=78,ymax=96, color='r')
    f.axes[5].vlines(x=178,ymin=8,ymax=10, color='r')
    # Dec 2019
    f.axes[3].vlines(x=179,ymin=72,ymax=88, color='r')
    f.axes[5].vlines(x=179,ymin=9,ymax=11, color='r')
    # Jan 2020
    f.axes[3].vlines(x=180,ymin=72,ymax=88, color='r')
    f.axes[5].vlines(x=180,ymin=9,ymax=11, color='r')
    # Feb 2020
    f.axes[3].vlines(x=181,ymin=71,ymax=87, color='r')
    f.axes[5].vlines(x=181,ymin=7,ymax=9, color='r')
    # March 2020
    f.axes[2].vlines(x=182,ymin=222,ymax=272, color='r')
    f.axes[4].vlines(x=182,ymin=32,ymax=39, color='r')
    f.axes[3].vlines(x=182,ymin=73,ymax=89, color='r')
    f.axes[5].vlines(x=182,ymin=6,ymax=8, color='r')
    # April 2020
    f.axes[1].vlines(x=183,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=183,ymin=73,ymax=89, color='r')
    f.axes[5].vlines(x=183,ymin=6,ymax=8, color='r')
    # plot next set of filter lines
    f.axes[0].vlines(x=184,ymin=20,ymax=80, color='r')
    f.axes[1].vlines(x=184,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=184,ymin=73,ymax=89, color='r')
    f.axes[5].vlines(x=184,ymin=17,ymax=21, color='r')
    f.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    f.axes[7].vlines(x=184,ymin=9,ymax=29, color='r')
    f.axes[8].vlines(x=184,ymin=21,ymax=35, color='r')

    # # stop the plots from overlapping
    f.fig.suptitle('Forecasting herbivore reintroductions vs. no reintroductions')
    plt.tight_layout()
    plt.legend(labels=['Reintroductions', 'No reintroductions'],bbox_to_anchor=(2.2, 0),loc='lower right', fontsize=12)
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs/one_perc/counterfactual.png')
    plt.show()


    # second graph: accepted vs rejected runs
    final_df = final_df.reset_index(drop=True)
    filtered_rejectedAccepted = final_df.loc[(final_df['runType'] == "Accepted") | (final_df['runType'] == "Rejected") ]
    g = sns.FacetGrid(filtered_rejectedAccepted, col="Ecosystem Element", hue = "runType", palette = colors, col_wrap=4, sharey = False)
    g.map(sns.lineplot, 'Time', 'Median')
    g.map(sns.lineplot, 'Time', 'fivePerc')
    g.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    for ax in g.axes.flat:
        ax.fill_between(ax.lines[2].get_xdata(),ax.lines[2].get_ydata(), ax.lines[4].get_ydata(), color = '#6788ee', alpha =0.2)
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[5].get_ydata(), color = '#e26952', alpha=0.2)
        ax.set_ylabel('Abundance')
    # add subplot titles
    axes = g.axes.flatten()
    # fill between the quantiles
    axes[0].set_title("Roe deer")
    axes[1].set_title("Exmoor pony")
    axes[2].set_title("Fallow deer")
    axes[3].set_title("Longhorn cattle")
    axes[4].set_title("Red deer")
    axes[5].set_title("Tamworth pigs")
    axes[6].set_title("Grassland")
    axes[7].set_title("Woodland")
    axes[8].set_title("Thorny scrub")
    axes[9].set_title("Bare ground")
    # add filter lines
    g.axes[0].vlines(x=50,ymin=6,ymax=40, color='r')
    g.axes[6].vlines(x=50,ymin=49,ymax=90, color='r')
    g.axes[7].vlines(x=50,ymin=7,ymax=27, color='r')
    g.axes[8].vlines(x=50,ymin=1,ymax=21, color='r')
    # plot post-reintro lines: April 2015
    g.axes[1].vlines(x=123,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=123,ymin=104,ymax=127, color='r')
    g.axes[5].vlines(x=123,ymin=20,ymax=24, color='r')
    # May 2015
    g.axes[3].vlines(x=124,ymin=116,ymax=142, color='r')
    g.axes[5].vlines(x=124,ymin=13,ymax=15, color='r')
    g.axes[1].vlines(x=124,ymin=9,ymax=11, color='r')
    # June 2015
    g.axes[3].vlines(x=125,ymin=116,ymax=142, color='r')
    g.axes[1].vlines(x=125,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=125,ymin=13,ymax=15, color='r')
    # July 2015
    g.axes[3].vlines(x=126,ymin=116,ymax=142, color='r')
    g.axes[1].vlines(x=126,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=126,ymin=13,ymax=15, color='r')
    # Aug 2015
    g.axes[3].vlines(x=127,ymin=116,ymax=142, color='r')
    g.axes[1].vlines(x=127,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=127,ymin=13,ymax=15, color='r')
    # Sept 2015
    g.axes[3].vlines(x=128,ymin=117,ymax=143, color='r')
    g.axes[1].vlines(x=128,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=128,ymin=13,ymax=15, color='r')
    # Oct 2015
    g.axes[3].vlines(x=129,ymin=82,ymax=100, color='r')
    g.axes[1].vlines(x=129,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=129,ymin=13,ymax=15, color='r')
    # Nov 2015
    g.axes[3].vlines(x=130,ymin=82,ymax=100, color='r')
    g.axes[1].vlines(x=130,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=130,ymin=12,ymax=14, color='r')
    # Dec 2015
    g.axes[3].vlines(x=131,ymin=77,ymax=94, color='r')
    g.axes[1].vlines(x=131,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=131,ymin=12,ymax=14, color='r')
    # Jan 2016
    g.axes[3].vlines(x=132,ymin=77,ymax=94, color='r')
    g.axes[1].vlines(x=132,ymin=9,ymax=11, color='r')
    g.axes[5].vlines(x=132,ymin=9,ymax=11, color='r')
    # Feb 2016
    g.axes[1].vlines(x=133,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=133,ymin=77,ymax=94, color='r')
    g.axes[5].vlines(x=133,ymin=7,ymax=9, color='r')
    # March 2016
    g.axes[1].vlines(x=134,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=134,ymin=77,ymax=94, color='r')
    g.axes[2].vlines(x=134,ymin=126,ymax=154, color='r')
    g.axes[4].vlines(x=134,ymin=23,ymax=29, color='r')
    g.axes[5].vlines(x=134,ymin=8,ymax=10, color='r')
    # April 2016
    g.axes[1].vlines(x=135,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=135,ymin=93,ymax=113, color='r')
    g.axes[5].vlines(x=135,ymin=8,ymax=10, color='r')
    # May 2016
    g.axes[1].vlines(x=136,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=136,ymin=97,ymax=119, color='r')
    g.axes[5].vlines(x=136,ymin=15,ymax=19, color='r')
    # June 2016
    g.axes[1].vlines(x=137,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=137,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=137,ymin=15,ymax=19, color='r')
    # July 2016
    g.axes[1].vlines(x=138,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=138,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=138,ymin=15,ymax=19, color='r')
    # Aug 2016
    g.axes[1].vlines(x=139,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=139,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=139,ymin=15,ymax=19, color='r')
    # Sept 2016
    g.axes[1].vlines(x=140,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=140,ymin=87,ymax=107, color='r')
    g.axes[5].vlines(x=140,ymin=15,ymax=19, color='r')
    # Oct 2016
    g.axes[1].vlines(x=141,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=141,ymin=87,ymax=107, color='r')
    g.axes[5].vlines(x=141,ymin=15,ymax=19, color='r')
    # Nov 2016
    g.axes[1].vlines(x=142,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=142,ymin=83,ymax=101, color='r')
    g.axes[5].vlines(x=142,ymin=15,ymax=19, color='r')
    # Dec 2016
    g.axes[1].vlines(x=143,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=143,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=143,ymin=12,ymax=14, color='r')
    # Jan 2017
    g.axes[1].vlines(x=144,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=144,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=144,ymin=8,ymax=10, color='r')
    # Feb 2017
    g.axes[1].vlines(x=145,ymin=10,ymax=12, color='r')
    g.axes[3].vlines(x=145,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=145,ymin=6,ymax=8, color='r')
    # March 2017
    g.axes[1].vlines(x=146,ymin=9,ymax=11, color='r')
    g.axes[2].vlines(x=146,ymin=149,ymax=182, color='r')
    g.axes[3].vlines(x=146,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=146,ymin=6,ymax=8, color='r')
    # April 2017
    g.axes[1].vlines(x=147,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=147,ymin=90,ymax=110, color='r')
    g.axes[5].vlines(x=147,ymin=20,ymax=24, color='r')
    # May 2017
    g.axes[1].vlines(x=148,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=148,ymin=98,ymax=120, color='r')
    g.axes[5].vlines(x=148,ymin=20,ymax=24, color='r')
    # June 2017
    g.axes[1].vlines(x=149,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=149,ymin=85,ymax=103, color='r')
    g.axes[5].vlines(x=149,ymin=20,ymax=24, color='r')
    # July 2017
    g.axes[1].vlines(x=150,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=150,ymin=85,ymax=103, color='r')
    g.axes[5].vlines(x=150,ymin=20,ymax=24, color='r')
    # Aug 2017
    g.axes[1].vlines(x=151,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=151,ymin=85,ymax=103, color='r')
    g.axes[5].vlines(x=151,ymin=20,ymax=24, color='r')
    # Sept 2017
    g.axes[1].vlines(x=152,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=152,ymin=81,ymax=99, color='r')
    g.axes[5].vlines(x=152,ymin=20,ymax=24, color='r')
    # Oct 2017
    g.axes[1].vlines(x=153,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=153,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=153,ymin=20,ymax=24, color='r')
    # Nov 2017
    g.axes[1].vlines(x=154,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=154,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=154,ymin=20,ymax=24, color='r')
    # Dec 2017
    g.axes[1].vlines(x=155,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=155,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=155,ymin=16,ymax=20, color='r')
    # Jan 2018
    g.axes[1].vlines(x=156,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=156,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=156,ymin=10,ymax=12, color='r')
    # Feb 2018
    g.axes[1].vlines(x=157,ymin=9,ymax=11, color='r')
    g.axes[3].vlines(x=157,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=157,ymin=14,ymax=18, color='r')
    # March 2018
    g.axes[1].vlines(x=158,ymin=8,ymax=10, color='r')
    g.axes[2].vlines(x=158,ymin=226,ymax=276, color='r')
    g.axes[3].vlines(x=158,ymin=79,ymax=97, color='r')
    g.axes[4].vlines(x=158,ymin=22,ymax=26, color='r')
    g.axes[5].vlines(x=158,ymin=14,ymax=18, color='r')
    # April 2018
    g.axes[1].vlines(x=159,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=159,ymin=91,ymax=111, color='r')
    g.axes[5].vlines(x=159,ymin=14,ymax=18, color='r')
    # May 2018
    g.axes[1].vlines(x=160,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=160,ymin=105,ymax=129, color='r')
    g.axes[5].vlines(x=160,ymin=21,ymax=25, color='r')
    # June 2018
    g.axes[1].vlines(x=161,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=161,ymin=93,ymax=113, color='r')
    g.axes[5].vlines(x=161,ymin=21,ymax=25, color='r')
    # July 2018
    g.axes[1].vlines(x=162,ymin=8,ymax=10, color='r')
    g.axes[3].vlines(x=162,ymin=93,ymax=113, color='r')
    g.axes[5].vlines(x=162,ymin=20,ymax=24, color='r')
    # Aug 2018
    g.axes[3].vlines(x=163,ymin=92,ymax=112, color='r')
    g.axes[5].vlines(x=163,ymin=20,ymax=24, color='r')
    # Sept 2018
    g.axes[3].vlines(x=164,ymin=95,ymax=117, color='r')
    g.axes[5].vlines(x=164,ymin=20,ymax=24, color='r')
    # Oct 2018
    g.axes[3].vlines(x=165,ymin=91,ymax=111, color='r')
    g.axes[5].vlines(x=165,ymin=19,ymax=23, color='r')
    # Nov 2018
    g.axes[3].vlines(x=166,ymin=84,ymax=102, color='r')
    g.axes[5].vlines(x=166,ymin=8,ymax=10, color='r')
    # Dec 2018
    g.axes[3].vlines(x=167,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=167,ymin=8,ymax=10, color='r')
    # Jan 2019
    g.axes[3].vlines(x=168,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=168,ymin=8,ymax=10, color='r')
    # Feb 2019
    g.axes[3].vlines(x=169,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=169,ymin=9,ymax=11, color='r')
    # March 2019
    g.axes[2].vlines(x=170,ymin=250,ymax=306, color='r')
    g.axes[3].vlines(x=170,ymin=78,ymax=96, color='r')
    g.axes[4].vlines(x=170,ymin=33,ymax=41, color='r')
    g.axes[5].vlines(x=170,ymin=8,ymax=10, color='r')
    # April 2019
    g.axes[3].vlines(x=171,ymin=91,ymax=111, color='r')
    g.axes[5].vlines(x=171,ymin=7,ymax=9, color='r')
    # May 2019
    g.axes[3].vlines(x=172,ymin=99,ymax=121, color='r')
    g.axes[5].vlines(x=172,ymin=7,ymax=9, color='r')
    # June 2019
    g.axes[3].vlines(x=173,ymin=80,ymax=98, color='r')
    g.axes[5].vlines(x=173,ymin=7,ymax=9, color='r')
    # July 2019
    g.axes[3].vlines(x=174,ymin=82,ymax=100, color='r')
    g.axes[5].vlines(x=174,ymin=8,ymax=10, color='r')
    # Aug 2019
    g.axes[3].vlines(x=175,ymin=82,ymax=100, color='r')
    g.axes[5].vlines(x=175,ymin=8,ymax=10, color='r')  
    # Sept 2019
    g.axes[3].vlines(x=176,ymin=84,ymax=102, color='r')
    g.axes[5].vlines(x=176,ymin=8,ymax=10, color='r')
    # Oct 2019
    g.axes[3].vlines(x=177,ymin=79,ymax=97, color='r')
    g.axes[5].vlines(x=177,ymin=8,ymax=10, color='r')
    # Nov 2019
    g.axes[3].vlines(x=178,ymin=78,ymax=96, color='r')
    g.axes[5].vlines(x=178,ymin=8,ymax=10, color='r')
    # Dec 2019
    g.axes[3].vlines(x=179,ymin=72,ymax=88, color='r')
    g.axes[5].vlines(x=179,ymin=9,ymax=11, color='r')
    # Jan 2020
    g.axes[3].vlines(x=180,ymin=72,ymax=88, color='r')
    g.axes[5].vlines(x=180,ymin=9,ymax=11, color='r')
    # Feb 2020
    g.axes[3].vlines(x=181,ymin=71,ymax=87, color='r')
    g.axes[5].vlines(x=181,ymin=7,ymax=9, color='r')
    # March 2020
    g.axes[2].vlines(x=182,ymin=222,ymax=272, color='r')
    g.axes[4].vlines(x=182,ymin=32,ymax=39, color='r')
    g.axes[3].vlines(x=182,ymin=73,ymax=89, color='r')
    g.axes[5].vlines(x=182,ymin=6,ymax=8, color='r')
    # April 2020
    g.axes[1].vlines(x=183,ymin=14,ymax=17, color='r')
    g.axes[3].vlines(x=183,ymin=73,ymax=89, color='r')
    g.axes[5].vlines(x=183,ymin=6,ymax=8, color='r')
    # plot next set of filter lines
    g.axes[0].vlines(x=184,ymin=20,ymax=80, color='r')
    g.axes[1].vlines(x=184,ymin=14,ymax=17, color='r')
    g.axes[3].vlines(x=184,ymin=73,ymax=89, color='r')
    g.axes[5].vlines(x=184,ymin=17,ymax=21, color='r')
    g.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    g.axes[7].vlines(x=184,ymin=9,ymax=29, color='r')
    g.axes[8].vlines(x=184,ymin=21,ymax=35, color='r')
    # stop the plots from overlapping
    g.fig.suptitle('Accepted vs. Rejected Runs')
    plt.tight_layout()
    plt.legend(labels=['Rejected Runs', 'Accepted Runs'],bbox_to_anchor=(2.2, 0), loc='lower right', fontsize=12)
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/many_outputs/one_perc/rejected_accepted_runs.png')
    plt.show()

graph_runs()
