from django.db import models

# Create your models here.

# class Empresa(models.Model):
#     nome = models.CharField(max_length=50)
#     cnpj = models.CharField(max_length=14, unique=True)
    
    
#     def __str__(self):
#         return self.nome


    
from unidecode import unidecode

class Topico(models.Model):
    nome = models.CharField(max_length=30, unique=True)
    nome_formatado = models.CharField(max_length=30, unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Remove acentos e transforma em minúsculas
        self.nome_formatado = unidecode(self.nome.strip().lower())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome


class Pratica(models.Model):
    nome = models.CharField(max_length=30, unique=True)
    topicos = models.ManyToManyField(Topico, related_name='praticas')

    def save(self, *args, **kwargs):
        # Salva o objeto Pratica primeiro para que ele tenha um ID
        super().save(*args, **kwargs)
        
        # Permitir apenas o primeiro tópico (se existirem múltiplos)
        if self.topicos.count() > 1:
            # Ajusta os tópicos depois que o objeto Pratica já foi salvo
            first_topico = self.topicos.first()
            self.topicos.set([first_topico])

    def __str__(self) -> str:
        return self.nome
