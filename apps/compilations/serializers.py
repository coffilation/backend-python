from rest_framework import serializers
from .models import Compilation
from apps.places.serializers import PlaceSerializer, Place
from apps.users.serializers import UserSerializer, User


class CompilationSerializer(serializers.ModelSerializer):
    color_regex = r'^#[0-9a-f]{6}$'
    primary_color = serializers.RegexField(color_regex, allow_null=True)
    secondary_color = serializers.RegexField(color_regex, allow_null=True)
    author_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.all(),
        source='author',
    )
    author = UserSerializer(read_only=True)

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
