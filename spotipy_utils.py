import spotipy
from tqdm import tqdm

def find_popular_by_query(query: str, sp: spotipy.Spotify, popularity: int = 70, retrieve_n: int = 500):
    results = {}
    for i in tqdm(range(0, retrieve_n, 50), leave=False):
        track_results = sp.search(q=f"track:{query}", type="track", limit=50, offset=i, market="NO")    
        for t in track_results['tracks']['items']:
            if(t["popularity"] > popularity):
                results[t["id"]] = {
                    "name": t["name"], 
                    "artist": t["artists"][0]["name"], 
                    "popularity": t["popularity"]
                    }
    return results


def create_playlist(name: str, user: str, sp: spotipy.Spotify):    
    playlist = sp.user_playlist_create(
        user, 
        name, 
        public=False, 
        collaborative=False, 
        description=f'A playlist containing songs related to {name.lower()}'
        )
    return playlist


def get_tracks_from_playlist(user: str, playlist_id: str, sp: spotipy.Spotify, max_len: int = 10000):
    track_ids = []
    total_tracks_in_playlist = []
    for i in range(0, max_len, 100):
        tracks_in_playlist = sp.user_playlist_tracks(user=user, playlist_id=playlist_id, limit=100, offset=i)
        total_tracks_in_playlist.append(tracks_in_playlist)
    for tracks_in_playlist in total_tracks_in_playlist:
        for track in tracks_in_playlist["items"]:
            track_ids.append(track["track"]["id"])
    return track_ids


def get_results_by_terms(queries: list[str], sp: spotipy.Spotify, popularity: int = 75, retrive_n: int = 500):
    total_result = []
    for query in tqdm(queries):
        result = find_popular_by_query(query=query.lower(), popularity=popularity, sp=sp, retrieve_n=retrive_n)
        total_result += result.keys()
    return total_result


def add_to_playlist_by_ids(ids: list[str], playlist_id, sp: spotipy.Spotify, user: str):
    for i in range(0, len(ids), 100):
        sp.user_playlist_add_tracks(user=user, playlist_id=playlist_id, tracks=ids[i:min(i+100, len(ids))], position=None)


def delete_playlist(playlist_id: str, sp: spotipy.Spotify ):
    sp.current_user_unfollow_playlist(playlist_id=playlist_id)