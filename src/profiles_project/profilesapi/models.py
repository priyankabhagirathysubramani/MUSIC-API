from django.db import models


# Create your models here.
class users(models.Model):
    """for creating users."""
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)

class genre(models.Model):
    """for storing genre details"""
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=30)

class artist(models.Model):
    """for storing artist related details"""
    artist_id = models.AutoField(primary_key=True)
    artist_name = models.CharField(max_length=30)
    total_Songs= models.IntegerField()

class album(models.Model):
    """for storing album details"""
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=30)
    genre_id = models.ForeignKey(genre,on_delete=models.CASCADE)
    total_track = models.IntegerField()

class songs(models.Model):
    """for storing songs"""
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    length = models.IntegerField()
    album_id = models.ForeignKey(album,on_delete=models.CASCADE)
    genre_id = models.ForeignKey(genre,on_delete=models.CASCADE)
    artist_id = models.ForeignKey(artist,on_delete=models.CASCADE)

class Favourite(models.Model):
     """to store Favourite flagged songs for user"""
     user_id = models.ForeignKey(users,on_delete=models.CASCADE)
     song_id = models.ForeignKey(songs,on_delete=models.CASCADE)

TypeChoices = (('Artist','AR'),('Song','SO'),('Album','AL'))
class Recommendation(models.Model):
    """Recommendation details of which user is reccommending which song,genre,artist to anther user"""
    user_from = models.IntegerField()
    user_to = models.IntegerField()
    u_id = models.ForeignKey(songs,on_delete=models.CASCADE)
    typeof =  models.CharField(max_length=2,choices = TypeChoices, default='Song')
    visited = models.BooleanField(default=False)

class playlist(models.Model):
    """playlist mapping of user to playlist"""
    playlist_name = models.CharField(max_length=30)
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    play_id = models.IntegerField(primary_key=True)

class playlist_song(models.Model):
    """for mapping playlist of user to song"""
    play_id = models.ForeignKey(playlist,on_delete=models.CASCADE)
    song_id = models.ForeignKey(songs,on_delete=models.CASCADE)
    class Meta:
        unique_together = (("play_id", "song_id"),)

class Rating(models.Model):
    """for rating of users for songs"""
    user_id = models.ForeignKey(users,on_delete=models.CASCADE)
    song_id = models.ForeignKey(songs,on_delete=models.CASCADE)
    rating = models.IntegerField()
    rateid = models.AutoField(primary_key=True)
    class Meta:
        unique_together = (("user_id", "song_id"),)
