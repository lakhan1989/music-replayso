from django.db import models

# Create your models here.
class Genre(models.Model):

    GENRE_CHOICES = [
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('hip hop', 'Hip hop'),
        ('electronic music', 'Electronic Music'),
        ('jazz', 'Jazz'),
        ('country music', 'Country Music'),
        ('classical music', 'Classical Music'),
        ('rap', 'Rap'),
        ('house music', 'House Music'),
        ('dubstep', 'Dubstep'),
        ('disco', 'Disco'),
        ('instrument', 'Instrument'),
        ('electronic dance music', 'Electronic Dance Music'),
        ('indie rock', 'Indie Rock')
    ]
    genre_name = models.CharField( choices = GENRE_CHOICES, max_length=100)
    description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.genre_name

class Artist(models.Model):
    artist_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    listeners = models.IntegerField(blank=True)
    picture = models.ImageField()
    genre = models.ManyToManyField(Genre)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist_name + " - " + str(self.id)


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    cover = models.ImageField()
    description = models.TextField(max_length=2000, blank=True)
    likes = models.IntegerField(default=0, blank=True, null=True)
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist.artist_name + " - " + str(self.id)

class Track(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    time = models.TimeField()
    plays = models.IntegerField(default=0, blank=True)
    likes = models.IntegerField(default=0, blank=True)
    release_date = models.DateField()
    artist = models.ManyToManyField(Artist)
    genre = models.ManyToManyField(Genre)
    created_at  = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " - " + str(self.id)