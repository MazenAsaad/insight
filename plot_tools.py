"""Functions used for visualizing data."""


# Import libraries and functions
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns; sns.set()
from spotify_tools import *
from model_tools import *



def log10ticks(y, pos):
    """Scientific notation for tick marks via FuncFormatter()."""
    return r'$10^{:.0f}$'.format(y)



def rebin(data, binwidth):
    """Bin the data by binwidth."""
    binning = np.arange(min(data), max(data) + binwidth, binwidth)
    return data, binning



def plot_columns(input_df):
    """Plot distributions of all feature columns from a dataframe."""
    # Drop the irrelevant columns
    all_features = drop_cols(input_df)

    # Plot the distributions and format the plots
    fig, axs = plt.subplots(len(all_features.columns), figsize = (14,90))
    for num, col in enumerate(all_features.columns):
        plt.sca(axs[num])
        dist = sns.distplot(all_features[col], kde=False)
        plt.xlabel(col.replace('Track_', ''), fontsize=18)
        plt.xticks(fontsize=14)
        plt.ylabel('# of Tracks', fontsize=18)
        plt.yticks(fontsize=14)
    plt.show()



def plot_popularity(input_df):
    """Plot the distribution of track popularity."""
    # Plot the data and format the plot
    plt.figure(figsize=(14,6))
    dist = sns.distplot(input_df['Track_Popularity'], kde=False, bins=np.array(range(0,100,2)))
    plt.xlabel('Popularity Score', fontsize=18)
    plt.xlim(0, 100)
    plt.xticks(fontsize=14)
    plt.ylabel('# of Tracks', fontsize=18)
    plt.yticks(fontsize=14)
    plt.show()



def plot_correlations(input_df):
    """Plot the correlations of the dataframe features."""
    # Drop the irrelevant columns
    all_features = drop_cols(input_df)

    # Get the correlations and set the column names
    corr = all_features.corr()
    col_names = [x.replace('Track_', '') for x in all_features.columns]

    # Plot the correlation heatmap and format the plot
    plt.figure(figsize=(10,8))
    htmp = sns.heatmap(corr, cmap='RdBu_r', vmin=-1, vmax=1)
    htmp.set_xticklabels(col_names, fontsize=14)
    htmp.set_yticklabels(col_names, fontsize=14)
    htmp.collections[0].colorbar.ax.tick_params(labelsize=14)
    plt.show()



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

    # Set the bins for the histograms
    data_sample, binning = rebin(np.log10(np.array(all_followers) + 1), 0.25) # +1 in case of log(0)
    data_full, binning = rebin(np.log10(np.array(followers) + 1), 0.25) # +1 in case of log(0)

    # Plot the two distributions together and format the plot
    plt.figure(figsize=(6,6))
    dist = sns.distplot(data_sample, bins=binning, kde=True)
    dist = sns.distplot(data_full, bins=binning, kde=True)
    plt.xlabel('# of Followers', fontsize=18)
    plt.xticks(fontsize=14)
    dist.axes.xaxis.set_major_formatter(mtick.FuncFormatter(log10ticks))
    plt.ylabel('# of Artists', fontsize=18)
    plt.yticks(fontsize=14)
    plt.show()



def plot_network_sizes(filerange=range(201)):
    """Plot the distribution of network sizes in the evaluation sample of artists."""
    # Load the data
    results_list = load_sample_data(filerange)

    # Pull out the length of each network
    all_nets = []
    for res in results_list:
        all_nets.append(len(res[2][1]))
    
    # Set the bins for the histogram
    data, binning = rebin(all_nets, 25)

    # Plot the data and format the plot
    plt.figure(figsize=(6,6))
    dist = sns.distplot(data, bins=binning, kde=False)
    plt.xlabel('# of Artists in Network', fontsize=18)
    plt.xticks(fontsize=14)
    plt.ylabel('# of Artists', fontsize=18)
    plt.yticks(fontsize=14)
    plt.show()



def plot_tracklist_sizes(filerange=range(201)):
    """Plot the distribution of seed artist tracklist sizes in the evaluation sample of artists."""
    # Load the data
    results_list = load_sample_data(filerange)

    # Pull out the length of each track list
    all_tracklists = []
    for res in results_list:
        all_tracklists.append(len(res[2][2]))

    # Set the bins for the histogram
    data, binning = rebin(np.log10(np.array(all_tracklists) + 1), 0.25) # +1 in case of log(0)

    # Plot the data and format the plot
    plt.figure(figsize=(6,6))
    dist = sns.distplot(data, bins=binning, kde=False)
    plt.xlabel('# of Tracks in Artist Library', fontsize=18)
    plt.xticks(fontsize=14)
    dist.axes.xaxis.set_major_formatter(mtick.FuncFormatter(log10ticks))
    plt.ylabel('# of Artists', fontsize=18)
    plt.yticks(fontsize=14)
    plt.show()



def plot_reclist_sizes(filerange=range(201)):
    """Plot the distribution of recommended tracklist sizes in the evaluation sample of artists."""
    # Load the data
    results_list = load_sample_data(filerange)

    # Pull out the length of each recommendation list
    all_recs = []
    for res in results_list:
        all_recs.append(len(res[2][4]))

    # Set the bins for the histogram
    data, binning = rebin(all_recs, 1000)

    # Plot the data and format the plot
    plt.figure(figsize=(6,6))
    dist = sns.distplot(data, bins=binning, kde=False)
    plt.xlabel('# of Tracks in Recommendation List', fontsize=18)
    plt.xticks(fontsize=14)
    plt.ylabel('# of Artists', fontsize=18)
    plt.yticks(fontsize=14)
    plt.show()