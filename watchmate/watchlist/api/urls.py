from django.urls import path
# from watchlist.api.views import movie_list, movie_detail
from watchlist.api.views import WatchListView, WatchDetailView, StreamingListView, StreamingDetailView

urlpatterns = [
    # path('list/', movie_list, name='movie-list'),
    # path('detail/<int:movie_id>/', movie_detail, name='movie-detail'),
    
    path('list/', WatchListView.as_view(), name='movie-list'),
    path('detail/<int:movie_id>/', WatchDetailView.as_view(), name='movie-detail'),
    path('stream_list/', StreamingListView.as_view(), name='stream-list'),
    path('stream_detail/<int:stream_type>', StreamingDetailView.as_view(), name='stream-detail'),

]
