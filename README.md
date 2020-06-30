# Music Mastery
___Empowering Artists to Find Their Niche___

The project was completed as part of the Insight Data Science Fellowship program (Summer 2020, New York, NY).

By Mazen Asaad, PhD

# Table of Contents
1. [Introduction](README.md#introduction)
2. [Approach](README.md#approach)
3. [Requirements](README.md#requirements)
4. [Repository Contents](README.md#repository-contents)
5. [Installation](README.md#installation)

# Introduction
The goal of this project is to provide a machine learning model and analytic dashboard to enable aspiring musicians to determine which audio features of songs drive popularity within their market segment, as well as to identify which songs in their library are underperforming expectations and should be the focus of future promotional resources.

# Approach
Artist, album, and track information, as well as audio features for each track, were taken from the Spotify API (https://developer.spotify.com/console). These features were processed and engineered to build a machine learning model predicting track popularity for different market segments. The information from this model and other analyses were then displayed as a dashboard via Streamlit. The final product was deployed on Amazon Web Services (AWS) for remote hosting.

# Requirements
The following languages and packages were used in this project:
* python 3.8.3
* numpy 1.18.1
* pandas 1.0.3
* matplotlib 3.1.3
* seaborn 0.10.1
* scikit-learn 0.22.1
* spotipy 2.12.0 (for interfacing with the Spotify API)
* streamlit 0.61.0 (for building a front-end dashboard)

As this project leverages data from Spotify, a client id and client secret are required as provided by the Spotify developer API (https://developer.spotify.com/dashboard). These details should be stored in a file called `spotify_credentials.py` in the same directory as `spotify_tools.py`. It should only contain the values for these two variables, as such:
```
client_id = 'YourClientIDStringGoesHere'
client_secret = 'YourClientSecretStringGoesHere'
```

# Repository Contents
* __Data/__ - Contains sample data pulled from the Spotify API used for model testing and validation at the time of this project's creation. Data pulled from the API at a future date may not exactly match the results shown here.
* __spotify_tools.py__ - Contains all of the relevant functions for pulling data from the Spotify API (via the spotipy package).
* __model_tools.py__ - Contains all of the relevant functions for generating and testing the machine learning models.
* __plot_tools.py__ - Contains all of the relevant functions for generating important visualizations.
* __save_cv_results.py__ - A script used for generating cross-validation results to compare model performance on sample data.
* __streamlit_app.py__ - The main script for running the dashboard via Streamlit.

# Installation
(Installation instructions and examples to come...)