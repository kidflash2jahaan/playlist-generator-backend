import spotipy, requests
from flask import Flask, request
from dotenv import dotenv_values
from prompt import get_playlist
from song_finder import find_song

config = dotenv_values(".env")
app = Flask(__name__)

sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id=config["SPOTIFY_CLIENT_ID"],
        client_secret=config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:9999",
        scope="playlist-modify-private",
    )
)

current_user = None


@app.route("/playlist")
def create_playlist():
    current_user = sp.current_user()
    assert current_user is not None

    prompt = request.args.get("prompt")
    count = int(request.args.get("count")) if request.args.get("count") else 8
    playlist = get_playlist(prompt, int(count) if count else 8)
    track_ids = []

    for item in playlist["playlist"]:
        artist, song = item["artist"], item["song"]
        query = f"{song} {artist}"
        track_ids.append(find_song(query))

    created_playlist = sp.user_playlist_create(
        current_user["id"],
        public=False,
        name=f"{prompt} - by spotify-gen",
    )

    sp.user_playlist_add_tracks(current_user["id"], created_playlist["id"], track_ids)

    return {"status": "success"}


if __name__ == "__main__":
    app.run(debug=True)
