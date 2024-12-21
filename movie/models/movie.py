import uuid

from django.db import models

from movie.models.genre import Genre
from movie.models.language import Language
from movie.models.production import Production

MOVIE_STATUS = [
    ('Released', 'Released'),
    ('In Production', 'In Production'),
    ('Post-Production', 'Post-Production'),
    ('Cancelled', 'Cancelled'),
]

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget = models.BigIntegerField(default=0)
    homepage = models.URLField(default='')
    original_language = models.TextField(default='')
    overview = models.TextField(default='')
    release_date = models.DateField()
    revenue = models.BigIntegerField(default=0)
    runtime = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Released', choices=MOVIE_STATUS)
    title = models.CharField(default='', max_length=255)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    production_company = models.ForeignKey(Production, on_delete=models.DO_NOTHING)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    languages = models.ManyToManyField(Language)

    def __str__(self):
        return self.title
