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

# Given an artist id, put relevant info into a dataframe
def artist_df(artist_id):
    # Set credentials and get artist
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    art = sp.artist(artist_id)
    
    # Pull out the relevant artist information
    art_name = art['name']
    art_id = art['id']
    art_genres = art['genres']
    art_pop = art['popularity']
    
    # Put it into a dataframe
    art_df = pd.DataFrame({
        'Artist_Name':art_name,
        'Artist_ID':art_id,
        'Artist_Genres':df_listcell(art['genres']),
        'Artist_Popularity':art_pop
    })
    return art_df

# Given an album id, put relevant info into a dataframe
def album_df(album_id):
    # Set credentials and get album
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    alb = sp.album(album_id)
    
    # Pull out the relevant album information
    alb_name = alb['name']
    alb_id = alb['id']
    alb_type = alb['album_type']
    alb_artists = [x['id'] for x in alb['artists']]
    alb_genres = alb['genres']
    alb_pop = alb['popularity']
    alb_label = alb['label']
    alb_date = alb['release_date']

    # Put it into a dataframe
    alb_df = pd.DataFrame({
        'Album_Name':alb_name,
        'Album_ID':alb_id,
        'Album_Type':alb_type,
        'Album_Artists':df_listcell(alb_artists),
        'Album_Genres':df_listcell(alb_genres),
        'Album_Popularity':alb_pop,
        'Album_Label':alb_label,
        'Album_Release_Date':alb_date
    })
    return alb_df

# Given a track id, put relevant info into a dataframe (including audio features)
def track_df(track_id):
    # Set credentials and get track
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    trk = sp.track(track_id)
    trk_feat = sp.audio_features(track_id)[0]
    
    # Pull out the relevant track information
    track_name = trk['name']
    track_id = trk['id']
    track_artists = [x['id'] for x in trk['artists']]
    track_album = trk['album']['id']
    track_pop = trk['popularity']
    track_explicit = trk['explicit']
    track_duration = trk['duration_ms']
    track_key = trk_feat['key']
    track_mode = trk_feat['mode']
    track_timesig = trk_feat['time_signature']
    track_acousticness = trk_feat['acousticness']
    track_danceability = trk_feat['danceability']
    track_energy = trk_feat['energy']
    track_instrumentalness = trk_feat['instrumentalness']
    track_liveness = trk_feat['liveness']
    track_loudness = trk_feat['loudness']
    track_speechiness = trk_feat['speechiness']
    track_valence = trk_feat['valence']
    track_tempo = trk_feat['tempo']

    # Put it into a dataframe
    trk_df = pd.DataFrame({
        'Track_Name':track_name,
        'Track_ID':track_id,
        'Track_Artists':df_listcell(track_artists),
        'Track_Album':track_album,
        'Track_Popularity':track_pop,
        'Track_Explicitness':track_explicit,
        'Track_Duration':track_duration,
        'Track_Key':track_key,
        'Track_Mode':track_mode,
        'Track_TimeSig':track_timesig,
        'Track_Acousticness':track_acousticness,
        'Track_Danceability':track_danceability,
        'Track_Energy':track_energy,
        'Track_Instrumentalness':track_instrumentalness,
        'Track_Liveness':track_liveness,
        'Track_Loudness':track_loudness,
        'Track_Speechiness':track_speechiness,
        'Track_Valence':track_valence,
        'Track_Tempo':track_tempo
    })
    return trk_df