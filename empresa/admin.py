from django.contrib import admin

# Register your models here.
from .models import Topico,Pratica

# admin.site.register(Empresa)
admin.site.register(Topico)
admin.site.register(Pratica)