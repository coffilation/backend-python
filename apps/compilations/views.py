from .serializers import Compilation, CompilationSerializer, CompilationPlacesSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class CompilationViewSet(viewsets.ModelViewSet):
    queryset = Compilation.objects.all()
    serializer_class = CompilationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user)

    @action(detail=True, methods=['put'])
    def places(self, request):
        compilation = self.get_object()
        serializer = CompilationPlacesSerializer(data=request.data)
        if serializer.is_valid():
            compilation.places = serializer.validated_data['places']
            compilation.save()
            return Response(serializer.validated_data['places'])
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
