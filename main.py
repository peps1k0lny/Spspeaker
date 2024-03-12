import spotipy
from spotipy.oauth2 import SpotifyOAuth
from gpiozero import Button


class Spspeaker:
    def __init__(self):
        super().__init__()
        self.DEVICE_ID = "509813d283dd03ad4038e74e28637311da0f8cd2"
        self.CLIENT_ID = "81823b42f6df4915803c2cb78ca141b9"
        self.CLIENT_SECRET = "f1c23862e3994a06bed524153212f688"
        self.REDIRECT_URI = "http://127.0.0.1"
        self.SCOPE = "user-read-playback-state,user-modify-playback-state"
        self.CACHE_PATH = "./tokens.txt"

        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                                                          client_secret=self.CLIENT_SECRET,
                                                                          redirect_uri=self.REDIRECT_URI,
                                                                          scope=self.SCOPE,
                                                                          open_browser=False,
                                                                          cache_path=self.CACHE_PATH))
        self.pause = False

        self.btnpause = Button(23)
        self.btnpllist1 = Button(26)
        self.btnpllist2 = Button(19)
        self.btnpllist3 = Button(13)
        self.btnpllist4 = Button(6)
        self.btnpllist5 = Button(5)

        while True:
            self.btnpause.when_pressed = self.pause_or_start
            self.btnpllist1.when_pressed = lambda: [self.start_playlist(0)]
            self.btnpllist2.when_pressed = lambda: [self.start_playlist(1)]
            self.btnpllist3.when_pressed = lambda: [self.start_playlist(2)]
            self.btnpllist4.when_pressed = lambda: [self.start_playlist(3)]
            self.btnpllist5.when_pressed = lambda: [self.start_playlist(4)]

    def pause_or_start(self):
        self.sp.transfer_playback(device_id=self.DEVICE_ID, force_play=False)
        if self.pause is False:
            print('start')
            self.sp.start_playback(device_id=self.DEVICE_ID)
            self.pause = True
        elif self.pause is True:
            print('pause')
            self.sp.pause_playback(device_id=self.DEVICE_ID)
            self.pause = False

    def start_playlist(self, num):
        playlists = ["spotify:playlist:4E4pze60aCpMHbslYqIyQx",
                     "spotify:playlist:37i9dQZF1EIhkGftn1D0Mh",
                     "spotify:playlist:37i9dQZF1Fa1IIVtEpGUcU",
                     "spotify:playlist:37i9dQZF1EIeYLhx9SJ9SI",
                     "spotify:playlist:337o1CcuOoRfoTbmpZ4enF"]
        self.pause = True
        print('playlist', num + 1)
        self.sp.transfer_playback(device_id=self.DEVICE_ID, force_play=False)
        self.sp.start_playback(device_id=self.DEVICE_ID,
                               context_uri=playlists[num],
                               offset={"position": 0},
                               position_ms=0)

    def next_track(self):
        self.pause = True
        self.sp.transfer_playback(device_id=self.DEVICE_ID, force_play=False)
        self.sp.next_track(device_id=self.DEVICE_ID)


if __name__ == '__main__':
    Spspeaker()
