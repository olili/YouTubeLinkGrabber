#! /usr/bin/python3
import requests
import os

def grab(url):
    response = requests.get(url, timeout = 15).text
    if '.m3u8' not in response:
        print("https://www.youtube.com/watch?v=1oh9IEwBbFY")
        return
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end - tuner : end]:
            link = response[end - tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    print(f"pipe://ffmpeg -loglevel fatal -re -i {link[start : end]} -ignore_unknown -map 0:0 -map 0:1 -map 0:2? -map 0:3? -map 0:4? -c:a:0 copy -c:a:1 copy -c:v copy -c:s copy -f mpegts -metadata service_name=\"YT\" pipe:1 ")

with open('./youtubeLink.txt', encoding='utf-8') as f:
    print(f'#EXTM3U ')
    for line in f:
        line = line.strip()
        if not line or line.startswith('##'):
            continue
        if not line.startswith('https:'):
            line = line.split('-')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            print(f'\n#EXTINF:-1 group-title="{grp_title}", {ch_name}')
        else:
            grab(line)          
    

            
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
