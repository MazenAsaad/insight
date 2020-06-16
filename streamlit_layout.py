# Import relevant libraries
import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from spotify_tools import *


# Set the title
st.title('Spotify Artist Analysis')
input_artist = None

# Add search functionality to the sidebar
search_box = st.sidebar.text_input('Search for artists')
if search_box:
	st.sidebar.header('Choose from below:')
	search_results = search_spotify(search_box)
	for n,res in enumerate(search_results):
		if st.sidebar.button(res[0], key='search{}'.format(n)):
			st.header('Selected Artist: {}'.format(res[0]))
			input_artist = res[1]
		if res[2]:
			st.sidebar.image(res[2][2]['url'])
		else:
			st.sidebar.markdown(':crying_cat_face: *No image found* :crying_cat_face:')
		st.sidebar.markdown('\n')
		st.sidebar.markdown('\n')



# Run the analyses & display the results
if input_artist:
	st.subheader('Recommended Collaborations:')
	related = related_artists_network(input_artist, 2)
	if related:
		related_df = artist_df(related)
		related_names = related_df['Artist_Name']
		st.dataframe(related_names)
	else:
		st.markdown(':crying_cat_face: ***None found (artist library likely too small)*** :crying_cat_face:')


	# input_artist_recs = track_recs(input_artist, degrees=1)
	# input_df = track_df_unlimited(input_artist_recs)
	# x = input_df.drop(['Track_Name','Track_ID','Track_Artists','Track_Album','Track_Popularity'], axis=1)
	# y = input_df['Track_Popularity']
	# artisttracks = artist_tracklist(input_artist)
	# artisttracklist_df = track_df_unlimited(artisttracks)
	# x_test = artisttracklist_df.drop(['Track_Name','Track_ID','Track_Artists','Track_Album','Track_Popularity'], axis=1)
	# y_test = artisttracklist_df['Track_Popularity']
	# from sklearn.ensemble import RandomForestRegressor 
	# regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
	# regressor.fit(x, y)
	# importance = regressor.feature_importances_

	importance = [5,10,7,13,11,6,5,8,2,5,9,10,11,10]


	st.subheader('Songs underperforming expectations:')
	tracklist = artist_tracklist(input_artist)
	tracks = [x[0] for x in tracklist]
	st.dataframe(tracks)


	st.subheader('Key song features driving popularity:')
	# for i,v in enumerate(importance):
		# st.text('Feature: %0d (%s), Score: %.5f' % (i,x.columns[i],v))
	st.bar_chart(importance)

