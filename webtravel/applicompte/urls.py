from django.urls import path, include
from django.contrib.auth import views as auth_views
from applicompte import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='applicompte/login.html'), name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('connexion/',views.connexion),
]