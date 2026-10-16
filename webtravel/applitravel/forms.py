from django import forms
from django.forms import ModelForm 
from applitravel.models import Ville, Voyage, Etape

class VilleForm(forms.ModelForm) :
    class Meta :
        model = Ville
        fields = ['NomVille', 'NomPays']
        labels = {
            'NomVille' : 'Nom de la ville',
            'NomPays' : 'Nom du Pays',
        }
        widgets = {
            'NomVille' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'NomPays' : forms.TextInput(attrs = {'class' : 'form-control'}),
        }

class VoyageForm(forms.ModelForm) : 
    class Meta :
        model = Voyage
        fields = ['Titre', 'Prix', 'image']
        labels = {
            'Titre' : 'Titre du voyage',
            'Prix' : 'Prix du voyage',
            'image' : 'Photo du voyage',
        }
        widgets = {
            'Titre' : forms.TextInput(attrs={'class': 'form-control'}),
            'Prix' : forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            # FileInput (et non ClearableFileInput) : pas de case "effacer", l'image existante est conservée si aucun fichier n'est envoyé
            'image' : forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class EtapeForm(forms.ModelForm) :
    class Meta:
        model = Etape
        fields = ['ville', 'Nb_Jours']
        labels = {
            'ville' : 'Nom de la ville',
            'Nb_Jours' : 'Nombre de jours',
        }
        widgets = {
            'ville' : forms.Select(attrs = {'class' : 'form-control'}),
            'Nb_Jours' : forms.NumberInput(attrs = {'class' : 'form-control', 'min': '1'}),
        }    