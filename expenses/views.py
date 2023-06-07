from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer
from . import services


class ExpenseViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for managing expenses.
    """

    permission_classes = [IsAuthenticated]

    # Create Expense
    def create(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = services.create_expense(
                request.user, serializer.validated_data)
            return Response(ExpenseSerializer(expense).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get All Expenses
    def list(self, request):
        expenses = services.get_all_expenses(request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    # Get Expense
    def retrieve(self, request, pk=None):
        expense = services.get_expense(request.user, pk)
        if expense:
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Update Expense
    def update(self, request, pk=None):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = services.update_expense(
                request.user, pk, serializer.validated_data)
            if expense:
                return Response(ExpenseSerializer(expense).data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete Expense
    def destroy(self, request, pk=None):
        if services.delete_expense(request.user, pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
