from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

# Create your models here.
class Ville(models.Model) :
    #IDVille est une clé primaire auto-incrementée
    IDVille = models.AutoField(primary_key = True)

    #nomVille est une chaine de caractère
    NomVille = models.CharField(max_length = 50)

    #NomPays est une chaine de caractère
    NomPays = models.CharField(max_length = 50)

    #une méthide de type, "tostring"
    def __str__(self) -> str :
        return self.NomVille + "(" + self.NomPays + ")"

class Voyage(models.Model) :
    #IDVoyage est une clé primaire auto-incrementée
    IDVoyage = models.AutoField(primary_key =True)

    #Titre est une chaine de caractère
    Titre = models.CharField(max_length = 50)

     #Le prix est un decimal positif, maximum 8 chiffres dont 2 decimales
    Prix = models.DecimalField(max_digits = 8, decimal_places = 2, validators = [MinValueValidator(Decimal('0.00'))])

    # l'image de presentation du voyage
    image = models.ImageField(default= 'imagesVoyage/default.jpg', upload_to='imagesVoyage/', blank = True)

    #une méthide de type, "tostring"
    def __str__(self) -> str :
        return self.Titre + '(' + str(self.Prix) + ')'

class Etape (models.Model):
    #la classe Meta qui gère l'unicité de la clé étrangère
    class Meta:
        unique_together = ('voyage', 'ville') #le nom des champs clés étrangères

    #IDEtape est unc clé primaire auto-incrémentée
    IDEtape = models.AutoField(primary_key = True)

    #les deux clés étrangères dont les nom correspondent aux classes respectives 
    # #en minuscule
    voyage = models.ForeignKey(Voyage, on_delete = models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete = models.CASCADE)

    #Nb Jours est un entier strictement positif
    Nb_Jours = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])

    #Une méthode de type "toString"
    def __str__(self) -> str :
        return f"{self.ville.NomVille} est une étape de {self.voyage.Titre} ({self.Nb_Jours} jour(s))"