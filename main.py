import spotipy
from spotipy.oauth2 import SpotifyOAuth
from gpiozero import Button, RotaryEncoder
import alsaaudio


class Spspeaker:
    def __init__(self):
        super().__init__()
        self.DEVICE_ID = "509813d283dd03ad4038e74e28637311da0f8cd2"
        self.CLIENT_ID = "***"
        self.CLIENT_SECRET = "***"
        self.REDIRECT_URI = "http://127.0.0.1"
        self.SCOPE = "user-library-modify,user-read-playback-state,user-modify-playback-state"
        self.CACHE_PATH = "./tokens.txt"

        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                                                          client_secret=self.CLIENT_SECRET,
                                                                          redirect_uri=self.REDIRECT_URI,
                                                                          scope=self.SCOPE,
                                                                          open_browser=False,
                                                                          cache_path=self.CACHE_PATH))
        self.sp.transfer_playback(device_id=self.DEVICE_ID, force_play=False)
        self.pause = self.sp.current_playback()["is_playing"]
        self.shuffle = self.sp.current_playback()["shuffle_state"]

        self.button_pause = Button(27)
        self.button_next = Button(17)
        self.button_prev = Button(22)
        self.button_shuffle = Button(10)
        self.button_like = Button(2)

        self.button_playlist1 = Button(26)
        self.button_playlist2 = Button(13)
        self.button_playlist3 = Button(6)
        self.button_playlist4 = Button(5)
        self.button_playlist5 = Button(11)

        self.rotor = RotaryEncoder(8, 7, wrap=True, max_steps=100)

        self.speaker = alsaaudio.Mixer()
        volume = self.speaker.getvolume()[0] - self.speaker.getvolume()[0] % 5
        self.rotor.steps = volume
        print(self.rotor.steps)

        while True:
            self.rotor.when_rotated_clockwise = self.plus_volume
            self.rotor.when_rotated_counter_clockwise = self.minus_volume

            self.button_pause.when_pressed = self.pause_or_start
            self.button_next.when_pressed = self.next_track
            self.button_prev.when_pressed = self.prev_track
            self.button_shuffle.when_pressed = self.shuffle_tracks
            self.button_like.when_pressed = self.like_track

            self.button_playlist1.when_pressed = lambda: [self.start_playlist(0)]
            self.button_playlist2.when_pressed = lambda: [self.start_playlist(1)]
            self.button_playlist3.when_pressed = lambda: [self.start_playlist(2)]
            self.button_playlist4.when_pressed = lambda: [self.start_playlist(3)]
            self.button_playlist5.when_pressed = lambda: [self.start_playlist(4)]

    def pause_or_start(self):
        self.pause = self.sp.current_playback()["is_playing"]
        if self.pause is False:
            print('start')
            self.sp.start_playback(device_id=self.DEVICE_ID)
        else:
            print('pause')
            self.sp.pause_playback(device_id=self.DEVICE_ID)

    def start_playlist(self, num):
        playlists = ["spotify:playlist:4E4pze60aCpMHbslYqIyQx",
                     "spotify:playlist:37i9dQZF1EIhkGftn1D0Mh",
                     "spotify:playlist:37i9dQZF1Fa1IIVtEpGUcU",
                     "spotify:playlist:37i9dQZF1EIeYLhx9SJ9SI",
                     "spotify:album:6eUW0wxWtzkFdaEFsTJto6"]
        print('playlist', num + 1)
        self.sp.transfer_playback(device_id=self.DEVICE_ID, force_play=False)
        self.sp.start_playback(device_id=self.DEVICE_ID,
                               context_uri=playlists[num],
                               offset={"position": 0},
                               position_ms=0)

    def next_track(self):
        print("next")
        self.sp.transfer_playback(device_id=self.DEVICE_ID, force_play=False)
        self.sp.next_track(device_id=self.DEVICE_ID)

    def prev_track(self):
        print("prev")
        self.sp.transfer_playback(device_id=self.DEVICE_ID, force_play=False)
        self.sp.previous_track(device_id=self.DEVICE_ID)

    def shuffle_tracks(self):
        print("shuffle")
        self.shuffle = self.sp.current_playback()["shuffle_state"]
        if self.shuffle is False:
            self.sp.shuffle(state=True, device_id=self.DEVICE_ID)
        else:
            self.sp.shuffle(state=False, device_id=self.DEVICE_ID)

    def like_track(self):
        print("like")
        self.sp.current_user_saved_tracks_add([self.sp.current_user_playing_track()["item"]["uri"]])
        print(self.sp.current_user_playing_track()["item"]["uri"])

    def plus_volume(self):
        if 0 <= self.rotor.steps < 100:
            self.rotor.steps += 4
            print(self.rotor.steps)
            self.speaker.setvolume(self.rotor.steps)

    def minus_volume(self):
        if 0 < self.rotor.steps <= 100:
            self.rotor.steps -= 4
            print(self.rotor.steps)
            self.speaker.setvolume(self.rotor.steps)


if __name__ == '__main__':
    Spspeaker()
