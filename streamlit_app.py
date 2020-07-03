"""Codebase for the streamlit front-end dashboard."""


# Import relevant libraries (many imports already contained within other scripts)
import streamlit as st
from spotify_tools import *
from model_tools import *
from plot_tools import *



# Set the title
st.title('Music Mastery')
st.markdown('**by Mazen Asaad**')

# Add search functionality to the sidebar
input_artist = None
search_box = st.sidebar.text_input('Search for artists')
if search_box:
    st.sidebar.header('Choose from below:')

    # Pull possible results to choose from
    search_results = search_spotify(search_box)
    for n, res in enumerate(search_results):
        if st.sidebar.button(res[0], key='search{}'.format(n)):
            st.header('Selected Artist: {}'.format(res[0]))
            input_artist = res[1]
        if res[2]:
            st.sidebar.image(res[2][2]['url'], caption=res[0], width=160)
        else:
            st.sidebar.markdown(':crying_cat_face: *No image found* :crying_cat_face:')
        st.sidebar.markdown('\n')
        st.sidebar.markdown('\n')

# Establish a default error message in case of network disconnects
error_msg = 'An error occurred. Please check your internet connection and try again.'




# input_artist = '6ImfL6wSxqhYl64AbsaNZX'
debugmode = 1

instructions = st.markdown('Here are instructions. Here are instructions. Here are instructions. Here are instructions. Here are instructions. Here are instructions. Here are instructions. Here are instructions.')
promote_header = st.subheader('Songs to Promote')
promote_text = st.markdown('Summary of how to intepret the results')
feature_header = st.subheader('Audio Features Driving Popularity')
feature_text = st.markdown('Summary of how to intepret the results')
collab_header = st.subheader('Possible Collaborations')
collab_text = st.markdown('Summary of how to intepret the results')


# Activate the rest of the dashboard when an artist is selected
if input_artist:
    try:
        # Load the data from the input artist
        loading_msg = st.warning('Loading & processing data. This may take a few minutes...')


        if debugmode == 1:
            import time
            time.sleep(3)
            with open('Testing/streamlit_sample_data.pkl', 'rb') as f:
                X_train, y_train, X_test, y_test, artist_library_df = pickle.load(f)
        else:
            seed_results = seed_data(input_artist)
            reclist_df = seed_results[5]
            if not reclist_df:
                error_msg = 'Error: Artist library too small, no related artists found.'
            artist_library_df = track_df(seed_results[2])
            X_train, y_train, X_test, y_test = prep_data_streamlit(artist_library_df, reclist_df)
        


        loading_msg.text('')


        # Set up and fit the model
        RFC = RandomForestClassifier(class_weight='balanced_subsample', n_estimators=100, max_depth=2, random_state=0)
        clf, cols2scale, cols2drop = build_pipeline(RFC)
        clf.fit(X_train, y_train)
        # Calculate y_pred
        y_pred = clf.predict(X_test)
        # Generate and display suggested songs to promote
        song_suggestions = songs_to_promote(artist_library_df, y_test, y_pred)
        num_songs = song_suggestions.shape[0]
        song_suggestions = song_suggestions.set_index(song_suggestions.index + 1)
        st.dataframe(song_suggestions)


        # Pull out the model components
        col_trans = clf['preprocess']
        forest = clf['model']
        # Generate the feature names
        new_cols = [c for c in X_train.columns if c not in cols2scale+cols2drop]
        new_cols = cols2scale + new_cols
        col_labels = [x.replace('Track_', '') for x in new_cols]
        # Preprocess X_train for calculating feature importance
        X_trans = col_trans.fit_transform(X_train)
        X_trans = pd.DataFrame({k:X_trans[:,n] for n, k in enumerate(col_labels)})
        # Calculate and plot the Random Forest feature importances
        sorted_mean, sorted_std, sorted_labels, sorted_colors = get_RFC_importances(forest, X_trans, y_train, col_labels)
        importances = plot_RFC_importances(sorted_mean, sorted_std, sorted_labels, sorted_colors, True)
        st.pyplot()
        st.table(importances)




        loading_msg = st.warning('Loading & processing data. This may take a few minutes...')
        if debugmode == 1:
            time.sleep(5)
            with open('Testing/streamlit_sample_collabs.pkl', 'rb') as f:
                collab_suggestions = pickle.load(f)
        else:
            collab_suggestions = suggested_collabs(input_artist)


        loading_msg.text('')
        st.dataframe(collab_suggestions)


    except:
        loading_msg.text('')
        st.error(error_msg)