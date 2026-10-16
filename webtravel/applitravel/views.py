from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from applitravel.models import Voyage, Ville, Etape
from applitravel.forms import VilleForm, VoyageForm, EtapeForm

# Décorateur des actions réservées au staff : un non-staff est renvoyé vers la liste des voyages
staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='/voyages/', redirect_field_name=None)

# Vue des voyages (Accessible à tout le monde)
@require_GET
def voyages(request) :
    paginator = Paginator(Voyage.objects.order_by('IDVoyage'), 6)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'applitravel/voyages.html', {'voyages': page})

# Vue des villes (Sécurisée : Staff uniquement)
@require_GET
@staff_required
def villes(request) :
    paginator = Paginator(Ville.objects.order_by('NomVille'), 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'applitravel/villes.html', {'villes': page})

# Détail voyage (Accessible à tout le monde)
@require_GET
def voyage(request, voyage_id) :
    leVoyage = get_object_or_404(Voyage, IDVoyage = voyage_id)
    lesEtapes = Etape.objects.filter(voyage = leVoyage).select_related('ville')
    return render(
        request,
        "applitravel/voyage.html",
        {'voyage': leVoyage, 'lesEtapes': lesEtapes, 'form': EtapeForm()}
    )

# actions réservées au staff

@require_GET
@staff_required
def formulaireCreationVille(request):
    form = VilleForm()
    return render(request, 'applitravel/formulaireCreationVille.html', {'form' : form})

@require_POST
@staff_required
def CreerVille(request):
    form = VilleForm(request.POST)
    if form.is_valid():
        laVille = form.save()
        messages.success(request, f"La ville {laVille.NomVille} a été créée.")
        return redirect('villes')
    return render(request, 'applitravel/formulaireCreationVille.html', {'form' : form}, status=400)

@require_GET
@staff_required
def formulaireCreationVoyage(request):
    form = VoyageForm()
    return render(request, 'applitravel/formulaireCreationVoyage.html', {'form' : form})

@require_POST
@staff_required
def CreerVoyage(request):
    form = VoyageForm(request.POST, request.FILES)
    if form.is_valid():
        leVoyage = form.save()
        messages.success(request, f"Le voyage {leVoyage.Titre} a été créé.")
        return redirect('voyages')
    return render(request, 'applitravel/formulaireCreationVoyage.html', {'form' : form}, status=400)

@require_POST
@staff_required
def ajouterEtape(request, IDVoyage):
    voy = get_object_or_404(Voyage, IDVoyage = IDVoyage)
    form = EtapeForm(request.POST)
    if form.is_valid() :
        vil = form.cleaned_data['ville']
        # Gestion doublons : une étape existante pour cette ville est remplacée
        Etape.objects.filter(voyage=voy, ville=vil).delete()
        Etape.objects.create(voyage=voy, ville=vil, Nb_Jours=form.cleaned_data['Nb_Jours'])
        messages.success(request, f"L'étape {vil.NomVille} a été ajoutée.")
    else:
        messages.error(request, "L'étape n'a pas pu être ajoutée : vérifiez la ville et le nombre de jours.")
    return redirect('voyage', voyage_id=IDVoyage)

@require_POST
@staff_required
def supprimerVoyage(request, voyage_id):
    leVoyage = get_object_or_404(Voyage, IDVoyage = voyage_id)
    leVoyage.delete()
    messages.success(request, f"Le voyage {leVoyage.Titre} a été supprimé.")
    return redirect('voyages')

@require_GET
@staff_required
def afficherFormulaireModificationVoyage(request, voyage_id):
    leVoyage = get_object_or_404(Voyage, IDVoyage = voyage_id)
    form = VoyageForm(instance = leVoyage)
    return render(request, 'applitravel/formulaireModificationVoyage.html', {'voyage': leVoyage, 'form': form})

@require_POST
@staff_required
def modifierVoyage(request, voyage_id):
    leVoyage = get_object_or_404(Voyage, IDVoyage = voyage_id)
    form = VoyageForm(request.POST, request.FILES, instance = leVoyage)
    if form.is_valid():
        form.save()
        messages.success(request, f"Le voyage {leVoyage.Titre} a été modifié.")
        return redirect('voyage', voyage_id=voyage_id)
    return render(request, 'applitravel/formulaireModificationVoyage.html', {'voyage': leVoyage, 'form': form}, status=400)

@require_POST
@staff_required
def supprimerVille(request, ville_id):
    laVille = get_object_or_404(Ville, IDVille = ville_id)
    laVille.delete()
    messages.success(request, f"La ville {laVille.NomVille} a été supprimée.")
    return redirect('villes')

@require_GET
@staff_required
def afficherFormulaireModificationVille(request, ville_id):
    laVille = get_object_or_404(Ville, IDVille = ville_id)
    form = VilleForm(instance = laVille)
    return render(request, 'applitravel/formulaireModificationVille.html', {'ville': laVille, 'form': form})

@require_POST
@staff_required
def modifierVille(request, ville_id):
    laVille = get_object_or_404(Ville, IDVille = ville_id)
    form = VilleForm(request.POST, instance = laVille)
    if form.is_valid():
        form.save()
        messages.success(request, f"La ville {laVille.NomVille} a été modifiée.")
        return redirect('villes')
    return render(request, 'applitravel/formulaireModificationVille.html', {'ville': laVille, 'form': form}, status=400)

@require_POST
@staff_required
def supprimerEtapeDansVoyage(request, voyage_id, etape_id):
    etape = get_object_or_404(Etape, IDEtape = etape_id, voyage__IDVoyage = voyage_id)
    etape.delete()
    messages.success(request, "L'étape a été supprimée.")
    return redirect('voyage', voyage_id=voyage_id)

# Formulaire d'étape dont la liste de villes exclut celles déjà utilisées par les AUTRES étapes du voyage
def _formulaireEtape(etape, data=None):
    form = EtapeForm(data, instance=etape)
    autresVilles = Etape.objects.filter(voyage=etape.voyage).exclude(IDEtape=etape.IDEtape).values_list('ville__IDVille')
    form.fields['ville'].queryset = Ville.objects.exclude(IDVille__in=autresVilles)
    return form

@require_GET
@staff_required
def afficherFormulaireModificationEtape(request, voyage_id, etape_id):
    etape = get_object_or_404(Etape, IDEtape = etape_id, voyage__IDVoyage = voyage_id)
    return render(request, 'applitravel/formulaireModificationEtape.html', {
        'voyage': etape.voyage, 'etape': etape, 'form': _formulaireEtape(etape)
    })

@require_POST
@staff_required
def ModifierEtapeDansVoyage(request, voyage_id, etape_id):
    etape = get_object_or_404(Etape, IDEtape = etape_id, voyage__IDVoyage = voyage_id)
    form = _formulaireEtape(etape, request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "L'étape a été modifiée.")
        return redirect('voyage', voyage_id=voyage_id)
    return render(request, 'applitravel/formulaireModificationEtape.html', {
        'voyage': etape.voyage, 'etape': etape, 'form': form
    }, status=400)