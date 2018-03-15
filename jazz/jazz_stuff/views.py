from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import sys
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth as sss
import spotipy.util as util
import math
import requests
import json
from django.http import HttpRequest, HttpResponse
import webbrowser
from django.template import loader
import sys
import socket

# Create your views here.

SPOTIPY_CLIENT_ID = 'this is where my id goes'
SPOTIPY_CLIENT_SECRET = 'this is where my secret key goes'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback/'
SCOPE = 'user-modify-playback-state user-top-read'
CACHE = '.spotipyoauthcache'

def index(request):
	return render(request, 'index.html')



def callSpotify(request):
	if request.method == 'POST':
		if request.is_ajax():
			sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, 
				SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE)
			url = sp_oauth.get_authorize_url()
			webbrowser.open(url)
			return HttpResponseRedirect('/')
	return None

def callback(request):
	sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE)
	code = request.GET['code']
	token = sp_oauth.get_access_token(code)['access_token']
	
	if token:
		sp = spotipy.Spotify(auth=token)
		tracks = sp.current_user_top_tracks(limit=10, time_range='long_term')
		features = []
		average_features = {
		'danceability': 0,
		'energy': 0,
		'key': 0,
		'speechiness': 0,
		'acousticness': 0,
		'instrumentalness': 0,
		'liveness': 0,
		'valence': 0,
		'tempo': 0,
		'mode': 0
		}


		size = len(tracks['items'])


		for track in tracks['items']:
			features.append(sp.audio_features(track['id'])[0])
		# print(features)

		for d in features:
			for key in average_features:
				average_features[key] += (d[key]/size)


		i = 0
		max_pos = 0;
		max_val = 0;

		features = []
		jazz = sp.user_playlist_tracks("alex.hunsader", playlist_id="0UEBW6fTHCOOItrkrJgfIh?si=ri6raet0RleXThDbhRtvKw", limit=10)
		for j in jazz['tracks']['items']:
			features.append(sp.audio_features(j['track']['id'])[0])


		for d in features:
			badness = 0;
			for key in average_features:
				badness += math.fabs(1 - d[key]/average_features[key])
			if badness > max_val:
				max_val = badness
				max_pos = i
			i += 1

		song = jazz['tracks']['items'][max_pos]['track']['name']
		image_url = jazz['tracks']['items'][max_pos]['track']['album']['images'][0]['url']
		print(image_url)
		print(max_val)

		try:
			results = sp.start_playback(device_id="", uris=[jazz['tracks']['items'][max_pos]['track']['uri']])
		except:
			print("could not play the song")

		return render(request, 'answer.html', context={'song': song, 'image': image_url})
	return HttpResponseRedirect('/')
	

