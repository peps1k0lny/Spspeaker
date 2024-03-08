import spotipy
from spotipy.oauth2 import SpotifyOAuth
from gpiozero import Button
from time import sleep

DEVICE_ID="509813d283dd03ad4038e74e28637311da0f8cd2"

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id="81823b42f6df4915803c2cb78ca141b9",
                                               client_secret="f1c23862e3994a06bed524153212f688",
                                               redirect_uri="http://127.0.0.1",
                                                             scope=scope,open_browser=False,cache_path="./tokens.txt"))
ps = 0

def start_playlist():
    global ps, DEVICE_ID
    ps = 1
    print('aboba')
    sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
    sp.start_playback(device_id=DEVICE_ID, context_uri="spotify:playlist:4E4pze60aCpMHbslYqIyQx", offset={"position": 0})

def pause_or_start():
    global ps
    if ps == 0:
        print('start')
        sp.start_playback()
        ps = 1
    elif ps == 1:
        print('pause')
        sp.pause_playback()
        ps = 0

btnpause = Button(23)
btnpllist1 = Button(24)

# pause
while True:
    btnpause.when_pressed = pause_or_start
    btnpllist1.when_pressed = start_playlist
