import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd

"""
Reference:
https://machinelearningknowledge.ai/tutorial-how-to-use-spotipy-api-to-scrape-spotify-data/
"""
def main():
    # import credentials
    credentials_file = json.load(open('auth.json'))
    client_id = credentials_file['client_id']
    client_secret = credentials_file['client_secret']
    redirect_uri = credentials_file['redirect_uri']

    auth = SpotifyOAuth(client_id, client_secret,redirect_uri)

    # import playlist details
    playlist_file = json.load(open('10smetal.json'))
    playlist_id = playlist_file['playlist_id']

    # authenticate request
    spotify = spotipy.Spotify(client_credentials_manager=auth)

    # fetching
    results = spotify.playlist(playlist_id, 'tracks')

    # select details
    playlist_tracks_data = results['tracks']
    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    playlist_tracks_album_id = []
    playlist_tracks_album_title = []
    playlist_tracks_album_genres = []
    playlist_tracks_popularity = []

    for track in playlist_tracks_data['items']:
        playlist_tracks_id.append(track['track']['id'])
        playlist_tracks_titles.append(track['track']['name'])
        # adds a list of all artists involved in the song to the list of artists for the playlist
        artist_list = []
        for artist in track['track']['artists']:
            artist_list.append(artist['name'])
        playlist_tracks_artists.append(artist_list)
        first_artist_id = track['track']['artists'][0]['id']
        playlist_tracks_first_artists.append(artist_list[0])
        # get album info
        playlist_tracks_album_id.append(track['track']['album']['id'])
        playlist_tracks_album_title.append(track['track']['album']['name'])
        # get genre
        playlist_tracks_album_genres.append(spotify.artist(first_artist_id)['genres'])
        # get track popularity
        playlist_tracks_popularity.append(track['track']['popularity'])
    # get features
    features = spotify.audio_features(playlist_tracks_id)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())

    # combining df with title + artist information
    features_df['title'] = playlist_tracks_titles
    features_df['first_artist'] = playlist_tracks_first_artists
    features_df['all_artists'] = playlist_tracks_artists
    features_df['album_id'] = playlist_tracks_album_id
    features_df['album_name'] = playlist_tracks_album_title
    features_df['genres'] = playlist_tracks_album_genres
    features_df['popularity'] = playlist_tracks_popularity
    print(features_df)
    #features_df = features_df.set_index('id')
    features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                               'album_id', 'album_name', 'genres',
                               'danceability', 'energy', 'key', 'loudness',
                               'mode', 'acousticness', 'instrumentalness',
                               'liveness', 'valence', 'tempo',
                               'duration_ms', 'time_signature', 'popularity']]
    features_df.tail()

    # convert to csv
    features_df.to_csv("10smetal.csv", encoding='utf-8', index="false")

if __name__ == '__main__':
    main()

