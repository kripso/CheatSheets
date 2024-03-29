import spotipy
import spotipy.util as util
import time
import sys
from pycaw.pycaw import AudioUtilities

spotifyUsername = ""
spotifyAccessScope = ""
spotifyClientID = ""
spotifyClientSecret = ""
spotifyRedirectURI = ""


def setupSpotifyObject(username, scope, clientID, clientSecret, redirectURI):
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI, cache_path=None, oauth_manager=None)
    return spotipy.Spotify(auth=token)


def main():
    global spotifyObject

    try:
        trackInfo = spotifyObject.current_user_playing_track()
    except:
        print("Token Expired")
        spotifyObject = setupSpotifyObject(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret, spotifyRedirectURI)
        trackInfo = spotifyObject.current_user_playing_track()

    try:
        if trackInfo["currently_playing_type"] == "ad":
            muteSpotifyTab(True)
        else:
            muteSpotifyTab(False)
    except TypeError:
        sys.exit(0)
        pass


def muteSpotifyTab(mute):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "Spotify.exe":
            if mute:
                volume.SetMute(1, None)
            else:
                volume.SetMute(0, None)


if __name__ == "__main__":
    spotifyObject = setupSpotifyObject(spotifyUsername, spotifyAccessScope, spotifyClientID, spotifyClientSecret, spotifyRedirectURI)

while True:
    main()
    time.sleep(1)
