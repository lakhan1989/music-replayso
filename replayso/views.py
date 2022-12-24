from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user, authenticate, login as login_user
import os
from django.core.files import File
import urllib.request
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.db.models import Q

from .replayso_data.album_data import album_data
from .replayso_data.artist_data import artist_data
from .replayso_data.genre_data import genre_data
from .replayso_data.track_data import track_data

from .models import Album, Artist, Track, Genre

# Create your views here.

def index(request):
  
# adding genre in admin=========================================================

    for gen in genre_data:
        Genre.objects.update_or_create(genre_name = gen["genre_name"], description = gen["description"])

# adding artist in admin=======================================================

    for art in artist_data:
        artist, obj = Artist.objects.update_or_create(artist_name = art["artist_name"], description = art["description"], listeners = art["listeners"])
        
        img_temp = NamedTemporaryFile()
        img_temp.write(urlopen(art["picture"]).read())
        img_temp.flush()

        artist.picture.save(os.path.basename(art["picture"]),File(img_temp))
        artist.save()

        for genre in art["genre"]:
            gen = Genre.objects.get(id=genre)
            artist.genre.add(gen) 
        
        

# adding album in admin===========================================================

    for alb in album_data:

        artist = Artist.objects.get(id=alb["artist"])

        album, albm = Album.objects.update_or_create(artist=artist, title = alb["title"], description = alb["description"], likes = alb['likes'], release_date = alb["release_date"])

        img_temp = NamedTemporaryFile()
        img_temp.write(urlopen(alb["cover"]).read())
        img_temp.flush()
    
        album.cover.save(os.path.basename(alb["cover"]),File(img_temp))
        album.save()


        for genre in alb["genre"]:
            gen = Genre.objects.get(id=genre)
            album.genre.add(gen)



# adding track in admin===========================================================
    
    for trk in track_data:

        album = Album.objects.get(id=trk["album"])

        track, trc = Track.objects.update_or_create(title = trk["title"], album = album, time = trk["time"], plays = trk["plays"], likes = trk["likes"], release_date = trk["release_date"])

        img_temp = NamedTemporaryFile()
        img_temp.write(urlopen(trk["cover"]).read())
        img_temp.flush()
    
        track.cover.save(os.path.basename(trk["cover"]),File(img_temp))
        track.save()

        for artist in trk["artist"]:
            print(artist)
            art = Artist.objects.get(id = artist)
            track.artist.add(art)
            
        for genre in trk["genre"]:
            gen = Genre.objects.get(id = genre)
            track.genre.add(gen)


    return render(request, "index.html")


import datetime

def home(request):
    
    if request.user.is_authenticated:

        data = {} 

        data["artists"] = Artist.objects.all()
        
        data["featured"] = Album.objects.all().order_by("-likes")[0:2]
        data["new_albums"] = Album.objects.all().order_by("created_at")[0:5]
        data["recommend"] = Track.objects.filter().order_by("-likes")[0:12]
        data["new_music"] = Track.objects.all().order_by("created_at")[0:5]
        data["top_tracks"] = Track.objects.all().order_by("-plays")[0:5]
        try:
            song = Track.objects.get(title="Smile")
            song.delete()
        except Exception as e:
            pass            
       
        
    else:
        return redirect("login")

    genre = Genre.objects.get(genre_name="Pop")
    
    track_genre = Genre.objects.get(genre_name="Rock")
    
    data["pop_albums"] = Album.objects.filter(genre__in=[genre.id]).order_by("genre")[0:4]
    
    data["rock_songs"] = Track.objects.filter(genre__in=[track_genre.id]).order_by("genre")[0:5]

    data["genres"] = Genre.objects.all()

    return render(request, "home.html", data)



def album(request, id):

    data = {}
         
    if request.method == "POST":
        liked = request.POST.get("like")
        
        if liked is not None:
            album = Album.objects.get(id=id)
            album.likes = album.likes + 1
            album.save()
            
    try:
        data["album"] = Album.objects.get(id=id)
    except Exception as e:
        return render(request, "404-error.html", data)
   
    data["all_albums"] = Album.objects.all().order_by("-likes")[0:5]
    data["arti"] = Album.objects.filter(artist__id=id) 
    data["tracks"] = Track.objects.filter(album__id = id)

    return render(request, "album.html", data)


def artist(request, id):
    data = {}
    data["artist"] = Artist.objects.all()
    data["artist"] = Artist.objects.get(id=id)
    data["all_albums"] = Album.objects.filter(artist__id = id)

    return render(request, "artist.html", data)
 

def login(request):
    
    data ={}
    
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
         
        user = authenticate(request, username = username, password = password)

        if user:
            login_user(request, user)
            return redirect("home")
        else:
            data["error"] = "Please Enter a Valid Username or Password"
            
    return render(request, "login.html", data)





def signup(request):
     
    if request.method == "POST":
        username = request.POST.get("username")
        email_address = request.POST.get("email")
        password = request.POST.get("password")
        
        if username and email_address:
            user = User.objects.create(username = username, email = email_address)
            user.set_password(password)
            user.save()
            login_user(request, user) 
            if request.user.is_authenticated:
                return redirect("home")
            
    return render(request, "signup.html")



def logout(request):
    logout_user(request)
    return redirect("login")


# def search(request):
   
#    data = {}
   
#    if request.method == "POST":
#        search = request.POST.get("search")
#        print(search)
#        if search:
           
#             data["search_artist"] = Artist.objects.filter(artist_name__icontains=search) 
#             print(data["search_artist"])
            
#             data["search_album"] = Album.objects.filter(Q(title__icontains=search) | Q(artist__artist_name__icontains=search)) 
#             print(data["search_album"])
           
#             data["search_track"] = Track.objects.filter(Q(title__icontains=search) | Q(artist__artist_name__icontains=search)) 
#             print(data["search_track"])
       
       
#    return render(request, "search.html", data)



def search(request):
    
    data ={}
    
    if request.method == "POST":
    
        search = request.POST.get("search")
        print(search)
    
        if search:
                data["search_album"] = Album.objects.filter(Q(title__icontains=search) | Q(artist__artist_name__icontains=search))
                
                
                data["search_artist"] = Artist.objects.filter(artist_name__icontains=search)
            
    return render(request, "search.html", data)