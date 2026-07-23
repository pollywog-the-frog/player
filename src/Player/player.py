#!/usr/bin/env python3

import mpv

url = input('url: ')

player = mpv.MPV(ytdl=True)
player.play(url)
player.wait_for_playback()