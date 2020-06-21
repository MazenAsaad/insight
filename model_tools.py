# Import libraries and functions
import os
import pickle
import numpy as np
import pandas as pd
from spotify_tools import *



# Turn popularity scores into classes based on percentile cutoffs
def pop_classes(pop_vals, cutoffs=[75]):
    # Check if the cutoffs is a single integer and not a list
    if isinstance(cutoffs,int):
        cutoffs = [cutoffs]
    
    # Convert popularity values to a numpy array (for speed)
    p = np.array(pop_vals)
    
    # Set each percentile chunk to a different class (in ranked order)
    classes = np.array([0]*len(p))
    for pct in cutoffs:
        c = np.where(p >= np.percentile(p,pct),1,0)
        classes = classes + c
    return classes



# Pull the relevant data for a seed artist
def seed_data(artist_id, degrees=2):
    # Get the network of related artists
    net = related_artists_network(artist_id, degrees)
    
    # Get the seed artist's tracklist
    seed_list = artist_tracklist(artist_id)
    seed_list = [x[1] for x in seed_list]
    
    # Get the list of recommended tracks and remove any belonging to the seed artist
    recs = recommended_tracks(net)
    recs_filt = list(set(recs).difference(seed_list))
    
    # Get the full dataframe for each track id in the recommendation list
    # Handle error in case the artist is so small there weren't any recommended artists
    if recs_filt:
    	df = track_df(recs_filt)
    else:
    	df = None
    return (artist_id,net,seed_list,recs,recs_filt,df)


# Go through the random_artists seed list and generate/save the data needed for modeling tests
def save_random_artist_data(start_idx=0, end_idx=3):
    # Load the random_artists list, or create & save it if it doesn't exist
    if os.path.exists('Data/random_artists.pkl'):
        print('Load: random_artists')
        with open('Data/random_artists.pkl', 'rb') as f:
            random_artists = pickle.load(f)
    else:
        random_artists = get_random_artists()
        with open('Data/random_artists.pkl', 'wb') as f:
            pickle.dump(random_artists, f)
        print('Saved: random_artists')

    # Get the seed_data for each artist and save it
    for n, artist in enumerate(random_artists[start_idx:end_idx]):
        save_name = 'data_artist_{}.pkl'.format(n+start_idx)
        save_path = 'Data/{}'.format(save_name)

        # Skip this file if it already exists
        if os.path.exists(save_path):
        	print('Skipped: ', save_name)
        	continue

        # Create and save the data
        save_data = seed_data(artist[1])
        with open(save_path, 'wb') as f:
            pickle.dump([save_name,artist,save_data], f)
        print('Saved: ', save_name)