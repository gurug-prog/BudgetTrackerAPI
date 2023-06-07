from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SavingGoalSerializer
from . import services

class SavingGoalViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for managing saving goals.
    """

    permission_classes = [IsAuthenticated]

    # Create Saving Goal
    def create(self, request):
        serializer = SavingGoalSerializer(data=request.data)
        if serializer.is_valid():
            goal = services.create_saving_goal(request.user, serializer.validated_data)
            return Response(SavingGoalSerializer(goal).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get All Saving Goals
    def list(self, request):
        goals = services.get_all_saving_goals(request.user)
        serializer = SavingGoalSerializer(goals, many=True)
        return Response(serializer.data)

    # Get Saving Goal
    def retrieve(self, request, pk=None):
        goal = services.get_saving_goal(request.user, pk)
        if goal:
            serializer = SavingGoalSerializer(goal)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Update Saving Goal
    def update(self, request, pk=None):
        serializer = SavingGoalSerializer(data=request.data)
        if serializer.is_valid():
            goal = services.update_saving_goal(request.user, pk, serializer.validated_data)
            if goal:
                return Response(SavingGoalSerializer(goal).data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete Saving Goal
    def destroy(self, request, pk=None):
        if services.delete_saving_goal(request.user, pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
