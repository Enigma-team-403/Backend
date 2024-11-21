# from django.shortcuts import render

# from rest_framework import viewsets

# from .models import Board, Label, List
# from .serializers.boards_serializers import BoardSerializer
# from .serializers.labels_serializers import LabelSerializer
# from .serializers.lists_serializers import ListSerializer


# class BoardViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet to provide CRUD functionality for Board model
#     """
#     serializer_class = BoardSerializer
#     def get_queryset(self):
#         """
#         Can be adjusted to filter boards more precisely
#         :return: QuerySet
#         """
#         return Board.objects.all()


# class ListViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet to provide CRUD functionality for List model
#     """
#     serializer_class = ListSerializer

#     def get_queryset(self):
#         """
#         Can be adjusted to filter lists more precisely
#         :return: QuerySet
#         """
#         return List.objects.all()


# class LabelViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet to provide CRUD functionality for Label model
#     """
#     serializer_class = LabelSerializer

#     def get_queryset(self):
#         """
#         Can be adjusted to filter labels more precisely
#         :return: QuerySet
#         """
#         return Label.objects.all()



from rest_framework import viewsets
from boards.models import Board
from boards.serializers.boards_serializers import BoardSerializer
from boards.models import List
from boards.serializers.lists_serializers import ListSerializer
from boards.models import Label
from boards.serializers.labels_serializers import LabelSerializer
from rest_framework.permissions import IsAuthenticated


from rest_framework.permissions import BasePermission

class BoardViewSet(viewsets.ModelViewSet):
    # queryset = Board.objects.all()
    serializer_class = BoardSerializer
    def get_queryset(self):
        return  Board.objects.all()
     

    def get_serializer_context(self):
        # Pass the request context to the serializer so it can access the user
        return {'request': self.request}



class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


    def get_serializer_context(self):
        return {'request': self.request}
    

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


    def get_serializer_context(self):
        return {'request': self.request}

