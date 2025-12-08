from django.shortcuts import render, redirect
from applitravel.models import Voyage, Ville, Etape
from applitravel.forms import VilleForm, VoyageForm, EtapeForm
from django.contrib.auth.models import User

# Vue des voyages (Accessible à tout le monde)
def voyages(request) :
    lesVoyages = Voyage.objects.all()
    user = request.user 
    return render(
        request,
        'applitravel/voyages.html',
        {'voyages': lesVoyages, 'user': user},
    )

# Vue des villes (Sécurisée : Staff uniquement)
def villes(request) :
    if request.user.is_staff:
        lesVilles = Ville.objects.all()
        return render(request, 'applitravel/villes.html', {'villes': lesVilles})
    else:
        # Si non staff, on redirige vers les voyages ou login
        return redirect('/voyages/')

# Détail voyage (Accessible à tout le monde)
def voyage(request, voyage_id) :
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)
    lesEtapes = Etape.objects.filter(voyage = voyage_id)
    lesVilles = Ville.objects.all()
    return render(
        request,
        "applitravel/voyage.html",
        {'voyage': leVoyage, 'lesEtapes': lesEtapes, 'lesVilles' : lesVilles}
    )

# actions réservées au staff

def formulaireCreationVille(request):
    if not request.user.is_staff: return redirect('/voyages/') 
    form = VilleForm()
    return render(request, 'applitravel/formulaireCreationVille.html', {'form' : form})

def CreerVille(request):
    if not request.user.is_staff: return redirect('/voyages/') 
    form = VilleForm(request.POST)
    if form.is_valid():
        nomV = form.cleaned_data['NomVille']
        form.save()
        return render(request, 'applitravel/traitementFormulaireCreationVille.html', {"nom" : nomV})
    return redirect('/villes/add')

def formulaireCreationVoyage(request):
    if not request.user.is_staff: return redirect('/voyages/') 
    form = VoyageForm()
    return render(request, 'applitravel/formulaireCreationVoyage.html', {'form' : form})

def CreerVoyage(request):
    if not request.user.is_staff: return redirect('/voyages/') 
    form = VoyageForm(request.POST, request.FILES)
    if form.is_valid():
        titre = form.cleaned_data['Titre']
        form.save()
        return render(request, 'applitravel/traitementFormulaireCreationVoyage.html', {"Titre" : titre})
    return redirect('/voyages/add')

def ajouterEtape(request, IDVoyage):
    if not request.user.is_staff: return redirect('/voyages/') 
    form = EtapeForm(request.POST)
    if form.is_valid() :
        vil = form.cleaned_data['ville']
        nbjours = form.cleaned_data['Nb_Jours']
        voy = Voyage.objects.get(IDVoyage = IDVoyage) 
        
        # Gestion doublons et création
        existing_etape = Etape.objects.filter(voyage=voy, ville=vil)
        if existing_etape.exists():
            existing_etape.delete()

        newEtape = Etape()
        newEtape.ville = vil
        newEtape.voyage = voy
        newEtape.Nb_Jours = nbjours
        newEtape.save()

    return redirect(f'/voyages/{IDVoyage}')

def supprimerVoyage(request, voyage_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)
    leVoyage.delete()
    return redirect('/voyages/')

def afficherFormulaireModiﬁcationVoyage(request, voyage_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)
    return render(request, 'applitravel/formulaireModiﬁcationVoyage.html', {'voyage': leVoyage})

def modifierVoyage(request, voyage_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)
    form = VoyageForm(request.POST, instance = leVoyage)
    if form.is_valid():
        form.save()
    return render(request, 'applitravel/traitementFormulaireModificationVoyage.html', {'voyage': leVoyage})

def supprimerVille(request, ville_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    laVille = Ville.objects.get(IDVille = ville_id)
    laVille.delete()
    return redirect('villes')

def afficherFormulaireModiﬁcationVille(request, ville_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    laVille = Ville.objects.get(IDVille = ville_id)
    return render(request, 'applitravel/formulaireModiﬁcationVille.html', {'ville': laVille})

def modifierVille(request, ville_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    laVille = Ville.objects.get(IDVille = ville_id)
    form = VilleForm(request.POST, instance = laVille)
    if form.is_valid():
        form.save()
    return render(request, 'applitravel/traitementFormulaireModificationVille.html', {'ville': laVille})

def supprimerEtapeDansVoyage(request, voyage_id, etape_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    etape = Etape.objects.get(IDEtape = etape_id)
    etape.delete()
    return redirect(f'/voyages/{voyage_id}')

def afficherFormulaireModiﬁcationEtape(request, voyage_id, etape_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    leVoyage = Voyage.objects.get(IDVoyage = voyage_id)
    lesEtapes = Etape.objects.all().filter(voyage = leVoyage)
    lesVillesdEtape = lesEtapes.values_list('ville__IDVille')
    lesVilles = Ville.objects.exclude(IDVille__in=lesVillesdEtape)
    return render(request, 'applitravel/formulaireModiﬁcationEtape.html', {
        'voyage': leVoyage, 'lesEtapes' : lesEtapes, 'lesVilles': lesVilles
    })

def ModifierEtapeDansVoyage(request, voyage_id, etape_id):
    if not request.user.is_staff: return redirect('/voyages/') 
    etape = Etape.objects.get(IDEtape = etape_id)
    form = EtapeForm(request.POST, instance=etape)
    if form.is_valid():
        form.save()
    return redirect(f'/voyages/{voyage_id}')