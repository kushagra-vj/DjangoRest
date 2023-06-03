from watchlist.models import WatchList, StreamingPlatform, Review
from watchlist.api.serializers import WatchListSerializer, StreamingPlatformSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ReviewListView(APIView):

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewDetailView(APIView):

    defs

class StreamingListView(APIView):

    def get(self, request):
        streaming_platforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(streaming_platforms, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StreamingDetailView(APIView):

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