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
    return x

# Given a playlist id, put relevant info into a dataframe
def playlist_df(playlist_id):
    # Set credentials and get playlist
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    pl = sp.playlist(playlist_id)
    
    # Pull out the relevant playlist information
    track_num = []
    track_id = []
    for num, data in enumerate(pl['tracks']['items']):
        track_num.append(num+1)
        track_id.append(data['track']['id'])
    
    # Put it into a dataframe
    pl_df = pd.DataFrame({
        'Track_Position':track_num,
        'Track_ID':track_id
    })
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
    
    art_df_list = []
    for art in arts['artists']:
        # Pull out the relevant artist information
        art_dict = {'Artist_Name':art['name'],
                    'Artist_ID':art['id'],
                    'Artist_Genres':df_listcell(art['genres'])[0],
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
    
    alb_df_list = []
    for alb in albs['albums']:
        # Pull out the relevant album information
        alb_dict = {'Album_Name':alb['name'],
                    'Album_ID':alb['id'],
                    'Album_Type':alb['album_type'],
                    'Album_Artists':df_listcell([x['id'] for x in alb['artists']])[0],
                    'Album_Genres':df_listcell(alb['genres'])[0],
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
    
    trk_df_list = []
    for trk in trks['tracks']:
        # Pull out the relevant track information
        trk_dict = {'Track_Name':trk['name'],
                    'Track_ID':trk['id'],
                    'Track_Artists':df_listcell([x['id'] for x in trk['artists']])[0],
                    'Track_Album':trk['album']['id'],
                    'Track_Popularity':trk['popularity'],
                    'Track_Explicitness':int(trk['explicit'] == True),
                    'Track_Duration':trk['duration_ms']}
        trk_df_list.append(trk_dict)
    
    trk_feat_df_list = []
    for trk_feat in trks_feat:
        # Pull out the relevant track feature information
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