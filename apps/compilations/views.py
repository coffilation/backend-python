from .serializers import Compilation, CompilationPlacesSerializer, CompilationSerializer, CompilationPlaceSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class CompilationViewSet(viewsets.ModelViewSet):
    queryset = Compilation.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('add_place', 'remove_place'):
            return CompilationPlaceSerializer
        if self.action in ('add_places', 'remove_places'):
            return CompilationPlacesSerializer
        return CompilationSerializer

    @action(detail=True, methods=['post'], url_path='addPlace')
    def add_place(self, request, pk):
        compilation = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        compilation.places.add(serializer.data['place_id'])
        return Response(status=204)

    @action(detail=True, methods=['post'], url_path='removePlace')
    def remove_place(self, request, pk):
        compilation = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        compilation.places.remove(serializer.data['place_id'])
        return Response(status=204)

    @action(detail=True, methods=['post'], url_path='addPlaces')
    def add_places(self, request, pk):
        compilation = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        compilation.places.add(*serializer.data['place_ids'])
        return Response(status=204)

    @action(detail=True, methods=['post'], url_path='removePlaces')
    def remove_places(self, request, pk):
        compilation = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        compilation.places.remove(*serializer.data['place_ids'])
        return Response(status=204)
