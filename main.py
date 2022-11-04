import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from tqdm import tqdm
import os
from dotenv import load_dotenv
from spotipy_utils import create_playlist, get_results_by_terms, add_to_playlist_by_ids

load_dotenv()

cid = os.getenv("CLIENT_ID")
secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
user = os.getenv("USER_ID")
scope = "playlist-modify-private"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
auth_manager = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=auth_manager, requests_timeout=10, retries=10)

with open("animals.txt", "r") as f:
    data = f.read()

animals = data.split(",")

animal_ids = get_results_by_terms(animals[::2], popularity=70, sp=sp, retrive_n=250)
animal_playlist = create_playlist("Animals", user=user, sp=sp)
add_to_playlist_by_ids(animal_ids, animal_playlist["id"], sp=sp, user=user)
