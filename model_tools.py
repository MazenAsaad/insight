# Import libraries and functions
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
    df = track_df(recs_filt)
    return (artist_id,net,seed_list,recs,recs_filt,df)