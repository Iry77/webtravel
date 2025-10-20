from django.shortcuts import render
from applitravel.models import Voyage, Ville, Etape
from applitravel.forms import VilleForm, VoyageForm

# Create your views here.
def voyages(request) :
    # recuperation des voyages dans la base de données avec les données du shell 
    lesVoyages = Voyage.objects.all()

    # retourne l'emplacement du template, calcul le voyage ainsi que le request
    return render(
        request,
        'applitravel/voyages.html',
        {'voyages': lesVoyages},
    )

def villes(request) :
    # recuperation des voyages dans la base de données avec les données du shell 
    lesVilles = Ville.objects.all()

    # retourne l'emplacement du template, calcul le voyage ainsi que le request
    return render(
        request,
        'applitravel/villes.html',
        {'villes': lesVilles},
    )

def voyage(request, voyage_id) :
    # récuperation du voyage dont l'identifiant a été passé en parametre
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)

    # récuperation des etapes filtrer par voyage
    lesEtapes = Etape.objects.filter(voyage = voyage_id)

    #On retourne l'emplacement du template et le voyage recuperer dans la base de données
    return render(
        request,
        "applitravel/voyage.html",
        {'voyage': leVoyage,
        'etapes': lesEtapes
        },
    )

def formulaireCreationVille(request) : 
    form = VilleForm()
    return render(
        request,
        'applitravel/formulaireCreationVille.html', {'form' : form}
    )

def CreerVille(request) :
    form = VilleForm(request.POST)
    if form.is_valid():
        nomV = form.cleaned_data['NomVille']
        form.save()
    return render(
        request,
        'applitravel/traitementFormulaireCreationVille.html',
        {"nom" : nomV}
    )

def formulaireCreationVoyage(request) : 
    form = VoyageForm()
    return render(
        request,
        'applitravel/formulaireCreationVoyage.html', {'form' : form}
    )

def CreerVoyage(request) : 
    form = VoyageForm(request.POST)
    if form.is_valid():
        titre = form.cleaned_data['Titre']
        form.save()
    return render(
        request,
        'applitravel/traitementFormulaireCreationVoyage.html',
        {"Titre" : titre}
    )

