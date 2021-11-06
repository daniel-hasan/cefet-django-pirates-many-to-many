from django.db import models

# Create your models here.

class Responsavel(model.Models):
    registro = models.IntegerField()
    nome = models.CharField(max_length=45)

class Tesouro(models.Model):
    nome = models.CharField(max_length=45)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10,decimal_places=2)
    img_tesouro = models.ImageField(upload_to="imgs")

    responsaveis_guarda = models.ManyToManyField(Responsavel)

