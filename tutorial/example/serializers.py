from rest_framework import serializers

from example.models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Movie
        exclude = ("created_on", )


class MovieMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "name", "viewed")
