from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Inscription d'un nouveau client, connecté automatiquement après création du compte
def inscription(request):
    if request.user.is_authenticated:
        return redirect('voyages')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username}, votre compte a été créé.")
            return redirect('voyages')
    else:
        form = UserCreationForm()
    return render(request, 'applicompte/register.html', {'form': form})