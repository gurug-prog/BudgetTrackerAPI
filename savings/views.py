from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SavingSerializer
from . import services

class SavingViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for managing savings.
    """

    permission_classes = [IsAuthenticated]

    # Create Saving
    def create(self, request):
        serializer = SavingSerializer(data=request.data)
        if serializer.is_valid():
            saving = services.create_saving(request.user, serializer.validated_data)
            return Response(SavingSerializer(saving).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get All Savings
    def list(self, request):
        savings = services.get_all_savings(request.user)
        serializer = SavingSerializer(savings, many=True)
        return Response(serializer.data)

    # Get Saving
    def retrieve(self, request, pk=None):
        saving = services.get_saving(request.user, pk)
        if saving:
            serializer = SavingSerializer(saving)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Update Saving
    def update(self, request, pk=None):
        serializer = SavingSerializer(data=request.data)
        if serializer.is_valid():
            saving = services.update_saving(request.user, pk, serializer.validated_data)
            if saving:
                return Response(SavingSerializer(saving).data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete Saving
    def destroy(self, request, pk=None):
        if services.delete_saving(request.user, pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
