from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from . import models
import json


# Create your views here.

# users who can login to system
def user(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        models.users.objects.create(
            first_name=payload['first_name'],
            last_name=payload['last_name'],
            email=payload['email']
        )
        #		print ("Hello")
        return HttpResponse("Done")
    if request.method == 'GET':
        return HttpResponse("List Users")


# GET has simple printing of genre name of particular album
def album(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        genre = models.genre.objects.get(genre_id=payload['genre_id'])
        models.album.objects.create(
            album_name=payload['album_name'],
            genre_id=genre,
            total_track=payload['total_track'],
        )
        return HttpResponse("Done")
    if request.method == 'GET':
        album = models.album.objects.get(album_id=1)
        data_out = (album.genre_id.genre_name)
        return HttpResponse(data_out)


# to store genre
def genre(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        models.genre.objects.create(
            genre_name=payload['genre_name']
        )
        return HttpResponse("Done")
    if request.method == 'GET':
        genre_get = request.GET.get("genre_id", None)
        data_out = models.genre.objects.get(genre_id=genre_get)
        return HttpResponse(data_out.genre_name)


# search songs based on genre,artist,album.Get the search value from URL
def song(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        models.song.objects.create(
            title=payload['title'],
            length=payload['length'],
            album_id=payload['album_id'],
            genre_id=payload['genre_id'],
            artist_id=payload['artist_id']
        )
        return HttpResponse("Done")
    if request.method == 'GET':
        search_album = request.GET.get("album_name", None)
        search_title = request.GET.get("title", None)
        search_artist = request.GET.get("artist_name", None)
        search_genre = request.GET.get("genre_name", None)
        if search_album:
            album = models.album.objects.get(album_name=search_album)
            song = models.songs.objects.filter(album_id=album['album_id'])
            return HttpResponse(song)
        elif search_title:
            songlist = models.songs.objects.get(title=search_title)
            song = models.songs.objects.filter(song_id=songlist['song_id'])
            return HttpResponse(song)
        elif search_artist:
            artistlist = models.artist.objects.get(artist_name=search_artist)
            song = models.songs.objects.filter(artist_id=artistlist['artist_id'])
            return HttpResponse(song)
        elif search_genre:
            genrelist = models.genre.objects.get(genre_name=search_genre)
            song = models.songs.objects.filter(genre_id=genrelist['genre_id'])
            return HttpResponse(song)


# for inputting values to artist table
def artist(request):
    payload = None
    if request.method == 'POST':
        payload = json.loads(request.body)
        models.artist.objects.create(
            artist_name=payload['artist_name'],
            total_Songs=payload['total_Songs']
        )
        return HttpResponse("Done")
    if request.method == 'GET':
        return HttpResponse("List Artists")


# create playlist for user and give it a name
def playlist(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        userid = models.users.object.get(user_id=payload['user_id'])
        models.playlist.create(
            playlist_name=payload['playlist_name'],
            user_id=userid
        )
        return HttpResponse("Done")
    if request.method == 'GET':
        user = models.playlist.objects.get(user_id=2)
        print(user.play_id.song_id)
        return HttpResponse("Songs of playlist of user")


# add or delete songs from a playlist of a user
def playlist_song(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        songid = models.songs.object.get(song_id=payload['song_id'])
        playid = models.users.object.get(play_id=payload['play_id'])
        models.playlist.create(
            song_id=songid,
            play_id=playid
        )
        return HttpResponse("Done")
    if request.method == 'GET':
        """returns the song ids inside the playlist."""
    return HttpResponse(
        json.dumps(list(models.playlist_song.filter(play_id=request.GET.get('play_id')).values('song_id'))))
    if request.method == 'DELETE':
        payload = json.loads(request.body)
        songid = models.songs.object.get(song_id=payload['song_id'])
        models.playlist_song.filter(song_id=songid).delete()


# user can rate any songs
def rating(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        songid = models.users.object.get(song_id=payload['song_id'])
        userid = models.users.object.get(user_id=payload['user_id'])
        models.playlist.create(
            rating=payload['rating'],
            song_id=songid,
            user_id=user
        )
        return HttpResponse("Done")

    """Returns the average rating of a song"""
    if request.method == 'GET':
        avg_r = models.Rating.filter(song_id=request.GET.get("song_id")).aggregate(Avg('rating'))
        return HttpResponse(avg_r.get("rating__avg"))
        return HttpResponse("Ratings of songs by users")


# user can recommend song,album,artist or genre to another user
def Recommendation(request):
    payload = None
    if request.method == 'POST':
        payload = request.POST
        rgenreid = models.genre.object.get(genre_id=payload['genre_id'])
        models.recommendation.create(

        )
        return HttpResponse("Done")
    if request.method == 'GET':
        return HttpResponse("Recommendation of songs by users to another user")


# auto suggest songs based on playlist(genre and Artist)
def autoget(request):
    payload = None
    if request.method == 'GET':
        playID = request.GET.get('play_id')
        songs_ids = models.playlist_song.filter(play_id=playID)
        TopGenreID = models.songs.objects.filter(song_id__in=songs_ids).annotate(group_count=Count('genre_id')).order_by('group_count')[0].genre_id
        song_suggest_genre = models.songs.objects.get(genre_id=TopGenreID['genre_id'])
        return_str_genre = "suggestion based on genre" + song_suggest_genre
        TopArtistID = models.songs.objects.filter(song_id__in=songs_ids).annotate(group_count=Count('artist_id')).order_by('group_count')[0].artist_id
        return_str_artist = models.songs.objects.get(artist_id=TopArtistID['artist_id'])
        return HttpResponse(return_str_genre + return_str_artist)

def Recommendation(request):
	payload = None
	if request.method == 'POST':
		payload = request.POST
		models.recommendation.create(
			user_from = payload['user_from'],
			user_to = payload['user_to'],
			typeof = payload['typeof'],
			visited = payload['visited']
		)
		return HttpResponse("Done")