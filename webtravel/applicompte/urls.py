from django.urls import path
from django.contrib.auth import views as auth_views
from applicompte import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='applicompte/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='applicompte/logout.html'), name='logout'),
    path('register/', views.inscription, name='register'),
]