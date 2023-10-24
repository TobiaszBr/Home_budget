from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer, UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    @action(detail=False)
    def report(self, request):
        print(request.query_params)
        year = request.query_params.get('year', '2024')
        # queryset ot work on - aggregates?
        queryset = self.get_queryset().filter(date__year=year)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)



class UsersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
