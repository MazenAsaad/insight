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

	# Pull possible results to choose from
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
# NB: This currently uses dummy values until the backend is connected to the front-end
if input_artist:
	st.subheader('Recommended Collaborations:')
	related = related_artists_network(input_artist, 2)
	if related:
		related_df = artist_df(related)
		related_names = related_df['Artist_Name']
		st.dataframe(related_names)
	else:
		st.markdown(':crying_cat_face: ***None found (artist library likely too small)*** :crying_cat_face:')

	st.subheader('Songs underperforming expectations:')
	tracklist = artist_tracklist(input_artist)
	tracks = [x[0] for x in tracklist]
	st.dataframe(tracks)

	st.subheader('Key song features driving popularity:')
	importance = [5, 10, 7, 13, 11, 6, 5, 8, 2, 5, 9, 10, 11, 10]
	st.bar_chart(importance)