from rest_framework import serializers
from .models import Compilation
from apps.places.serializers import PlaceSerializer, Place


class CompilationSerializer(serializers.ModelSerializer):
    color_regex = r'^#[0-9a-f]{6}$'
    primary_color = serializers.RegexField(color_regex)
    secondary_color = serializers.RegexField(color_regex)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Compilation
        exclude = ['places']


class CompilationPlacesSerializer(serializers.ModelSerializer):
    place_ids = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        write_only=True,
        source='places'
    )
    places = PlaceSerializer(many=True)

    class Meta:
        model = Compilation
        fields = ['places']
