from django.db import models
from django.contrib.auth.models import AbstractUser
from empresa.models import Pratica

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    # empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='funcionarios', null=True, blank=True)
    praticas = models.ManyToManyField(Pratica, related_name='usuarios', blank=True)  # Remove 'null=True'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
