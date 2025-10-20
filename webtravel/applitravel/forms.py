from django import forms
from django.forms import ModelForm 
from applitravel.models import Ville, Voyage

class VilleForm(forms.ModelForm) :
    class Meta :
        model = Ville
        fields = ['NomVille', 'NomPays']
        labels = {
            'NomVille' : 'Nom de la ville',
            'NomPays' : 'Nom du Pays',
        }

class VoyageForm(forms.ModelForm) : 
    class Meta :
        model = Voyage
        fields = ['Titre', 'Prix']
        labels = {
            'Titre' : 'Titre du voyage',
            'Prix' : 'Prix du voyage',
        }