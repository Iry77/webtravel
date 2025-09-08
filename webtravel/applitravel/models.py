from django.db import models

# Create your models here.

class Ville(models.Model) :
    #IDVille est une clé primaire auto-incrementée
    IDVille = models.AutoField(primary_key =True)

    #nomVille est une chaine de caractère
    NomVille = models.CharField(max_length = 50)

    #NomPays est une chaine de caractère
    NomPays = models.CharField(max_length = 50)

    #une méthide de type, "tostring"
    def __str__(self) -> str :
        return self.NomVille