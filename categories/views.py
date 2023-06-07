from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer
from . import services


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for managing categories.
    """

    permission_classes = [IsAuthenticated]

    # Create Category
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = services.create_category(serializer.validated_data)
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get All Categories
    def list(self, request):
        categories = services.get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # Get Category
    def retrieve(self, request, pk=None):
        category = services.get_category(pk)
        if category:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Update Category
    def update(self, request, pk=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = services.update_category(pk, serializer.validated_data)
            if category:
                return Response(CategorySerializer(category).data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete Category
    def destroy(self, request, pk=None):
        if services.delete_category(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
