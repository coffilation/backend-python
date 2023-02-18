from .serializers import PlaceSerializer, Place
from rest_framework import viewsets, mixins


# Create your views here.
class PlaceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        queryset = Place.objects.all()
        return queryset
