"""Codebase for the streamlit front-end dashboard."""


# Import relevant libraries (many imports contained within other scripts)
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






# Activate the rest of the dashboard when an artist is selected
if input_artist:
    # # Load the data from the input artist
    # X_train, y_train, X_test, y_test, artist_library_df = prep_data_streamlit(input_artist)

    # Load the sample data for debugging
    with open('Testing/streamlit_sample_data.pkl', 'rb') as f:
        X_train, y_train, X_test, y_test, artist_library_df = pickle.load(f)



    # Set up and fit the model
    RFC = RandomForestClassifier(class_weight='balanced_subsample', n_estimators=100, max_depth=2, random_state=0)
    clf, cols2scale, cols2drop = build_pipeline(RFC)
    clf.fit(X_train, y_train)



    # SUGGEST SONGS TO PROMOTE
    # Calculate y_pred
    y_pred = clf.predict(X_test)
    # Generate and display suggested songs to promote
    song_suggestions = songs_to_promote(artist_library_df, y_test, y_pred)
    st.table(song_suggestions)



    # RETURN IMPORTANT FEATURES DRIVING POPULARITY
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



    # # Generate and display suggested artist collaborations
    # collab_suggestions = suggested_collabs(input_artist)
    # st.dataframe(collab_suggestions)





# Run the analyses & display the results
# if input_artist:
#   st.subheader('Recommended Collaborations:')
#   related = related_artists_network(input_artist, 2)
#   if related:
#       related_df = artist_df(related)
#       related_names = related_df['Artist_Name']
#       st.dataframe(related_names)
#   else:
#       st.markdown(':crying_cat_face: ***None found (artist library likely too small)*** :crying_cat_face:')

#   st.subheader('Songs underperforming expectations:')
#   tracklist = artist_tracklist(input_artist)
#   tracks = [x[0] for x in tracklist]
#   st.dataframe(tracks)

#   st.subheader('Key song features driving popularity:')
#   importance = [5, 10, 7, 13, 11, 6, 5, 8, 2, 5, 9, 10, 11, 10]
#   st.bar_chart(importance)