from io import TextIOWrapper

from django.utils.dateparse import parse_date
from rest_framework import serializers, status
from rest_framework.decorators import api_view
import csv
import ast
from rest_framework.response import Response
from movie.models import Movie, Language, Production, Genre
from movie.models.movie import MOVIE_STATUS


class MovieSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_status(self, value):
        if value not in MOVIE_STATUS:
            value = 'NA'
        return value


@api_view(['POST'])
def upload_movie_data(request, *args, **kwargs):
    file = request.FILES['file']
    if not file:
        return Response({'error': 'No csv file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    if file:
        if not file.name.endswith('.csv'):
            return Response({'error': 'Only csv files are supported'}, status=status.HTTP_400_BAD_REQUEST)

    file_data = TextIOWrapper(file, encoding='utf-8')
    csv_reader = csv.DictReader(file_data)
    saved_row_count = 0
    errors = []
    for row in csv_reader:
        movie_data = {
            'budget': row.get('budget', 0),
            'homepage': row.get('homepage', ''),
            'original_language': row.get('original_language', ''),
            'original_title': row.get('original_title', ''),
            'overview': row.get('overview', ''),
            'release_date': parse_date(row.get('release_date', '')),
            'revenue': row.get('revenue', 0),
            'runtime': row.get('runtime', 0),
            'status': row.get('status', 'Released'),
            'title': row.get('title', ''),
            'vote_average': row.get('vote_average', 0),
            'vote_count': row.get('vote_count', 0),
            'production_company': row.get('production_company_id'),
            'genre': row.get('genre_id'),
            'languages': row.get('languages', []),
        }

        genre_id = movie_data.get('genre')
        if genre_id:
            genre_id = int(genre_id)
            genre_obj = Genre.objects.get_or_create(id=genre_id, name=f'Genre with id {genre_id}')[0]
            movie_data['genre'] = genre_obj.id

        production_id = movie_data.get('production_company')
        if production_id:
            production_id = int(production_id)
            production_obj = \
                Production.objects.get_or_create(id=production_id, name=f'Production with id {production_id}')[0]
            movie_data['production_company'] = production_obj.id

        languages = movie_data.get('languages')
        if languages:
            language_instances = []
            if isinstance(languages, str):
                try:
                    languages = ast.literal_eval(
                        languages)
                except (ValueError, SyntaxError):
                    value = []

            for language_name in languages:
                language_instance, created = Language.objects.get_or_create(name=language_name)
                language_instances.append(language_instance.id)
            movie_data['languages'] = language_instances

        serializer = MovieSerializer(data=movie_data)
        if not serializer.is_valid():
            errors.append(serializer.errors)
            continue

        serializer.save()
        saved_row_count = saved_row_count + 1

    return Response({'rows saved': saved_row_count, 'rows with invalid data': len(errors), 'errors': errors, })
