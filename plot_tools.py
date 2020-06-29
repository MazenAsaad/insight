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
        plt.sca(axs[num])
        _ = sns.distplot(all_features[col], kde=False)
        plt.ylabel('# of Tracks')



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



def plot_follower_count(filerange=range(201)):
    """Plot the distribution of followers from the evaluation sample of artists."""
    # Load the data
    results_list = load_sample_data(filerange)

    # Get the follower counts from the evaluation sample
    followers = []
    for res in results_list:
        followers.append(res[1][2])

    # Get the follower counts from the full 2000 random artist list for comparison
    fpath = 'Data/random_artists.pkl'
    with open(fpath, 'rb') as f:
        random_artists = pickle.load(f)
    all_followers = [x[2] for x in random_artists]

    # Plot the two distributions together (log-scale)
    _ = sns.distplot(np.log(np.array(all_followers) + 1), kde=True) # +1 in case of log(0)
    _ = sns.distplot(np.log(np.array(followers) + 1), kde=True) # +1 in case of log(0)
    plt.xlabel('# of Followers (log-scale)')
    plt.ylabel('# of Artists')



def plot_network_sizes(filerange=range(201)):
    """Plot the distribution of network sizes in the evaluation sample of artists."""
    # Load the data
    results_list = load_sample_data(filerange)
    all_nets = []
    for res in results_list:
        all_nets.append(len(res[2][1]))
    _ = sns.distplot(all_nets, kde=True)
    plt.xlabel('# of Artists in Network')
    plt.ylabel('# of Artists')



def plot_tracklist_sizes(filerange=range(201)):
    """Plot the distribution of seed artist tracklist sizes in the evaluation sample of artists."""
    # Load the data
    results_list = load_sample_data(filerange)
    all_tracklists = []
    for res in results_list:
        all_tracklists.append(len(res[2][2]))
    _ = sns.distplot(np.log(np.array(all_tracklists) + 1), kde=True) # +1 in case of log(0)
    plt.xlabel('# Tracks in Artist Library (log-scale)')
    plt.ylabel('# of Artists')



def plot_reclist_sizes(filerange=range(201)):
    """Plot the distribution of recommended tracklist sizes in the evaluation sample of artists."""
    # Load the data
    results_list = load_sample_data(filerange)
    all_recs = []
    for res in results_list:
        all_recs.append(len(res[2][4]))
    _ = sns.distplot(all_recs, kde=True)
    plt.xlabel('# of Tracks in Recommendation List')
    plt.ylabel('# of Artists')