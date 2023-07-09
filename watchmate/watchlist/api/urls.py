from django.urls import path
# from watchlist.api.views import movie_list, movie_detail
from watchlist.api.views import WatchListView, WatchDetailView, StreamingListView, StreamingDetailView, \
    ReviewListView, ReviewDetailsView, ReviewCreateView, UserReview, WatchListSearch, \
    WatchListOrder

urlpatterns = [
    # path('list/', movie_list, name='movie-list'),
    # path('detail/<int:movie_id>/', movie_detail, name='movie-detail'),
    
    path('list/', WatchListView.as_view(), name='movie-list'),
    path('detail/<int:movie_id>/', WatchDetailView.as_view(), name='movie-detail'),
    path('stream_list/', StreamingListView.as_view(), name='stream-list'),
    path('stream_detail/<int:stream_type>', StreamingDetailView.as_view(), name='stream-detail'),

    # Generic views
    # path('reviews/', ReviewListView.as_view(), name='review-list'),
    # path('reviews/<int:pk>', ReviewDetailsView.as_view(), name='review-detail'),

    path('<int:pk>/review_create/', ReviewCreateView.as_view(), name='review-create'), #create reviews for perticular movie
    path('<int:pk>/reviews/', ReviewListView.as_view(), name='review-list'), #All reviews for perticular id
    path('review/<int:pk>/', ReviewDetailsView.as_view(), name='review-detail'), # specific review

    path('reviews/', UserReview.as_view(), name='user-review-detail'),

    # Searching
    path('search_watch/', WatchListSearch.as_view(), name='search-watch'), 

    # Ordering
    path('ordering_watch/', WatchListOrder.as_view(), name='order-watch'), 

]
