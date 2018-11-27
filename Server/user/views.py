from django.shortcuts import render
from .models import DirFile
from .serializers import DirFileDetailSerializer
from rest_framework import generics
# Create your views here.


# class based view to view list of all the files owned by a user
# also for creating new file for the user
class DirFileList(generics.ListCreateAPIView):
    # setting the basic queryset and serializer
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer


# class based view to view update or delete file instances
class DirFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer
    # changing lookup fields according to the path
    lookup_field = 'file_path'
    lookup_url_kwarg = 'file_path'
