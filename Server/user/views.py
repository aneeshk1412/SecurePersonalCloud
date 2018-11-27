from django.shortcuts import render
from .models import DirFile
from .serializers import DirFileDetailSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
# Create your views here.


# class based view to view list of all the files owned by a user
# Create new Files and Directories <-Main Use
class DirFileList(generics.ListCreateAPIView):
    # setting the basic queryset and serializer
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# class based view to view update or delete file instances
# File handling and File end point<- Main Use
class DirFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer
    # changing lookup fields according to the path
    lookup_field = 'file_path'
    lookup_url_kwarg = 'file_path'


# Listing all the users
# Debugging purposes
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Details of a particular user
# Can use it for user home page <- Main Use
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
