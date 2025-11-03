from django.shortcuts import render
from applitravel.models import Voyage, Ville, Etape
from applitravel.forms import VilleForm, VoyageForm, EtapeForm

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

    # recuperer toutes les villes
    lesVilles = Ville.objects.all()

    #On retourne l'emplacement du template et le voyage recuperer dans la base de données
    return render(
        request,
        "applitravel/voyage.html",
        {'voyage': leVoyage,
        'lesEtapes': lesEtapes,
        'lesVilles' : lesVilles,
        }
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

def ajouterEtape (request, IDVoyage) : # on récupère le formulaire
    form = EtapeForm(request.POST)
    #on teste la validité du formulaire
    if form.is_valid() :
        #on récupère les éléments du formulaire
        vil = form.cleaned_data['ville']
        nbjours = form.cleaned_data['Nb_Jours']
        voy = Voyage.objects.get(IDVoyage = IDVoyage) 
        lesEtapes = Etape.objects.filter(voyage = IDVoyage) 
        lesEtapesduvoyage = ((ligne.ville) for ligne in lesEtapes)

        #on supprime l'étape si elle existe déjà
        if vil in lesEtapesduvoyage :
            eta = Etape.objects.filter(voyage = voy, ville = vil) 
            eta.delete()

        # création de la nouvelle étape et remplissage des attributs 
        newEtape = Etape()
        newEtape.ville = vil
        newEtape.voyage = voy
        newEtape.Nb_Jours = nbjours
        newEtape.save()

    # récupération du voyage dont l'identifiant a été
    # passé en paramètre (voyage_id)
    leVoyage = Voyage.objects.get(IDVoyage = IDVoyage)

    # récupération des étapes constituant le voyage
    lesEtapes = Etape.objects.all().filter(voyage = leVoyage)

    # on récupère toutes les villes
    lesVilles = Ville.objects.all()
    return render(
        request,
        'applitravel/voyage.html',
        {'voyage': leVoyage, 
        'lesEtapes' : lesEtapes, 
        'lesVilles': lesVilles,
        },
    )