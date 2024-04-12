import mesa
from network import Network
import matplotlib.pyplot as plt

import pandas as pd

# Setup the different parameters to test
params = {"K": [4, 10], "infectivity": [0.01, 0.1]}

# Run the batch run
results = mesa.batch_run(
    Network,
    parameters=params,
    iterations=10,
    max_steps=1000,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

# Convert the results to a DataFrame
df = pd.DataFrame(results)
complete_df = df.copy()
df = df.groupby("RunId").last().reset_index()

# Filter the data for each parameter combination
df_k4_i001 = df[(df["K"] == 4) & (df["infectivity"] == 0.01)]
df_k4_i01 = df[(df["K"] == 4) & (df["infectivity"] == 0.1)]
df_k10_i001 = df[(df["K"] == 10) & (df["infectivity"] == 0.01)]
df_k10_i01 = df[(df["K"] == 10) & (df["infectivity"] == 0.1)]

all_df_k4_i001 = complete_df[(complete_df["K"] == 10) & (complete_df["infectivity"] == 0.1)]

# Gather the data for each parameter combination
def average_data(df, k, infectivity, column='Percentage Infected'):
    all_df = df[(df["K"] == k) & (df["infectivity"] == infectivity)]
    all_means = []
    all_min = []
    all_max = []
    for i in range(0, all_df['Step'].max() + 1):
        step_i = all_df[all_df["Step"] == i]
        all_means.append(step_i[column].mean())
        all_min.append(step_i[column].min())
        all_max.append(step_i[column].max())
    return all_df.groupby("RunId").last().reset_index(), all_means, all_min, all_max

# Plot the data
def line_plotter(df_mean, df_min, df_max, cutoff, title, horizontal_line=None):

    plt.plot(df_mean[:cutoff], color='red', label='mean')
    plt.plot(df_min[:cutoff], color='blue', label='min')
    plt.plot(df_max[:cutoff], color='blue', label='max')
    if horizontal_line is not None:
        plt.axhline(horizontal_line, color='green', label='cutoff', linestyle='dotted', xmin=0, xmax=cutoff)
    plt.xlabel("Steps")
    plt.ylabel("Percentage Infected")
    plt.legend()
    plt.title(title)
    plt.show()

# Plot the histogram
def histogram_plotter(df, title, xlim):
    plt.hist(df["Step"], alpha=0.5, label="Steps taken", color='#FFCD00', edgecolor='black')
    plt.xlabel("Steps")
    plt.ylabel("Frequency")
    plt.text(0.95, 0.95, f"Average Steps: {df['Step'].mean():.2f}", ha='right', va='top', transform=plt.gca().transAxes)
    plt.title(title)
    plt.xlim(0, xlim)
    plt.show()

# Call to plot the lines for each parameter combination
def plot_lines():
#To make sure the plot works as intended, go to the network file and set the cutoff to False
    line_plotter(all_df4001_means, all_df4001_min, all_df4001_max, 1000, 'K=4, infectivity=0.01', 0.9)
    line_plotter(all_df4010_means, all_df4010_min, all_df4010_max, 1000, 'K=4, infectivity=0.1', 0.9)
    line_plotter(all_df10001_means, all_df10001_min, all_df10001_max, 1000, 'K=10, infectivity=0.01', 0.9)
    line_plotter(all_df10010_means, all_df10010_min, all_df10010_max, 1000, 'K=10, infectivity=0.1', 0.9)

#call to plot the histograms for each parameter combination
def plot_histograms():
    #To make sure the histograms work as intended, go to the network file and set the cutoff to True
    histogram_plotter(df4001, 'K=4, infectivity=0.01', xlim=1000)
    histogram_plotter(df4010, 'K=4, infectivity=0.1', xlim=400)
    histogram_plotter(df10001, 'K=10, infectivity=0.01', xlim=400)
    histogram_plotter(df10010, 'K=10, infectivity=0.1', xlim=50)

# Call to average the data for each parameter combination
df4001, all_df4001_means, all_df4001_min, all_df4001_max = average_data(complete_df, 4, 0.01)
df4010, all_df4010_means, all_df4010_min, all_df4010_max = average_data(complete_df, 4, 0.1)
df10001, all_df10001_means, all_df10001_min, all_df10001_max = average_data(complete_df, 10, 0.01)
df10010, all_df10010_means, all_df10010_min, all_df10010_max = average_data(complete_df, 10, 0.1)

# Call to plot the lines and histograms, we can only run one at the time since we need 
# to set the cutoff to True or False
#plot_lines()
plot_histograms()