from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    TYPE_OP = 'op'
    TYPE_CLIENT = 'client'
    TYPE_CHOICES = [
        (TYPE_OP, 'Operation User'),
        (TYPE_CLIENT, 'Client User'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

class File(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name