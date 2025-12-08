from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from applitravel.models import Voyage

# Create your views here.
def connexion(request):
    usr=request.POST['username']
    pwd=request.POST['password']
    user=authenticate(request, username=usr, password=pwd)
    if user is not None:
        login(request, user)
        lesVoyages = Voyage.objects.all()
        return render(
            request, 
            'applitravel/voyages.html', 
            {'voyages': lesVoyages,
             'user': user}
        )
    else:
        return render(
            request, 
            'applicompte/login.html'
        )
    
def deconnexion(request):
    logout(request)
    return render(
        request,
        'applicompte/logout.html'
    )