from django.urls import path
from watchlist.views import movie_list, movie_detail

urlpatterns = [
    path('list/', movie_list, name='movie-listt'),
    path('detail/<int:movie_id>/', movie_detail, name='movie-detaill'),
]
