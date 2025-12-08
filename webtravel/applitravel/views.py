from django.shortcuts import render, redirect
from applitravel.models import Voyage, Ville, Etape
from applitravel.forms import VilleForm, VoyageForm, EtapeForm
from django.urls import reverse

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
    form = VoyageForm(request.POST, request.FILES)
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

def supprimerVoyage(request, voyage_id):
    # Recuperer le voyage
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)

    #Supprimer le voyage
    leVoyage.delete()

    # Récupérer la liste de toutes les voyages
    lesVoyages = Voyage.objects.all()

    # retourne l'emplacement du template, calcul le voyage ainsi que le request
    return render(
        request,
        'applitravel/voyages.html',
        {'voyages': lesVoyages},
    )

def afficherFormulaireModiﬁcationVoyage(request, voyage_id):
    # Recuperer le voyage
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)

    # retourne l'emplacement du template, calcul le voyage ainsi que le request
    return render(
        request,
        'applitravel/formulaireModiﬁcationVoyage.html',
        {'voyage': leVoyage},
    )

def modifierVoyage(request, voyage_id):
    # Recuperer le voyage
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)

    #on recupere le formulaire et on instancie leVoyage
    form = VoyageForm(request.POST, instance = leVoyage)

    if form.is_valid():
        form.save()
    
    #aller chercher dans la base le voyage modifer
    return render(
        request,
        'applitravel/traitementFormulaireModificationVoyage.html',
        {'voyage': leVoyage},
    )

def supprimerVille(request, ville_id):
    # Recuperer le ville
    laVille = Ville.objects.get(IDVille = ville_id)

    #Supprimer le ville
    laVille.delete()

    # Récupérer la liste de toutes les villes
    lesVilles = Ville.objects.all()

    # retourne l'emplacement du template, calcul la ville ainsi que le request
    return redirect('villes')

def afficherFormulaireModiﬁcationVille(request, ville_id):
    # Recuperer la ville
    laVille = Ville.objects.get(IDVille = ville_id)

    # retourne l'emplacement du template, calcul le ville ainsi que le request
    return render(
        request,
        'applitravel/formulaireModiﬁcationVille.html',
        {'ville': laVille},
    )

def modifierVille(request, ville_id):
    # Recuperer la ville
    laVille = Ville.objects.get(IDVille = ville_id)

    #on recupere le formulaire et on instancie laVille
    form = VilleForm(request.POST, instance = laVille)

    if form.is_valid():
        form.save()
    
    #aller chercher dans la base la ville modifer
    return render(
        request,
        'applitravel/traitementFormulaireModificationVille.html',
        {'ville': laVille},
    )

def supprimerEtapeDansVoyage(request, voyage_id, etape_id):
    # Recuperer l'etape
    etape = Etape.objects.get(IDEtape = etape_id)

    # Supprimer l'etape
    etape.delete()

    # Recuperer voyage
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)

    # Récupérer toutes les étapes concernant le voyage
    lesEtapes = Etape.objects.all().filter(voyage = leVoyage)

    # Refabriquer la liste des villes du voyage
    lesVilles = Ville.objects.all()

    return render(
        request,
        'applitravel/voyage.html',
        {'voyage': leVoyage, 
        'lesEtapes' : lesEtapes, 
        'lesVilles': lesVilles,
        },
    )

def afficherFormulaireModiﬁcationEtape(request, voyage_id, etape_id):
    # Recuperer l'etape
    etape = Etape.objects.get(IDEtape = etape_id)
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)

    # recuperation des étapes liée à ce voyage
    lesEtapes = Etape.objects.all().filter(voyage = leVoyage)
    lesVillesdEtape = lesEtapes.values_list('ville__IDVille')

    # Recuperer les villes sans ceux deja existante
    lesVilles = Ville.objects.exclude(IDVille__in=lesVillesdEtape)

    return render(
        request,
        'applitravel/formulaireModiﬁcationEtape.html',
        {
            'voyage': leVoyage, 
            'lesEtapes' : lesEtapes, 
            'lesVilles': lesVilles,
        }
    )

def ModifierEtapeDansVoyage(request, voyage_id, etape_id):
    # Recuperer l'etape
    etape = Etape.objects.get(IDEtape = etape_id)

    form = EtapeForm(request.POST)

    if form.is_valid():
        form.save()
    
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)

    # Récupérer toutes les étapes concernant le voyage
    lesEtapes = Etape.objects.all().filter(voyage = leVoyage)

    # Refabriquer la liste des villes du voyage
    lesVilles = Ville.objects.all()

    return render(
        request,
        'applitravel/voyage.html',
        {'voyage': leVoyage, 
        'lesEtapes' : lesEtapes, 
        'lesVilles': lesVilles,
        },
    )


    

