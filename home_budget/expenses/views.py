from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer, UserSerializer

from django.db.models import Sum
import json

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
        year = request.query_params.get("year", 0)
        month = request.query_params.get("month", 0)

        queryset = self.get_queryset().filter(date__year=year).values("category").annotate(total=Sum("amount"))
        #serializer = self.get_serializer(queryset, many=True)

        response = {k:v for k, v in request.query_params.items()}
        response["data"] = queryset
        #response = json.dumps(response, indent=4)


        #return Response(serializer.data)
        # czy to json response na pewno? nie ma [] na początku
        return Response(response)



class UsersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
