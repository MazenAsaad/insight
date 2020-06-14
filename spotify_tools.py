# Set up Spotipy (Spotify API package)
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_credentials import *
os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret



# Helper function to store lists in dataframes
def df_listcell(input_list):
    x = pd.Series([],dtype='object')
    x[0] = input_list
    return x[0]



# Yield successive n-sized chunks from a list
def chunks(inputlist, n):
    for i in range(0, len(inputlist), n):
        yield inputlist[i:i + n]



# Given a playlist id, put relevant info into a dataframe
def playlist_df(playlist_id):
    # Set credentials and get playlist
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    pl = sp.playlist(playlist_id)
    
    # Pull out the relevant playlist information
    track_obj = pl['tracks']
    track_id = []
    for trk in track_obj['items']:
        track_id.append(trk['track']['id'])
    
    # Go through the pagination for the rest of the data
    while track_obj['next']:
        track_obj = sp.next(track_obj)
        for trk in track_obj['items']:
            track_id.append(trk['track']['id'])
    
    # Put it into a dataframe
    pl_df = pd.DataFrame({'Track_ID':track_id})
    pl_df['Track_Position'] = pl_df.index + 1
    return pl_df



# Given a list of artist ids (limit 50), put relevant info into a dataframe
def artist_df(artist_id_list):
    # Check if the input is an individual string and not a list
    if isinstance(artist_id_list,str):
        artist_id_list = [artist_id_list]
    # Check the input list length
    if len(artist_id_list) > 50:
        raise ValueError('Input list must not exceed 50 artists')
        
    # Set credentials and get artists
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    arts = sp.artists(artist_id_list)
    
    # Pull out the relevant artist information
    art_df_list = []
    for art in arts['artists']:
        art_dict = {'Artist_Name':art['name'],
                    'Artist_ID':art['id'],
                    'Artist_Genres':df_listcell(art['genres']),
                    'Artist_Followers':art['followers']['total'],
                    'Artist_Popularity':art['popularity']}
        art_df_list.append(art_dict)
    
    # Put it into a dataframe
    art_df = pd.DataFrame(art_df_list)
    return art_df



# Given a list of album ids (limit 20), put relevant info into a dataframe
def album_df(album_id_list):
    # Check if the input is an individual string and not a list
    if isinstance(album_id_list,str):
        album_id_list = [album_id_list]
    # Check the input list length
    if len(album_id_list) > 20:
        raise ValueError('Input list must not exceed 20 albums')
    
    # Set credentials and get albums
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    albs = sp.albums(album_id_list)
    
    # Pull out the relevant album information
    alb_df_list = []
    for alb in albs['albums']:
        alb_dict = {'Album_Name':alb['name'],
                    'Album_ID':alb['id'],
                    'Album_Type':alb['album_type'],
                    'Album_Artists':df_listcell([x['id'] for x in alb['artists']]),
                    'Album_Genres':df_listcell(alb['genres']),
                    'Album_Popularity':alb['popularity'],
                    'Album_Label':alb['label'],
                    'Album_Release_Date':alb['release_date']}
        alb_df_list.append(alb_dict)
    
    # Put it into a dataframe
    alb_df = pd.DataFrame(alb_df_list)
    return alb_df



# Given a list of track ids (limit 50), put relevant info into a dataframe (including audio features)
def track_df(track_id_list):
    # Check if the input is an individual string and not a list
    if isinstance(track_id_list,str):
        track_id_list = [track_id_list]
    # Check the input list length
    if len(track_id_list) > 50:
        raise ValueError('Input list must not exceed 50 tracks')
        
    # Set credentials and get tracks
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    trks = sp.tracks(track_id_list)
    trks_feat = sp.audio_features(track_id_list)

    # Pull out the relevant track information    
    trk_df_list = []
    for trk in trks['tracks']:
        trk_dict = {'Track_Name':trk['name'],
                    'Track_ID':trk['id'],
                    'Track_Artists':df_listcell([x['id'] for x in trk['artists']]),
                    'Track_Album':trk['album']['id'],
                    'Track_Popularity':trk['popularity'],
                    'Track_Explicitness':int(trk['explicit'] == True),
                    'Track_Duration':trk['duration_ms']}
        trk_df_list.append(trk_dict)
    
    # Pull out the relevant track feature information
    trk_feat_df_list = []
    for trk_feat in trks_feat:
        trk_feat_dict = {'Track_Key':trk_feat['key'],
                         'Track_Mode':trk_feat['mode'],
                         'Track_TimeSig':trk_feat['time_signature'],
                         'Track_Acousticness':trk_feat['acousticness'],
                         'Track_Danceability':trk_feat['danceability'],
                         'Track_Energy':trk_feat['energy'],
                         'Track_Instrumentalness':trk_feat['instrumentalness'],
                         'Track_Liveness':trk_feat['liveness'],
                         'Track_Loudness':trk_feat['loudness'],
                         'Track_Speechiness':trk_feat['speechiness'],
                         'Track_Valence':trk_feat['valence'],
                         'Track_Tempo':trk_feat['tempo']}
        trk_feat_df_list.append(trk_feat_dict)    

    # Put it into a dataframe
    trk_df = pd.DataFrame(trk_df_list).join(pd.DataFrame(trk_feat_df_list))
    return trk_df



# Given a list of track ids (unlimited), put relevant info into a dataframe (including audio features)
def track_df_unlimited(track_id_list):
    # Check if the input is an individual string and not a list
    if isinstance(track_id_list,str):
        track_id_list = [track_id_list]
        
    # Set credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    trk_df_list = []
    trk_feat_df_list = []
    
    # Break the list into chunks of 50 and iterate over them
    chunked = list(chunks(track_id_list,50))
    for chunk in chunked:
        trks = sp.tracks(chunk)
        trks_feat = sp.audio_features(chunk)

        # Pull out the relevant track information    
        for trk in trks['tracks']:
            trk_dict = {'Track_Name':trk['name'],
                        'Track_ID':trk['id'],
                        'Track_Artists':df_listcell([x['id'] for x in trk['artists']]),
                        'Track_Album':trk['album']['id'],
                        'Track_Popularity':trk['popularity'],
                        'Track_Explicitness':int(trk['explicit'] == True),
                        'Track_Duration':trk['duration_ms']}
            trk_df_list.append(trk_dict)

        # Pull out the relevant track feature information
        for trk_feat in trks_feat:
            if trk_feat is None:
                trk_feat_dict = {'Track_Key':None,
                                 'Track_Mode':None,
                                 'Track_TimeSig':None,
                                 'Track_Acousticness':None,
                                 'Track_Danceability':None,
                                 'Track_Energy':None,
                                 'Track_Instrumentalness':None,
                                 'Track_Liveness':None,
                                 'Track_Loudness':None,
                                 'Track_Speechiness':None,
                                 'Track_Valence':None,
                                 'Track_Tempo':None}
            else:
                trk_feat_dict = {'Track_Key':trk_feat['key'],
                                 'Track_Mode':trk_feat['mode'],
                                 'Track_TimeSig':trk_feat['time_signature'],
                                 'Track_Acousticness':trk_feat['acousticness'],
                                 'Track_Danceability':trk_feat['danceability'],
                                 'Track_Energy':trk_feat['energy'],
                                 'Track_Instrumentalness':trk_feat['instrumentalness'],
                                 'Track_Liveness':trk_feat['liveness'],
                                 'Track_Loudness':trk_feat['loudness'],
                                 'Track_Speechiness':trk_feat['speechiness'],
                                 'Track_Valence':trk_feat['valence'],
                                 'Track_Tempo':trk_feat['tempo']}
            trk_feat_df_list.append(trk_feat_dict)

    # Put it into a dataframe
    trk_df = pd.DataFrame(trk_df_list).join(pd.DataFrame(trk_feat_df_list))
    # Drop rows without audio feature data
    trk_df = trk_df[trk_df['Track_Key'].notna()].reset_index(drop=True)
    return trk_df



# Given an artist id, return the id of all albums as a list
def artist_albumlist(artist_id):
    # Set credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    
    # Loop through album types and get info from API
    alb_types = ['album','single','compilation'] # exclude 'appears_on'
    results = []
    for typ in alb_types:
        art = sp.artist_albums(artist_id, album_type=typ, limit=50)
    
        # Put data into a list and go through pagination
        results.extend([x['id'] for x in art['items']])
        while art['next']:
            art = sp.next(art)
            results.extend([x['id'] for x in art['items']])
    return results



# Given an album id, return the id of all tracks as a list
def album_tracklist(album_id):
    # Set credentials and get info from API
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    alb = sp.album_tracks(album_id, limit=50)
    
    # Put data into a list and go through pagination
    results = [x['id'] for x in alb['items']]
    while alb['next']:
        alb = sp.next(alb)
        results.extend([x['id'] for x in alb['items']])
    return results



# Given an artist id, return the id of all tracks as a list
def artist_tracklist(artist_id):
    # NB: It's much faster to only call spotipy.Spotify() once
    # rather than chaining artist_albumlist() & album_tracklist()
    
    # Set credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # Loop through album types and get artist's albums from API
    alb_types = ['album','single','compilation'] # exclude 'appears_on'
    albumlist = []
    for typ in alb_types:
        art = sp.artist_albums(artist_id, album_type=typ, limit=50)
    
        # Put data into a list and go through pagination
        albumlist.extend([x['id'] for x in art['items']])
        while art['next']:
            art = sp.next(art)
            albumlist.extend([x['id'] for x in art['items']])    
    
    # Pull the tracks for each album one-by-one
    tracklist = []
    for album in albumlist:
        # Get album tracks from API
        alb = sp.album_tracks(album, limit=50)
        
        # Put data into a list and go through pagination
        tracklist.extend([(x['name'],x['id']) for x in alb['items']])
        while alb['next']:
            alb = sp.next(alb)
            tracklist.extend([(x['name'],x['id']) for x in alb['items']])
    return tracklist



# Given an artist id, return the id of all 20 related artists in a list
def related_artists(artist_id):
    # Set credentials and return related artists
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    arts = sp.artist_related_artists(artist_id)
    related = [(x['name'],x['id']) for x in arts['artists']]
    return related



# Find artist or album name & id from a search query
def search_spotify(query, fieldtype='artist'):
    # Set credentials and run the query
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = sp.search(q=query, type=fieldtype)
    
    # Return the name and id results as a tuple
    return [(x['name'],x['id'],x['images']) for x in results[fieldtype+'s']['items']]



# Get a list of similar tracks based on a seed artist and their similar artists distributed across popularity scores
def track_recs(artist_id, degrees=0, pop_list=range(5,100,15)):
    # Check if the input is an individual string and not a list
    if isinstance(artist_id,str):
        artist_id = [artist_id]
    
    # Set credentials
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    
    # Generate the list of artists to iterate over
    unchecked = artist_id
    checked = []
    artist_list = []
    while degrees > 0:
        for art in unchecked:
            related_artists = sp.artist_related_artists(art)
            related_ids = [x['id'] for x in related_artists['artists']]
            checked.append(art)
            artist_list.extend(related_ids)
        unchecked = list(set(artist_list).difference(checked))
        degrees -= 1
    artist_list = list(set(checked).union(unchecked))
    
    # Generate a list of similar tracks for each artist, balanced by popularity score
    tracklist = []
    for art in artist_list:
        for pop in pop_list:
            recs = sp.recommendations(seed_artists=[art], limit=100, target_popularity=pop)
            tracklist.extend([x['id'] for x in recs['tracks']])

    # Remove duplicate tracks and return the list
    tracklist = list(set(tracklist))
    return tracklist