from django.core.paginator import Paginator
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movie.models import Movie, Language, Production, Genre


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ['created_at', 'updated_at']


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        exclude = ['created_at', 'updated_at']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['created_at', 'updated_at']


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    production_company = ProductionSerializer()
    languages = LanguageSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ['created_at', 'updated_at']


@api_view(['GET'])
def movie_list(request, *args, **kwargs):
    sort_by_ratings = request.query_params.get('sort_by_ratings', None)
    sort_by_release = request.query_params.get('sort_by_release', None)
    year_of_release = request.query_params.get('year_of_release', None)
    languages = request.query_params.get('languages', None)

    movies = Movie.objects.all()
    if sort_by_ratings:
        if sort_by_ratings.lower() == 'true':
            movies = movies.order_by('-vote_average')
        elif sort_by_ratings.lower() == 'false':
            movies = movies.order_by('vote_average')
        else:
            return Response({'error': 'sort_by_ratings must be "true" or "false"'})

    if sort_by_release:
        if sort_by_release.lower() == 'true':
            movies = movies.order_by('-release_date')
        elif sort_by_release.lower() == 'false':
            movies = movies.order_by('release_date')
        else:
            return Response({'error': 'sort_by_release must be "true" or "false"'})

    if year_of_release:
        if isinstance(year_of_release, str):
            year_of_release = year_of_release.split(",")
            year_of_release = [year.strip() for year in year_of_release]
            if all(year.isdigit() for year in year_of_release):
                year_of_release = [int(year) for year in year_of_release]
                movies = movies.filter(release_date__year__in=year_of_release)
            else:
                return Response({'error': 'year_of_release must be a digit or digits seperated by comma'},
                                status=status.HTTP_400_BAD_REQUEST)

    if languages:
        if isinstance(languages, str):
            languages = languages.split(",")
            languages = [language.strip() for language in languages]
            movies = movies.filter(languages__name__in=languages)
        else:
            return Response({'error': 'languages must be a list of strings or string'},
                            status=status.HTTP_400_BAD_REQUEST)

    paginator = Paginator(movies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    serializer = MovieSerializer(page_obj, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def test(request, *args, **kwargs):
    return Response('test')
