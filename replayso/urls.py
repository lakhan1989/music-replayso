from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('album/<int:id>/', views.album, name='album'),
    path('artist/<int:id>/', views.artist, name='artist'),
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search')
    
]