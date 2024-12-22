import plexapi, plexapi.server
import config as cfg
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import quote


server = plexapi.server.PlexServer(
    baseurl=cfg.baseurl,
    token=cfg.plex_token
)

scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))



if __name__ == "__main__":
    print("Plexamp ↔ Spotify Playback Link")

    last_played_guid = ""

    while True:
        time.sleep(2)
        
        sessions = server.sessions()
        
        if sessions == []:
            print("Nothing playing. Waiting 5 seconds.")
            time.sleep(3)
            continue
        
        for session in sessions:
            if session.type == 'track': # Pick the session that's playing music
                currentSession = session
            
        if currentSession.player.state == 'paused': # Is the session paused?
            print("paused")
            continue
        
        if currentSession.guid == last_played_guid: # Have we already been listening to this?
            # print("already played")
            continue
        
        track = {
            "title": currentSession.title,
            "artist": currentSession.artist().title,
            "album": currentSession.album().title,
            "guid": currentSession.guid
        }
        
        last_played_guid = track['guid']
        
        for i in track:
            print(track[i])
            
        # END PLEX | BEGIN SPOTIFY
        
        device_id = False
        
        for i in sp.devices()["devices"]:
            print(i["name"])
            if i["name"] == cfg.device_name:
                device_id = i["id"]
                print(device_id)
            
        if not device_id: 
            print("No devices found")
            continue
        
        query = quote(f'track:{track["title"]} artist:{track["artist"]} album:{track["album"]}')

        result = sp.search(q=query, limit=1, type="track", market="GB")
        
        if result["tracks"]["total"] == 0:
            print(f"Track {track['title']} by {track['artist']} could not be found")
            continue
            
        sp_uri = result["tracks"]["items"][0]["uri"]
        
        
        # print(sp.devices())
        
        print("transferring playback")
        
        sp.transfer_playback(device_id=device_id)
        
        time.sleep(1)
        
        print(f"Beginning playback of {track['title']} by {track['artist']} ({sp_uri}) on device_id '{device_id}'")
        sp.start_playback(device_id=device_id, uris=[sp_uri], position_ms=10)
        print("Begun.")
        
        
        
        
        
        