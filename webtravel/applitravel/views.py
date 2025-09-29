from django.shortcuts import render
from applitravel.models import Voyage

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