from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from .models import Card
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    ViewSet to provide CRUD functionality to card model
    """
    serializer_class = CardSerializer

    def get_queryset(self):
        """
        Can be adjusted to filter cards more precisely
        :return: QuerySet
        """
        return Card.objects.all()
