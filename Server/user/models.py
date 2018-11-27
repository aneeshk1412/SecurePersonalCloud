from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DirFile(models.Model):
    # Basic File Details

    name = models.CharField(max_length=5000)
    file_type = models.CharField(max_length=20)
    modified_time = models.DateTimeField(auto_now=True)
    encryption_scheme = models.CharField(max_length=100)
    md5code = models.TextField()
    file_path = models.TextField()

    # User Details , to be changed for file sharing
    owners = models.ManyToManyField('auth.User', related_name='user')

    # File Contents , to be changed for block level encryption

    file_contents = models.TextField()

    # define the string view of the model instances
    def __str__(self):
        name = str(self.name)
        file_type = str(self.file_type)
        encryption_scheme = str(self.encryption_scheme)
        res = "Name : " + name + " Type : " + file_type + " Scheme : " + encryption_scheme
        return res
