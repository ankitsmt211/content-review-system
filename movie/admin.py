from django.contrib import admin

from movie.models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'status', 'budget', 'revenue')
    list_filter = ('status', 'release_date', 'genre')
    search_fields = ('title','id')
    list_per_page = 20

    fields = (
        'title', 'release_date', 'status', 'budget', 'revenue', 'runtime', 'overview', 'production_company', 'genre',
        'languages')

    filter_horizontal = ('languages',)

admin.site.register(Movie, MovieAdmin)
