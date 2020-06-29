"""Functions used for visualizing data."""


# Import libraries and functions
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from spotify_tools import *
from model_tools import *



def plot_columns(input_df):
    """Plot distributions of all feature columns from a dataframe."""
    # Drop the irrelevant columns
    all_features = drop_cols(input_df)

    # Plot the distributions
    fig, axs = plt.subplots(len(all_features.columns), figsize = (16,80))
    for num, col in enumerate(all_features.columns):
        _ = sns.distplot(all_features[col], kde=False, ax=axs[num])



def plot_popularity(input_df):
    """Plot the distribution of track popularity."""
    # Plot and format the results
    plt.figure(figsize=(14,6))
    _ = sns.distplot(input_df['Track_Popularity'], kde=False, bins=np.array(range(0,100,2)))
    plt.xlabel('Popularity Score', fontsize=18)
    plt.xlim(0, 100)
    plt.xticks(fontsize=14)

    plt.ylabel('# of Tracks', fontsize=18)
    plt.yticks(fontsize=14)



def plot_correlations(input_df):
    """Plot the correlations of the dataframe features."""
    # Drop the irrelevant columns
    all_features = drop_cols(input_df)

    # Get the correlations and plot them
    corr = all_features.corr()
    plt.figure(figsize=(10,8))
    _ = sns.heatmap(corr, cmap='RdBu_r', vmin=-1, vmax=1)