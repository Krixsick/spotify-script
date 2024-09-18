import os
import json
import spotipy
import time
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()
user_input = 0

class Spotify():
    
    details = """
1: Display Your Profile Information
2. Search 
3. Create Playlist
4. Add to Playlist
5. Remove Songs from a Playlist
6. User Music Library
7. More Info
                 """
    
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= os.environ["spotify_id"],
                                               client_secret=os.environ["spotify_sec"],
                                               redirect_uri=os.environ["spotify_redirect"],
                                               scope="user-library-read"))
        self.exit = False
        self.options_dict = {
            "1": self.display_profile_info,
            "2": self.search
        }
        
        self.options()
    def options(self):
        while not self.exit:
            time.sleep(1)
            print(Spotify.details)
            try:
                user_input = input("Please choose one of the following options (Number): ")
                choice = self.options_dict[user_input]
                if choice:
                    choice()
                else:
                    print("Invalid, please type in a number listed in the options")
            except Exception as e:
                print(e)
        
    def display_profile_info(self):
        current_user = self.sp.current_user()

        print(f"""
PROFILE
-----------------------------------------------------------
Username: {current_user['display_name']}
Profile Link: {current_user['external_urls']["spotify"]}
Followers: {current_user["followers"]["total"]}
Image: {current_user["images"][0]["url"]}
-----------------------------------------------------------
                  """)
        
    def _search_one_function(self):
        try:
            artist_input = input("Artist name: ")
            self.result = self.sp.search(q=artist_input, limit=1, type="artist")
            artist = self.result["artists"]["items"][0]
        except Exception as e:
            print(e)
        if self.result["artists"]["items"]:
            print(f"""
PROFILE
-----------------------------------------------------------
Username: {artist['name']}
URL: {artist['external_urls']['spotify']}
Followers: {artist['followers']['total']}
Image: {artist['images'][0]['url']}
-----------------------------------------------------------
                    """)
                    
        self.results = self.sp.artist_albums(artist['uri'], album_type='album')
        self.albums = self.results['items']
        
    def search(self):
        user_input = None
        while user_input not in (1, 2, 3):
            print("""
1: Check Albums
2: Check Songs From Each Album
3. Search up playlists or artists
                  """)
            try:
                user_input = int(input("Please choose option 1, 2, or 3: "))
            except Exception as e:
                print(e)
            if user_input == 1:
                self._search_one_function()
                #prints out albums
                while self.results['next']:
                    self.results = self.sp.next(self.results)
                    self.albums.extend(self.results['items'])

                for album in self.albums:
                    print(album['name'])
                
            elif user_input == 2:
                self._search_one_function()
                for album in self.albums:
                    #Gets albums id to find the tracks
                    album_id = album['id']
                    tracks = self.sp.album_tracks(album_id)['items']
                    print(f"-------Album: {album['name']}-------")
                    for track in tracks:
                        print(f"- {track['name']}")
            elif user_input == 3:
                try:
                    search_input = input("Input: ")
                    self.result = self.sp.search(q=search_input, type="artist,playlist,track", limit=10)
                except Exception as e:
                    print(e)
                
                print("Here is what showed up: ")
                print("-----Artists-----")
                for artist in self.result['artists']['items']:
                    print(artist['name'])
                    print(artist["id"])
                print("-----Playlists-----")
                for playlist in self.result['playlists']['items']:
                    print(playlist['name'])
                print("-----Tracks-----")
                for track in self.result['tracks']['items']:
                    print(track['name'])
                try:
                    print("""
                          1. Artist
                          2. Playlist
                          3. Track
                          """)
                    choice_input = int(input("Which choice"))
                
                except Exception as e:
                    print(e)
                
                if choice_input == 1:
                    try:
                        artist_input = input("")
                        pass
                            

            
        
        
        
        
        
        #Display each song from album
        
        #Search up artists and playlists
        
        
            #follow if you want



w = Spotify()


