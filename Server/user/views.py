from django.shortcuts import render
from .models import DirFile
from .serializers import DirFileDetailSerializer, UserSerializer, DirFileDataSerializer, DirStatusSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.decorators import login_required
# Create your views here.


# class based view to view list of all the files owned by a user
# Create new Files and Directories <-Main Use
class DirFileList(generics.ListCreateAPIView):
    # setting the basic queryset and serializer
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        # serializer.save(owners=User.objects.filter(username__exact=self.request.user.username))
        serializer.save(last_update_by=self.request.user.username)

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owners__pk=self.request.user.pk)


# class based view to view update or delete file instances
# File handling and File end point<- Main Use
class DirFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DirFile.objects.all()
    serializer_class = DirFileDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    # changing lookup fields according to the path
    lookup_field = 'file_path'
    lookup_url_kwarg = 'file_path'


# class based view to view list of all the files owned by a user (DATA Included)
# Create new Files and Directories <-Main Use
class DirFileDataList(generics.ListCreateAPIView):
    # setting the basic queryset and serializer
    queryset = DirFile.objects.all()
    serializer_class = DirFileDataSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        # serializer.save(owners=User.objects.filter(username__exact=self.request.user.username))
        serializer.save(last_update_by=self.request.user.username)

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owners__pk=self.request.user.pk)


# class based view to view update or delete file instances (DATA Included)
# File handling and File end point<- Main Use
class DirFileData(generics.RetrieveUpdateDestroyAPIView):
    queryset = DirFile.objects.all()
    serializer_class = DirFileDataSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    # changing lookup fields according to the path
    lookup_field = 'file_path'
    lookup_url_kwarg = 'file_path'


# # Listing all the users
# # Debugging purposes
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# Details of a particular user
# Can use it for user home page <- Main Use
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'
    lookup_url_kwarg = 'username'


class DirStatus(generics.ListAPIView):
    queryset = DirFile.objects.all()
    serializer_class = DirStatusSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        dir_path = self.kwargs['dir_path']
        queryset = queryset.filter(file_path__startswith=dir_path)
        return queryset.filter(owners__pk=self.request.user.pk)


# Create your views here.
@login_required(login_url="/accounts/login/")
def user_home(request, username):
    if not request.user.username == username:
        return render(request, 'invalid.html')
    res_docs = DirFile.objects.filter(owners__pk=request.user.pk).filter(parent_id__exact=0)
    context = {'files': res_docs}
    return render(request, 'userhome.html', context)


def dfs(node, current_user_pk, tab):
    if not node.file_type == 'Directory':
        return " " * tab + "|\n" + " " * tab + "|___ " + node.name[:-6] + "\n"
    else:
        children = DirFile.objects.filter(owners__pk=current_user_pk).filter(parent_id__exact=node.id)
        children = [c for c in children]
        res_str = " " * tab + "|\n" + " " * tab + "|___ " + node.name + "\n"
        for c in children:
            res_str = res_str + dfs(c, current_user_pk, tab + 6)
        return res_str


@login_required(login_url="/accounts/login/")
def tree_view(request, username):
    if not request.user.username == username:
        return render(request, 'invalid.html')
    res_docs = DirFile.objects.filter(owners__pk=request.user.id).filter(parent_id__exact=0)
    res_docs = [r for r in res_docs]
    result = ""
    while not len(res_docs) == 0:
        node = res_docs.pop(0)
        cur = dfs(node, request.user.pk, 0)
        result = result + cur
    context = {'resstring': result}
    return render(request, 'treeviewpage.html', context)


@login_required(login_url="/accounts/login/")
def dir_view(request, pk, username):
    if not request.user.username == username:
        return render(request, 'invalid.html')
    cur_dir = DirFile.objects.filter(owners__pk=request.user.id).get(id=pk)
    if cur_dir.file_type == 'Directory':
        res_docs = DirFile.objects.filter(owners__pk=request.user.id).filter(parentId__exact=pk)
        dir_name = cur_dir.name
        context = {'files': res_docs, 'dir': dir_name}
        return render(request, 'directorypage.html', context)
    else:
        file_name = cur_dir.name
        file_data = cur_dir.file_content
        file_type = cur_dir.file_type
        context = { 'file_name': file_name, 'file_data': file_data, 'file_type': file_type}
        return render(request, 'filepage.html', context)
    # else:
        # if cur_dir.encryption_scheme == 'aes':
        #     filename = cur_dir.name
        #     filename = filename[:-6]
        #     # look at this later
        #     filedata = cur_dir.fileContent
        #     # look at this later
        #     filetype = cur_dir.file_type
        #     context = {'file_name': filename, 'file_data': filedata, 'file_type': filetype}
        #     return render(request, 'AESFileview.html', context)
