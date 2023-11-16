import spotipy
from dotenv import dotenv_values

config = dotenv_values(".env")

sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id=config["SPOTIFY_CLIENT_ID"],
        client_secret=config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:9999",
    )
)

def find_song(song):
    search_results = sp.search(q=song, type="track", limit=1)
    return search_results["tracks"]["items"][0]["id"]