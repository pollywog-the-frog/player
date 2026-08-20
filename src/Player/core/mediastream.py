from yt_dlp import YoutubeDL
import os
import mpv
import time

class MediaStream:
    def __init__(self, url: str) -> None:
        self.ydl_opts = {
            'format' : 'bestvideo[height<=1080]+bestaudio/best',
            'js_runtimes' : {
                'deno' : {
                    'path' : os.getenv("DENO_PATH")
                },
            },
            'verbose' : True,
            'quiet' : False,
            'cookiesfrombrowser' : ('firefox',),
        }
        self.url = url
        with YoutubeDL(self.ydl_opts) as ydl:
            self.info = ydl.extract_info(url, download=False)
        
        if 'requested_formats' in self.info:
            self.video_url = self.info['requested_formats'][0]['url']
            self.audio_url = self.info['requested_formats'][1]['url']
        else:
            self.video_url = self.info['url']
        
        self.title = self.info.get('title')
        self.duration = self.info.get('duration')
        self.just_played_all = False
        self.just_played_aud = False
        self.just_played_vid = False
