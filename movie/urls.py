from django.urls import path

from movie.views.movie import movie_list, test
from movie.views.upload import upload_movie_data

urlpatterns = [
    path('upload/', upload_movie_data),
    path('list/', movie_list),
    path('test/', test),
]