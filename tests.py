from youtube_search import YoutubeSearch
import requests
from bs4 import BeautifulSoup
from google import google
import urllib.request
import requests
import json
import youtube_dl
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def search(query):
	ret = []
	url = "https://deezerdevs-deezer.p.rapidapi.com/search"
	querystring = {"q": query}
	headers = {
	    'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
	    'x-rapidapi-key': "8c265a3574mshbc1cca717a8a3adp1a6359jsnb33733cf16c1"
	    }

	response = requests.request("GET", url, headers=headers, params=querystring)
	results = json.loads(YoutubeSearch(f'{query} audio', max_results=10).to_json())
	#print(results)
	link = f'youtube.com{results["videos"][0]["link"]}'
	data = json.loads(response.text)
	for r in data['data'][:5]:
		print(r)
		result = r['title'], r['artist']['name'], r['album']['title'], r['album']['cover_xl'], r['preview']
		ret.append(result)
	return ret, link

def download(link, title):
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    loc = f'music/{title}.mp3'
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    for file in os.listdir():
        if file.endswith('mp3'):
            os.rename(file, loc)
    return loc

#print(results)
results, link = search('You was right')
print(results[0])
#download(link, 'You Was Right')

#results = google.search_images("you was right album art")
#print(results)
