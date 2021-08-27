# graph the runs
from run_experiments import run_counterfactual
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def graph_runs():
    number_simulations, final_results, counterfactual, accepted_parameters = run_counterfactual()

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
    species_list_finaldf = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 51*number_simulations) 
    species_list_counterfactual = np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland", "Thorny Scrub", "Bare ground"], 51*len(accepted_parameters))
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


    # first graph: counterfactual & forecasting
    counterfactual_graph = final_df.loc[(final_df['runType'] == "Accepted") | (final_df['runType'] == "noReintro")]
    g = sns.FacetGrid(counterfactual_graph, col="Ecosystem Element", hue = "runType", palette = colors, col_wrap=4, sharey = False)
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
    # plot next set of filter lines
    # g.axes[0].vlines(x=184,ymin=20,ymax=40, color='r')
    # g.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    # g.axes[7].vlines(x=184,ymin=21,ymax=35, color='r')
    # g.axes[8].vlines(x=184,ymin=9,ymax=29, color='r')
    # # stop the plots from overlapping
    plt.tight_layout()
    plt.legend(labels=['Reintroductions', 'No reintroductions'],bbox_to_anchor=(2.2, 0),loc='lower right', fontsize=12)
    plt.show()



    # second graph: accepted vs rejected runs
    filtered_rejectedAccepted = final_df.loc[(final_df['runType'] == "Accepted") | (final_df['runType'] == "Rejected") ]
    r = sns.FacetGrid(filtered_rejectedAccepted, col="Ecosystem Element", hue = "runType", palette = colors, col_wrap=4, sharey = False)
    r.map(sns.lineplot, 'Time', 'Median')
    r.map(sns.lineplot, 'Time', 'fivePerc')
    r.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    for ax in r.axes.flat:
        ax.fill_between(ax.lines[2].get_xdata(),ax.lines[2].get_ydata(), ax.lines[4].get_ydata(), color = '#6788ee', alpha =0.2)
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[5].get_ydata(), color = '#e26952', alpha=0.2)
        ax.set_ylabel('Abundance')
    # add subplot titles
    axes = r.axes.flatten()
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
    r.axes[0].vlines(x=50,ymin=6,ymax=40, color='r')
    r.axes[6].vlines(x=50,ymin=49,ymax=90, color='r')
    r.axes[7].vlines(x=50,ymin=1,ymax=21, color='r')
    r.axes[8].vlines(x=50,ymin=7,ymax=27, color='r')
    # plot next set of filter lines
    # r.axes[0].vlines(x=184,ymin=20,ymax=40, color='r')
    # r.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    # r.axes[7].vlines(x=184,ymin=21,ymax=35, color='r')
    # r.axes[8].vlines(x=184,ymin=9,ymax=29, color='r')
    # stop the plots from overlapping
    plt.tight_layout()
    plt.legend(labels=['Rejected Runs', 'Accepted Runs'],bbox_to_anchor=(2.2, 0), loc='lower right', fontsize=12)
    plt.show()

graph_runs()
