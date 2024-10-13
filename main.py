"""
Firstly, thank you to Spotipy's api and commands. Everything was possible due to their library. 

Purpose: A short python script to add songs, create playlists, search up albums and tracks for artists. Please remember
to change the parameters in SpotifyOAuth to your own. 

"""

import os
import spotipy
import time
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

#in the future i may add a way to remove tracks 

load_dotenv()
user_input = 0

class Spotify():
    
    details = """
1: Display Your Profile Information
2. Search 
3. Create Playlist
4. Add to Playlist
5. User Music Library
6. More Info
                 """
    
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= os.environ["spotify_id"],
                                               client_secret=os.environ["spotify_sec"],
                                               redirect_uri=os.environ["spotify_redirect"],
                                               scope="user-library-read user-read-private playlist-modify-public playlist-modify-private"))
        self.exit = False
        self.my_id = False
        self.options_dict = {
            "1": self.display_profile_info,
            "2": self.search,
            "3": self.create_playlist,
            "4": self.add_to_playlist,
            "5": self.user_music_lib
        }
        
        self.playlist_to_id =  {
            
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
        self.current_user = self.sp.current_user()

        print(f"""
PROFILE
-----------------------------------------------------------
Username: {self.current_user['display_name']}
Profile Link: {self.current_user['external_urls']["spotify"]}
Followers: {self.current_user["followers"]["total"]}
Image: {self.current_user["images"][0]["url"]}
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
                #prints out tracks
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
                    """ 
                    I want to use another function here to add songs to a playlist or favourite songs/artists/playlists
                    """
                except Exception as e:
                    print(e)
                
                if choice_input == 1:
                    try:
                        artist_input = input("")
                    except Exception as e:
                        print(e)
                    
    
    def _get_id_of_user(self):
        #We get the current user and id of your spotify
        self.current_user = self.sp.current_user()
        self.my_id = self.current_user["id"]
        
    def _get_user_playlist(self):
        #playlist gets the current playlist of the user's spotify and gets the most recent playlists
        self.playlist = self.sp.current_user_playlists(limit=25)
        #Looping through each playlist in the json file
        for item in self.playlist["items"]:
            #We make the dictionary store the information of the name of the playlist and id
            self.playlist_to_id[item["name"]] = item["id"]
        
    
    def create_playlist(self):
        if self.my_id is False: 
            self._get_id_of_user()
        playlist = input("Do you want to create a playlist(Y/N): ").lower()
        
        if playlist == "y": 
            try:
                name = input("Name of Playlist: ")
                public_or_private = input("Public or Private: ").strip().lower()
                is_public = True if public_or_private == 'public' else False
                description = input("Description: ")
            except Exception as e:
                print(e)
            #We create the playlist
            self.sp.user_playlist_create(self.my_id, name, is_public, description)

    def add_to_playlist(self):
        self._get_user_playlist()
        self._get_id_of_user()
        try: 
            #Searches song
            song_input = input("Name of song: ")
            for playlist in self.playlist_to_id:
                print(playlist)
            playlist_type = input("What is the name of your playlist you want to use (Be exact): ")
            result = self.sp.search(q=song_input, type="track", limit=1)
            #Gets track id
            track_id = result['tracks']['items'][0]["id"]
        except Exception as e:
            print(e)
        
        self.sp.user_playlist_add_tracks(self.my_id, self.playlist_to_id[playlist_type], [track_id])
    
    
    def user_music_lib(self):
        self._get_user_playlist()
        for playlist in self.playlist["items"]:
            #Gets the ids of the track
            tracks = self.sp.playlist_tracks(playlist['id'])
            print(f'----------{playlist["name"]}----------')
            #Prints out the tracks and the artists who made them
            for idx, item in enumerate(tracks['items']):
                track = item['track']
                print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")

    def more_info(self):
        print("Please follow this link for help ")



w = Spotify()


