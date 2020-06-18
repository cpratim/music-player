from flask import Flask, render_template, url_for, redirect, request, send_file
import requests
import json
from youtube_search import YoutubeSearch
import youtube_dl
import os
from database import Database

app = Flask(__name__)
db = Database('data.json')

def _search(query):
	ret = []
	url = "https://deezerdevs-deezer.p.rapidapi.com/search"
	querystring = {"q": query}
	headers = {
	    'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
	    'x-rapidapi-key': "8c265a3574mshbc1cca717a8a3adp1a6359jsnb33733cf16c1"
	    }

	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text)
	for r in data['data'][:7]:
		result = r['title'], r['artist']['name'], r['album']['title'], r['album']['cover_xl'], r['preview']
		ret.append(result)
	return ret

def _details(title):
	url = "https://deezerdevs-deezer.p.rapidapi.com/search"
	querystring = {"q": title}
	headers = {
	    'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
	    'x-rapidapi-key': "8c265a3574mshbc1cca717a8a3adp1a6359jsnb33733cf16c1"
	    }
	response = requests.request("GET", url, headers=headers, params=querystring)
	r = json.loads(response.text)['data'][0]
	return r['title'], r['artist']['name'], r['album']['title'], r['album']['cover_xl'], r['duration']

def _download(title, filename):
	print(f'{title}')
	results = json.loads(YoutubeSearch(f'{title}', max_results=10).to_json())
	print(results)
	link = f'youtube.com{results["videos"][0]["link"]}'
	ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    	}],
    }
	loc = f'music/{filename}.mp3'
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([link])
	for file in os.listdir():
	    if file.endswith('mp3'):
	        os.rename(file, loc)
	return loc

@app.route('/')
def player():
	songs = db.get_songs()
	active = songs[[k for k in songs][0]]
	print(active)
	return render_template('player.html', songs=songs, active=active)

@app.route('/song/<string:name>')
def song(name):
	songs = db.get_songs()
	active = songs[name]
	return render_template('player.html', songs=songs, active=active)

@app.route('/download')
def download():
	song = request.args.get('song')
	title, artist, album, art, length = _details(song)
	filename = '-'.join(title.split(' '))
	_download(song, filename)
	db.add_song(title, artist, album, art, length)
	return redirect('/')

@app.route('/search/<string:act>', methods=['GET', 'POST'])
def search(act):
	if request.method == 'POST':
		query = request.form['query']
		results = _search(query)
		songs = db.get_songs()
		active = songs[act]
		return render_template('player.html', songs=songs, active=active, query=query, results=results)
	return render_template('results.html', query='Search')

@app.route('/music/<string:title>')
def music(title):
	return send_file(f'music/{title}')

if __name__ == '__main__':
	app.run(port=5000)