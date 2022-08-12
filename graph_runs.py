# graph the runs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import os
import itertools    
import gc
from scipy import stats
import matplotlib.patches as mpatches
import xarray as xr


def organise_output_data():

    # # check which filters were hardest to pass; open and merge files 
    # filter_files = glob.glob(os.path.join("outputs/perc_bound_experiments/fifty_perc_copy/", "difficult_filters*.csv"))
    # final_filters = pd.concat(map(pd.read_csv, filter_files), ignore_index=True).iloc[: , 1:]
    # # sum filters & add row where filter_number = 0 and times_passed = 100000 for starting condition so we can divide them
    # summed_filters = final_filters.groupby(['filter_number'], as_index=False).sum().append({'times_passed': 100000, 'filter_number':0}, ignore_index = True)
    # # add proportion to find bottlenecks 
    # sorted = summed_filters.sort_values('times_passed', ascending=True)
    # sorted.to_excel("sorted_filters.xlsx")

    # setting the path for joining multiple files & list of merged files returned
    files = glob.glob(os.path.join("outputs/perc_bound_experiments/fifty_perc_copy/", "final_results*.csv"))
    parameter_files = glob.glob(os.path.join("outputs/perc_bound_experiments/fifty_perc_copy/", "all_parameters*.csv"))

    # # make sure run_numbers don't overlap
    # numbers = 0
    # for f in files:
    #     for pf in parameter_files:
    #         a, b = f.split('_'), pf.split('_')
    #         if a[6] == b[6]: # check this each time
    #             df, df1 = pd.read_csv(f), pd.read_csv(pf)
    #             df['run_number'] = df['run_number'] + numbers
    #             df1['run_number'] = df1['run_number'] + numbers
    #             numbers += 10000
    #             df.to_csv(f'{f}')
    #             df1.to_csv(f'{pf}')

    # create a temporary file with only the last year that passed habs filters, filters passed
    last_year_accepted_habitats = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        # drop the first two columns
        df = df.iloc[: , 2:]
        # look at only the last year
        last_year = df.loc[df['Time'] == 184]
        # does it pass the habitat filters?
        accepted_habs = last_year.loc[(last_year['Grassland'] <= 69) & (last_year['Grassland'] >= 49) & 
        (last_year['Thorny Scrub'] <= 35) & (last_year["Thorny Scrub"] >= 21) & 
        (last_year["Woodland"] <= 29) & (last_year["Woodland"] >= 9) &
        (last_year["Roe deer"] <= 80) & (last_year["Roe deer"] >= 20)]
        # if yes, append it to the temp dataframe
        last_year_accepted_habitats = last_year_accepted_habitats.append(accepted_habs)
    print(len(last_year_accepted_habitats))

    # take the top 1% of those runs 
    best_results = last_year_accepted_habitats.nlargest(round(last_year_accepted_habitats.shape[0]*0.01), 'passed_filters')
    print(len(best_results))
    # loop through the csvs again
    final_accepted_results = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        # drop first column
        df = df.iloc[: , 2:]
        # if the accepted run_number is there, label as accepted
        df['accepted?'] = np.where(df['run_number'].isin(best_results['run_number']), 'Accepted', 'Rejected')
        accepted_df = df.loc[df['accepted?'] == 'Accepted']
        # and append it to final_results
        final_accepted_results = final_accepted_results.append(accepted_df)

    # pick one df; take the rejected runs and append to a diff dataframe (for graphing)
    temp_df = pd.read_csv(files[0]).iloc[: , 2:]
    temp_df['accepted?'] = np.where(temp_df['run_number'].isin(best_results['run_number']), 'Accepted', 'Rejected')
    temp_df_rejected = temp_df.loc[temp_df['accepted?'] == 'Rejected']

    # concat the dataframes and save to csv
    final_results = pd.concat([final_accepted_results,temp_df_rejected], axis=0)
    final_results.to_csv("combined_results.csv")

    # now find accepted parameters
    final_parameters = pd.concat(map(pd.read_csv, parameter_files), ignore_index=True)
    # drop first column
    final_parameters = final_parameters.iloc[: , 2:] 
    # select the top 1% of parameters
    accepted_parameters = final_parameters[final_parameters['run_number'].isin(best_results['run_number'])]
    accepted_parameters.to_csv("combined_accepted_parameters.csv")

    # use accepted params to run experiments
    from experiments_counterfac_stockingDensity import run_counterfactual
    counterfactual = run_counterfactual(accepted_parameters)
    number_simulations = 100000


def histograms():
    
    final_results = pd.read_csv('combined_results.csv') 
    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv') 

    # KS test
    accepted = accepted_parameters.iloc[:,1:52]
    accepted = accepted.drop(['initial_roeDeer', 'initial_grassland', 'initial_woodland', 'initial_scrubland'], 1)
    for column in accepted:
        print(column,stats.kstest(accepted[column], stats.uniform(loc=min(accepted[column]), scale=(max(accepted[column])-min(accepted[column]))).cdf))
    
    # corr matrix
    corr = accepted.corr()
    # mask the upper triangle; True = do NOT show
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # graph it 
    f, ax = plt.subplots(figsize=(11, 9))
    cmap =sns.diverging_palette(220, 60, l=65, center="light", as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
    heatmap = sns.heatmap(
        corr,          # The data to plot
        mask=mask,     # Mask some cells
        cmap=cmap,     # What colors to plot the heatmap as
        annot=False,    # Should the values be plotted in the cells?
        vmax=1,       # The maximum value of the legend. All higher vals will be same color
        vmin=-1,      # The minimum value of the legend. All lower vals will be same color
        center=0,      # The center value of the legend. With divergent cmap, where white is
        square=True,   # Force cells to be square
        linewidths=0.1, # Width of lines that divide cells
        cbar_kws={"shrink": .5},  # Extra kwargs for the legend; in this case, shrink by 50%
    )
    heatmap.figure.tight_layout()
    plt.savefig('corr_matrix.png')
    plt.show()

    # Histograms
    # 1
    accepted_parameters["chance_reproduceSapling"].hist()
    plt.title("Histogram of chance_reproduceSapling")
    plt.savefig('hist_parameter1.png')
    plt.show()
    # 2
    accepted_parameters["chance_reproduceYoungScrub"].hist()
    plt.title("Histogram of chance_reproduceYoungScrub")
    plt.savefig('hist_parameter2.png')
    plt.show()
    # 3
    accepted_parameters["chance_saplingBecomingTree"].hist()
    plt.title("Histogram of chance_saplingBecomingTree")
    plt.savefig('hist_parameter3.png')
    plt.show()
    # 4
    accepted_parameters["chance_youngScrubMatures"].hist()
    plt.title("Histogram of chance_youngScrubMatures")
    plt.savefig('hist_parameter4.png')
    plt.show()
    # 5
    accepted_parameters["chance_grassOutcompetedByTree"].hist()
    plt.title("Histogram of chance_grassOutcompetedByTree")
    plt.savefig('hist_parameter5.png')
    plt.show()
    # 6
    accepted_parameters["chance_grassOutcompetedByScrub"].hist()
    plt.title("Histogram of chance_grassOutcompetedByScrub")
    plt.savefig('hist_parameter6.png')
    plt.show()
    # 7
    accepted_parameters["chance_saplingOutcompetedByTree"].hist()
    plt.title("Histogram of chance_saplingOutcompetedByTree")
    plt.savefig('hist_parameter7.png')
    plt.show()
    # 8
    accepted_parameters["roeDeer_reproduce"].hist()
    plt.title("Histogram of roeDeer_reproduce")
    plt.savefig('hist_parameter8.png')
    plt.show()
    # 9
    accepted_parameters["cows_reproduce"].hist()
    plt.title("Histogram of cows_reproduce")
    plt.savefig('hist_parameter9.png')
    plt.show()
    # 10
    accepted_parameters["fallowDeer_reproduce"].hist()
    plt.title("Histogram of fallowDeer_reproduce")
    plt.savefig('hist_parameter10.png')
    plt.show()
    # 11
    accepted_parameters["redDeer_reproduce"].hist()
    plt.title("Histogram of redDeer_reproduce")
    plt.savefig('hist_parameter11.png')
    plt.show()
    # 12
    accepted_parameters["pigs_reproduce"].hist()
    plt.title("Histogram of pigs_reproduce")
    plt.savefig('hist_parameter12.png')
    plt.show()



def graph_passed_filters():
    # graph the number of filters passed per % above/below
    palette=['#db5f57', '#57d3db', '#57db5f','#5f57db', '#db57d3']
    filters = pd.read_csv('combined_results.csv')
    filters = filters.loc[filters['Time'] == 184]
    filters["passed_filters"] = filters[["passed_filters"]]/64 # show percentage passed

    d = np.diff(np.unique(filters[['passed_filters']])).min()
    left_of_first_bin = np.unique(filters[['passed_filters']]).min() - float(d)/2
    right_of_last_bin = np.unique(filters[['passed_filters']]).max() + float(d)/2

    fig, ax = plt.subplots()
    sns.histplot(
        data=filters, x='passed_filters', hue='accepted?', multiple='stack',
        ax=ax, palette="hls", bins=np.arange(left_of_first_bin, right_of_last_bin + d, d)
    )
    plt.xlabel("Percentage of filters passed")
    plt.ylabel("Count")
    plt.title("Percentage of filters passed by the accepted runs")
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/filtersPassed_100k.png')
    plt.show()


def graph_hardest_filters():
    final_results = pd.read_csv('combined_results.csv') 
    temp_results = final_results.loc[final_results['Time'] == 184]
    
    fig, ax = plt.subplots()
    sns.histplot(
        data=temp_results, x='Woodland', multiple='stack',
        ax=ax, palette="hls", bins=35) # ,bins = 25

    plt.xlabel("Percentage Woodland")
    plt.ylabel("Count")
    plt.title("Woodland in May 2020")
    # add filter numbers
    left, bottom, width, height = (9, 0, 20 , 30000)
    rect=mpatches.Rectangle((left,bottom),width,height, 
                            alpha=0.1,
                        facecolor="red")
    plt.gca().add_patch(rect)
    plt.savefig('/Users/emilyneil/Desktop/KneppABM/outputs/hardestFilter_wood_May2020.png')
    plt.show()

graph_hardest_filters()

def clean_dataframes():
    # open the counterfactul dataframe
    counterfactual = pd.read_csv('combined_counterfactual.csv').iloc[: , 1:]
    # and main dataframe
    final_results = pd.read_csv('combined_results.csv').iloc[: , 1:]
    # and parameters
    accepted_parameters = pd.read_csv('combined_accepted_parameters.csv').iloc[: , 1:]

     # now create the new df - numbers
    final_df_numbers = pd.DataFrame(np.concatenate([np.repeat(final_results['accepted?'], 12), np.repeat(counterfactual['accepted?'], 12)], axis=0), columns=['runType']).astype("category")
    final_df_numbers["Abundance %"] = pd.DataFrame(np.concatenate(
                    (final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"]].values.flatten(),
                     counterfactual[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"]].values.flatten()), 
                     axis=0))
    final_df_numbers["runNumber"] = pd.DataFrame(np.concatenate([np.repeat(final_results['run_number'], 12), np.repeat(counterfactual['run_number'], 12)], axis=0)).astype("int32")
    final_df_numbers["Time"] = pd.DataFrame(np.concatenate([np.repeat(final_results['Time'], 12), np.repeat(counterfactual['Time'], 12)], axis=0)).astype("int16")
    # this should be len(number_simulations) and len(accepted_parameters)
    final_df_numbers["Ecosystem Element"] = pd.DataFrame(np.concatenate(
        (np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], len(final_results)),
                    np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grass", "Trees", "Mature Scrub", "Saplings", "Young Scrub", "Bare Areas"], 185*len(accepted_parameters))),
                    axis=0)).astype("category")
    # calculate median 
    m = final_df_numbers.groupby(['Time', 'runType', 'Ecosystem Element'])[['Abundance %']].apply(np.median)
    m.name = 'Median'
    final_df_numbers = final_df_numbers.join(m, on=['Time', 'runType', 'Ecosystem Element'])
    # calculate quantiles
    perc1 = final_df_numbers.groupby(['Time', 'runType', 'Ecosystem Element'])['Abundance %'].quantile(.95)
    perc1.name = 'ninetyfivePerc'
    final_df_numbers = final_df_numbers.join(perc1, on=['Time', 'runType', 'Ecosystem Element'])
    perc2 = final_df_numbers.groupby(['Time', 'runType', 'Ecosystem Element'])['Abundance %'].quantile(.05)
    perc2.name = "fivePerc"
    final_df_numbers = final_df_numbers.join(perc2, on=['Time','runType', 'Ecosystem Element'])
    # reset the index
    final_df_numbers = final_df_numbers.reset_index(drop=True)
    final_df_numbers.to_csv("combined_df_numbers.csv")

    # clear memory (so RAM isn't overloaded)
    del final_df_numbers
    gc.collect()

    # now create the new df
    final_df = pd.DataFrame(np.concatenate([np.repeat(final_results['accepted?'], 10), np.repeat(counterfactual['accepted?'], 10)], axis=0), columns=['runType']).astype("category")
    final_df["Abundance %"] = pd.DataFrame(np.concatenate(
                    (final_results[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland","Woodland", "Thorny Scrub","Bare ground"]].values.flatten(),
                     counterfactual[["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Woodland","Thorny Scrub", "Bare ground"]].values.flatten()), 
                     axis=0))
    final_df["runNumber"] = pd.DataFrame(np.concatenate([np.repeat(final_results['run_number'], 10), np.repeat(counterfactual['run_number'], 10)], axis=0)).astype("int32")
    final_df["Time"] = pd.DataFrame(np.concatenate([np.repeat(final_results['Time'], 10), np.repeat(counterfactual['Time'], 10)], axis=0)).astype("int16")
    # this should be len(number_simulations) and len(accepted_parameters)
    final_df["Ecosystem Element"] = pd.DataFrame(np.concatenate(
        (np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs", "Grassland", "Thorny Scrub", "Woodland", "Bare ground"], len(final_results)),
                    np.tile(["Roe deer", "Exmoor pony", "Fallow deer", "Longhorn cattle", "Red deer", "Tamworth pigs",  "Grassland", "Thorny Scrub", "Woodland", "Bare ground"], 185*len(accepted_parameters))),
                    axis=0)).astype("category")
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
    # reset the index
    final_df = final_df.reset_index(drop=True)
    final_df.to_csv("combined_df.csv")


def graph_counterfac():
    # open dataframes
    final_df_numbers = pd.read_csv('combined_df_numbers.csv').iloc[: , 1:]
    final_df = pd.read_csv('combined_df.csv').iloc[: , 1:]

    # COUNTERFACTUAL GRAPHS
    palette=['#db5f57', '#57d3db', '#57db5f','#5f57db', '#db57d3']
    
    # numbers
    final_df_numbers = final_df_numbers.loc[(final_df_numbers['runType'] == "Accepted") | (final_df_numbers['runType'] == "noReintro") ]
    h = sns.FacetGrid(final_df_numbers, col="Ecosystem Element", hue = "runType", palette = palette, col_wrap=5, sharey = False)
    h.map(sns.lineplot, 'Time', 'Median')
    h.map(sns.lineplot, 'Time', 'fivePerc')
    h.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    for ax in h.axes.flat:
        ax.fill_between(ax.lines[2].get_xdata(),ax.lines[2].get_ydata(), ax.lines[4].get_ydata(),color="#db5f57",alpha =0.2)
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[5].get_ydata(), color="#57d3db",alpha=0.2)
        ax.set_xlabel('Time (Months)')
        ax.set_ylabel('Abundance')
    # fill between the quantiles
    axes = h.axes.flatten()
    axes[0].set_title("Roe deer")
    axes[1].set_title("Exmoor pony")
    axes[2].set_title("Fallow deer")
    axes[3].set_title("Longhorn cattle")
    axes[4].set_title("Red deer")
    axes[5].set_title("Tamworth pigs")
    axes[6].set_title("Grass")
    axes[7].set_title("Mature Trees")
    axes[8].set_title("Mature Scrub")
    axes[9].set_title("Saplings")
    axes[10].set_title("Young Scrub")
    axes[11].set_title("Bare ground")
    # stop the plots from overlapping
    h.fig.suptitle("Reintroduction vs. No Reintroduction: Ecosystem Elements & Habitat Components")
    plt.tight_layout()
    plt.legend(labels=['Reintroductions', 'No reintroductions'],bbox_to_anchor=(2.2, 0),loc='lower right', fontsize=12)
    plt.savefig('outputs_numbers_counterfactual.png')
    plt.show()
    
    # conditions
    counterfactual_graph = final_df.loc[(final_df['runType'] == "Accepted") | (final_df['runType'] == "noReintro")]
    counterfactual_graph = counterfactual_graph.reset_index(drop=True)
    f = sns.FacetGrid(counterfactual_graph, col="Ecosystem Element", hue = "runType", palette = palette, col_wrap=4, sharey = False)
    f.map(sns.lineplot, 'Time', 'Median')
    f.map(sns.lineplot, 'Time', 'fivePerc')
    f.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    for ax in f.axes.flat:
        ax.fill_between(ax.lines[2].get_xdata(),ax.lines[2].get_ydata(), ax.lines[4].get_ydata(),  color="#db5f57",alpha =0.2)
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[5].get_ydata(), color="#57d3db",alpha=0.2)
        ax.set_ylabel('Abundance')
        ax.set_xlabel('Time (Months)')
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
    f.axes[0].vlines(x=50,ymin=12,ymax=40, color='r')
    f.axes[6].vlines(x=50,ymin=49,ymax=80, color='r')
    f.axes[7].vlines(x=50,ymin=7,ymax=27, color='r')
    f.axes[8].vlines(x=50,ymin=1,ymax=21, color='r')
    f.axes[1].vlines(x=123,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=123,ymin=90,ymax=140, color='r')
    f.axes[5].vlines(x=123,ymin=12,ymax=32, color='r')
    # May 2015
    f.axes[3].vlines(x=124,ymin=104,ymax=154, color='r')
    f.axes[5].vlines(x=124,ymin=4,ymax=24, color='r')
    f.axes[1].vlines(x=124,ymin=9,ymax=11, color='r')
    # June 2015
    f.axes[3].vlines(x=125,ymin=104,ymax=154, color='r')
    f.axes[1].vlines(x=125,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=125,ymin=4,ymax=24, color='r')
    # July 2015
    f.axes[3].vlines(x=126,ymin=104,ymax=154, color='r')
    f.axes[1].vlines(x=126,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=126,ymin=4,ymax=24, color='r')
    # Aug 2015
    f.axes[3].vlines(x=127,ymin=104,ymax=154, color='r')
    f.axes[1].vlines(x=127,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=127,ymin=4,ymax=24, color='r')
    # Sept 2015
    f.axes[3].vlines(x=128,ymin=105,ymax=155, color='r')
    f.axes[1].vlines(x=128,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=128,ymin=4,ymax=24, color='r')
    # Oct 2015
    f.axes[3].vlines(x=129,ymin=66,ymax=116, color='r')
    f.axes[1].vlines(x=129,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=129,ymin=4,ymax=24, color='r')
    # Nov 2015
    f.axes[3].vlines(x=130,ymin=66,ymax=116, color='r')
    f.axes[1].vlines(x=130,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=130,ymin=3,ymax=23, color='r')
    # Dec 2015
    f.axes[3].vlines(x=131,ymin=61,ymax=111, color='r')
    f.axes[1].vlines(x=131,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=131,ymin=3,ymax=23, color='r')
    # Jan 2016
    f.axes[3].vlines(x=132,ymin=61,ymax=111, color='r')
    f.axes[1].vlines(x=132,ymin=9,ymax=11, color='r')
    f.axes[5].vlines(x=132,ymin=1,ymax=20, color='r')
    # Feb 2016
    f.axes[1].vlines(x=133,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=133,ymin=61,ymax=111, color='r')
    f.axes[5].vlines(x=133,ymin=1,ymax=20, color='r')
    # March 2016
    f.axes[1].vlines(x=134,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=134,ymin=61,ymax=111, color='r')
    f.axes[2].vlines(x=134,ymin=90,ymax=190, color='r')
    f.axes[4].vlines(x=134,ymin=21,ymax=31, color='r')
    f.axes[5].vlines(x=134,ymin=1,ymax=19, color='r')
    # April 2016
    f.axes[1].vlines(x=135,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=135,ymin=78,ymax=128, color='r')
    f.axes[5].vlines(x=135,ymin=1,ymax=19, color='r')
    # May 2016
    f.axes[1].vlines(x=136,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=136,ymin=83,ymax=133, color='r')
    f.axes[5].vlines(x=136,ymin=7,ymax=27, color='r')
    # June 2016
    f.axes[1].vlines(x=137,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=137,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=137,ymin=7,ymax=27, color='r')
    # July 2016
    f.axes[1].vlines(x=138,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=138,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=138,ymin=7,ymax=27, color='r')
    # Aug 2016
    f.axes[1].vlines(x=139,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=139,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=139,ymin=7,ymax=27, color='r')
    # Sept 2016
    f.axes[1].vlines(x=140,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=140,ymin=72,ymax=122, color='r')
    f.axes[5].vlines(x=140,ymin=7,ymax=27, color='r')
    # Oct 2016
    f.axes[1].vlines(x=141,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=141,ymin=72,ymax=122, color='r')
    f.axes[5].vlines(x=141,ymin=7,ymax=27, color='r')
    # Nov 2016
    f.axes[1].vlines(x=142,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=142,ymin=67,ymax=117, color='r')
    f.axes[5].vlines(x=142,ymin=7,ymax=27, color='r')
    # Dec 2016
    f.axes[1].vlines(x=143,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=143,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=143,ymin=3,ymax=23, color='r')
    # Jan 2017
    f.axes[1].vlines(x=144,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=144,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=144,ymin=1,ymax=19, color='r')
    # Feb 2017
    f.axes[1].vlines(x=145,ymin=10,ymax=12, color='r')
    f.axes[3].vlines(x=145,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=145,ymin=1,ymax=17, color='r')
    # March 2017
    f.axes[1].vlines(x=146,ymin=9,ymax=11, color='r')
    f.axes[2].vlines(x=146,ymin=115,ymax=200, color='r')
    f.axes[3].vlines(x=146,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=146,ymin=1,ymax=17, color='r')
    # April 2017
    f.axes[1].vlines(x=147,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=147,ymin=75,ymax=125, color='r')
    f.axes[5].vlines(x=147,ymin=12,ymax=32, color='r')
    # May 2017
    f.axes[1].vlines(x=148,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=148,ymin=84,ymax=134, color='r')
    f.axes[5].vlines(x=148,ymin=12,ymax=32, color='r')
    # June 2017
    f.axes[1].vlines(x=149,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=149,ymin=69,ymax=119, color='r')
    f.axes[5].vlines(x=149,ymin=12,ymax=32, color='r')
    # July 2017
    f.axes[1].vlines(x=150,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=150,ymin=69,ymax=119, color='r')
    f.axes[5].vlines(x=150,ymin=12,ymax=32, color='r')
    # Aug 2017
    f.axes[1].vlines(x=151,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=151,ymin=69,ymax=119, color='r')
    f.axes[5].vlines(x=151,ymin=12,ymax=32, color='r')
    # Sept 2017
    f.axes[1].vlines(x=152,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=152,ymin=65,ymax=115, color='r')
    f.axes[5].vlines(x=152,ymin=20,ymax=24, color='r')
    # Oct 2017
    f.axes[1].vlines(x=153,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=153,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=153,ymin=12,ymax=32, color='r')
    # Nov 2017
    f.axes[1].vlines(x=154,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=154,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=154,ymin=12,ymax=32, color='r')
    # Dec 2017
    f.axes[1].vlines(x=155,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=155,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=155,ymin=8,ymax=28, color='r')
    # Jan 2018
    f.axes[1].vlines(x=156,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=156,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=156,ymin=1,ymax=21, color='r')
    # Feb 2018
    f.axes[1].vlines(x=157,ymin=9,ymax=11, color='r')
    f.axes[3].vlines(x=157,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=157,ymin=6,ymax=26, color='r')
    # March 2018
    f.axes[1].vlines(x=158,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=158,ymin=63,ymax=113, color='r')
    f.axes[4].vlines(x=158,ymin=19,ymax=29, color='r')
    f.axes[5].vlines(x=158,ymin=6,ymax=26, color='r')
    # April 2018
    f.axes[1].vlines(x=159,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=159,ymin=76,ymax=126, color='r')
    f.axes[5].vlines(x=159,ymin=6,ymax=26, color='r')
    # May 2018
    f.axes[1].vlines(x=160,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=160,ymin=92,ymax=142, color='r')
    f.axes[5].vlines(x=160,ymin=13,ymax=33, color='r')
    # June 2018
    f.axes[1].vlines(x=161,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=161,ymin=78,ymax=128, color='r')
    f.axes[5].vlines(x=161,ymin=13,ymax=33, color='r')
    # July 2018
    f.axes[1].vlines(x=162,ymin=8,ymax=10, color='r')
    f.axes[3].vlines(x=162,ymin=78,ymax=128, color='r')
    f.axes[5].vlines(x=162,ymin=12,ymax=32, color='r')
    # Aug 2018
    f.axes[3].vlines(x=163,ymin=77,ymax=127, color='r')
    f.axes[5].vlines(x=163,ymin=12,ymax=32, color='r')
    # Sept 2018
    f.axes[3].vlines(x=164,ymin=81,ymax=131, color='r')
    f.axes[5].vlines(x=164,ymin=12,ymax=32, color='r')
    # Oct 2018
    f.axes[3].vlines(x=165,ymin=76,ymax=126, color='r')
    f.axes[5].vlines(x=165,ymin=11,ymax=31, color='r')
    # Nov 2018
    f.axes[3].vlines(x=166,ymin=68,ymax=118, color='r')
    f.axes[5].vlines(x=166,ymin=1,ymax=19, color='r')
    # Dec 2018
    f.axes[3].vlines(x=167,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=167,ymin=1,ymax=19, color='r')
    # Jan 2019
    f.axes[3].vlines(x=168,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=168,ymin=1,ymax=19, color='r')
    # Feb 2019
    f.axes[3].vlines(x=169,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=169,ymin=1,ymax=20, color='r')
    # March 2019
    f.axes[2].vlines(x=170,ymin=253,ymax=303, color='r')
    f.axes[3].vlines(x=170,ymin=62,ymax=112, color='r')
    f.axes[4].vlines(x=170,ymin=32,ymax=42, color='r')
    f.axes[5].vlines(x=170,ymin=1,ymax=19, color='r')
    # April 2019
    f.axes[3].vlines(x=171,ymin=76,ymax=126, color='r')
    f.axes[5].vlines(x=171,ymin=1,ymax=18, color='r')
    # May 2019
    f.axes[3].vlines(x=172,ymin=85,ymax=135, color='r')
    f.axes[5].vlines(x=172,ymin=1,ymax=18, color='r')
    # June 2019
    f.axes[3].vlines(x=173,ymin=64,ymax=114, color='r')
    f.axes[5].vlines(x=173,ymin=1,ymax=18, color='r')
    # July 2019
    f.axes[3].vlines(x=174,ymin=66,ymax=116, color='r')
    f.axes[5].vlines(x=174,ymin=1,ymax=19, color='r')
    # Aug 2019
    f.axes[3].vlines(x=175,ymin=66,ymax=116, color='r')
    f.axes[5].vlines(x=175,ymin=1,ymax=19, color='r')  
    # Sept 2019
    f.axes[3].vlines(x=176,ymin=68,ymax=118, color='r')
    f.axes[5].vlines(x=176,ymin=1,ymax=19, color='r')
    # Oct 2019
    f.axes[3].vlines(x=177,ymin=63,ymax=113, color='r')
    f.axes[5].vlines(x=177,ymin=1,ymax=19, color='r')
    # Nov 2019
    f.axes[3].vlines(x=178,ymin=62,ymax=112, color='r')
    f.axes[5].vlines(x=178,ymin=1,ymax=19, color='r')
    # Dec 2019
    f.axes[3].vlines(x=179,ymin=55,ymax=105, color='r')
    f.axes[5].vlines(x=179,ymin=1,ymax=20, color='r')
    # Jan 2020
    f.axes[3].vlines(x=180,ymin=55,ymax=105, color='r')
    f.axes[5].vlines(x=180,ymin=1,ymax=20, color='r')
    # Feb 2020
    f.axes[3].vlines(x=181,ymin=54,ymax=104, color='r')
    f.axes[5].vlines(x=181,ymin=1,ymax=18, color='r')
    # March 2020
    f.axes[2].vlines(x=182,ymin=222,ymax=272, color='r')
    f.axes[4].vlines(x=182,ymin=30,ymax=40, color='r')
    f.axes[3].vlines(x=182,ymin=56,ymax=106, color='r')
    f.axes[5].vlines(x=182,ymin=1,ymax=17, color='r')
    # April 2020
    f.axes[1].vlines(x=183,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=183,ymin=56,ymax=106, color='r')
    f.axes[5].vlines(x=183,ymin=1,ymax=17, color='r')
    # plot next set of filter lines
    f.axes[0].vlines(x=184,ymin=20,ymax=80, color='r')
    f.axes[1].vlines(x=184,ymin=14,ymax=17, color='r')
    f.axes[3].vlines(x=184,ymin=56,ymax=106, color='r')
    f.axes[5].vlines(x=184,ymin=9,ymax=29, color='r')
    f.axes[6].vlines(x=184,ymin=49,ymax=69, color='r')
    f.axes[7].vlines(x=184,ymin=9,ymax=29, color='r')
    f.axes[8].vlines(x=184,ymin=21,ymax=35, color='r')
    # stop the plots from overlapping
    f.fig.suptitle('Current dynamics vs. if reintroductions had not occurred')
    plt.tight_layout()
    plt.legend(labels=['Reintroductions', 'No reintroductions'],bbox_to_anchor=(2.2, 0),loc='lower right', fontsize=12)
    plt.savefig('counterfactual.png')
    plt.show()

def graph_accepted_rejected():

    # open dataframes
    final_df = pd.read_csv('combined_df.csv') .iloc[: , 1:]
    palette=['#db5f57', '#57d3db', '#57db5f','#5f57db', '#db57d3']

    # Accepted vs rejected runs
    final_df = final_df.reset_index(drop=True)
    filtered_rejectedAccepted = final_df.loc[(final_df['runType'] == "Accepted") | (final_df['runType'] == "Rejected") ]
    g = sns.FacetGrid(filtered_rejectedAccepted, col="Ecosystem Element", hue = "runType", palette = palette, col_wrap=4, sharey = False)
    g.map(sns.lineplot, 'Time', 'Median')
    g.map(sns.lineplot, 'Time', 'fivePerc')
    g.map(sns.lineplot, 'Time', 'ninetyfivePerc')
    for ax in g.axes.flat:
        ax.fill_between(ax.lines[2].get_xdata(),ax.lines[2].get_ydata(), ax.lines[4].get_ydata(),color="#db5f57", alpha =0.2)
        ax.fill_between(ax.lines[3].get_xdata(),ax.lines[3].get_ydata(), ax.lines[5].get_ydata(), color="#57d3db", alpha=0.2)
        ax.set_ylabel('Abundance')
        ax.set_xlabel('Time (Months)')

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
    g.axes[0].vlines(x=50,ymin=12,ymax=40, color='r')
    g.axes[6].vlines(x=50,ymin=49,ymax=80, color='r')
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
    plt.legend(labels=['Accepted Runs', 'Rejected Runs'],bbox_to_anchor=(2.2, 0), loc='lower right', fontsize=12)
    plt.savefig('rejected_accepted_runs.png')
    plt.show()