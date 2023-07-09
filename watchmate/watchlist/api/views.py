from watchlist.models import WatchList, StreamingPlatform, Review
from watchlist.api.serializers import WatchListSerializer, StreamingPlatformSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend # only applicable for generic classes
from rest_framework import filters
from watchlist.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly


from watchlist.api.pagination import WatchListPagination, WatchListLOPagination,WatchListCursorPagination

class WatchListSearch(generics.ListAPIView): 
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']


class WatchListOrder(generics.ListAPIView): 
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCursorPagination
    # filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs.get('username', None)
    #     return Review.objects.filter(review_user__username=username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)        
        return Review.objects.filter(review_user__username=username)


class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(review_user=review_user, watchlist=movie)

        if review_queryset.exists():
            raise ValidationError("You have already given review for this movie!")
        
        if movie.number_of_rating == 0:
            movie.avg_rating = serializer.validated_data["rating"]
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data["rating"]) / 2

        movie.number_of_rating += 1
        movie.save()
        serializer.save(watchlist=movie, review_user = review_user)


class ReviewListView(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist_id=pk)


class ReviewDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]


# Using mixins
# class ReviewListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetailsView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class StreamingListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        streaming_platforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(streaming_platforms, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data, 
                                                context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StreamingDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, stream_type):
        try:
            streaming_platform = StreamingPlatform.objects.get(id=stream_type)
        except StreamingPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamingPlatformSerializer(streaming_platform, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, stream_type):
        try:
            streaming_platform = StreamingPlatform.objects.get(id=stream_type)
        except StreamingPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamingPlatformSerializer(streaming_platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, stream_type):
        try:
            streaming_platform = StreamingPlatform.objects.get(id=stream_type)
        except StreamingPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        streaming_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class WatchListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movie = WatchList.objects.all()
        serializer = WatchListSerializer(movie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, movie_id):
        try:
            movie = WatchList.objects.get(id=movie_id)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, movie_id):
        movie = WatchList.objects.get(pk=movie_id)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        movie = WatchList.objects.get(pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movie = Movie.objects.all()
#         serilizer = MovieSerializer(movie, many=True) # when multiple objects are returned
#         return Response(serilizer.data)
    
#     if request.method == 'POST':
#         serilizer = MovieSerializer(data=request.data)
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response(serilizer.data, status=201)
#         return Response(serilizer.errors, status=400)
 

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, movie_id):
#     try:
#         movie = Movie.objects.get(pk=movie_id)
#     except Movie.DoesNotExist:
#         return Response({'Error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serilizer = MovieSerializer(movie)
#         return Response(serilizer.data, status=status.HTTP_200_OK)
    
#     if request.method == 'PUT':
#         serilizer = MovieSerializer(movie, data=request.data)
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response(serilizer.data)
#         return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)