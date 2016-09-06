#!/usr/bin/env python

import re
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError

yt_regex = re.compile(r'(http://|https://)www.youtube.com/watch\?v=(\w*).*')
with open('youtube.tk', 'r') as input:
    DEVELOPER_KEY = input.readline().strip()
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

class NoMusicFoundException(Exception):
    pass

class NoVideoFoundException(Exception):
    pass

def get_youtube_code(msg : str):
    yt_code = None
    match = yt_regex.search(msg)
    if match:
            yt_code = match.group(2)
    else:
        try:
            yt_code = search_youtube_song(msg)
        except NoMusicFoundException:
            return 'No music found.'
    return yt_code

def search_youtube_song(msg : str):
    if ' - ' in msg: # search string is in 'Artist - Song' form
        try:
            return search_youtube_video(msg)
        except NoVideoFoundException:
            raise NoMusicFoundException
    else:
        raise NoMusicFoundException

def search_youtube_video(msg : str):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    try:
        response = youtube.search().list(q = msg, part = 'id', maxResults = 5).execute()
    except HttpError as err:
        print('An HTTP error {0} occured:\n{1}'.format(e.resp.status, e.content))
        raise NoVideoFoundException
    videos = []
    for result in response.get('items', []):
        if result['id']['kind'] == 'youtube#video':
            videos.append(result['id']['videoId'])
    if len(videos) < 1:
        raise NoVideoFoundException
    else:
        return videos[0]

def main():
    print(get_youtube_code('https://www.youtube.com/watch?v=Rrq0g837XZo?t=25'))
    print(get_youtube_code('https://www.youtube.com/playlist?list=FL3yd_LE1pLxBXBWR3aGSKLA'))
    print(get_youtube_code('https://www.youtube.com/watch?v=2lEnpkePi4c&index=1&list=FL3yd_LE1pLxBXBWR3aGSKLA'))
    print(get_youtube_code('The Beatles - Let It Be'))
    print(get_youtube_code('alma'))


if __name__ == '__main__':
    sys.exit(int(main() or 0))
