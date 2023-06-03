# from django.shortcuts import render
# from .models import Movie
# from django.http import JsonResponse


# def movie_list(request):
#     movie = Movie.objects.all().values_list()

#     data = {
#                'movie': list(movie)
#     }
#     return JsonResponse(data, safe=True)    


# def movie_detail(request, movie_id):
#     movie = Movie.objects.get(id=movie_id)
#     data = {
#               'name': movie.name,
#               'description': movie.description,
#               'active': movie.active
#     }
#     return JsonResponse(data, safe=True)