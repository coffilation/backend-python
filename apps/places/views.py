from functools import reduce
import requests
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from dots.settings import NOMINATIM_LOOKUP_ENDPOINT, NOMINATIM_SEARCH_ENDPOINT
from .serializers import *
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action


class PlaceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()


class NominatimPlaceViewSet(viewsets.GenericViewSet):
    osm_type_to_prefix = {
        'node': 'N',
        'way': 'W',
        'relation': 'R',
    }
    nominatim_request_params = {
        'format': 'jsonv2',
        'addressdetails': 1,
        'accept-language': 'ru',
    }

    def get_place_object_from_nominatim_place(self, nominatim_place):
        return {
            'latitude': nominatim_place['lat'],
            'longitude': nominatim_place['lon'],
            'osm_id': nominatim_place['osm_id'],
            'osm_type': nominatim_place['osm_type'],
            'display_name': nominatim_place['display_name'],
            'category': nominatim_place['category'],
            'type': nominatim_place['type'],
            'address': nominatim_place['address'],
        }

    @extend_schema(parameters=[NominatimLookupQuerySerializer], responses=PlaceSerializer)
    @action(detail=False, methods=['get'])
    def lookup(self, request):
        serializer = NominatimLookupQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        if Place.objects.filter(**serializer.data).exists():
            return Response(PlaceSerializer(Place.objects.get(**serializer.data)).data)

        try:
            lookup_data = requests.get(
                NOMINATIM_LOOKUP_ENDPOINT,
                params={
                    **self.nominatim_request_params,
                    'osm_ids': self.osm_type_to_prefix[serializer.data['osm_type']] + str(
                        serializer.data['osm_id']
                    )
                },
            ).json()
            for place in lookup_data:
                if place['category'] == serializer.data['category']:
                    place_in_orm = Place.objects.create(
                        **self.get_place_object_from_nominatim_place(place),
                    )
                    return Response(PlaceSerializer(place_in_orm).data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_424_FAILED_DEPENDENCY)

    @extend_schema(
        parameters=[NominatimSearchQuerySerializer],
        responses=PlaceSerializer(many=True)
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        serializer = NominatimSearchQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        try:
            search_data = requests.get(
                NOMINATIM_SEARCH_ENDPOINT,
                params={
                    **self.nominatim_request_params,
                    'bounded': 1,
                    **serializer.data,
                }
            ).json()

            Place.objects.bulk_create(
                [
                    Place(**self.get_place_object_from_nominatim_place(place))
                    for place in search_data
                ],
                ignore_conflicts=True
            )

            place_query = reduce(
                lambda query, place: query | Q(
                    osm_id=place['osm_id'],
                    osm_type=place['osm_type'],
                    category=place['category'],
                ),
                search_data,
                Q(),
            )

            places_in_orm = Place.objects.filter(place_query)

            return Response(PlaceSerializer(places_in_orm, many=True).data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_424_FAILED_DEPENDENCY)
