import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

config = dotenv_values(".env")
client_id = config.get('CLIENT_ID')
client_secret = config.get('CLIENT_SECRET')

date = input("Please the date you would to travel YYYY-MM-DD")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
billboard_web_page = response.text
soup = BeautifulSoup(billboard_web_page, "html.parser")

all_songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
songs_titles = [song.getText() for song in all_songs]

all_artists = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
songs_artist = [song.getText() for song in all_artists]

songs_track = {songs_titles[i]: songs_artist[i] for i in range(len(songs_titles))}

print(songs_track)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                              client_secret=client_secret,
                                              redirect_uri="http://example.com",
                                              scope="playlist-modify-private",
                                              show_dialog=True,
                                              cache_path=".cache")
                    )
sp_list = []
for songs in songs_track:
   try:
       results = sp.search(q=f"track:{songs} artist:{songs_track[songs]}", type='track', limit=1)
       sp_list.append(results['tracks']['items'][0]['uri'])
   except IndexError:
       print("Track not found")

playlist = sp.user_playlist_create(sp.current_user()["id"], f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=sp_list)
