from django.urls import path
from django.views.generic import RedirectView
from applitravel import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='voyages', permanent=False), name='home'),
    path('voyages/', views.voyages, name='voyages'),
    path('villes/', views.villes, name = 'villes'),
    path('voyages/<int:voyage_id>', views.voyage, name='voyage'),
    path('villes/add', views.formulaireCreationVille, name='ajouter_ville'),
    path('villes/create', views.CreerVille, name='creer_ville'),
    path('voyages/add', views.formulaireCreationVoyage, name='ajouter_voyage'),
    path('voyages/create', views.CreerVoyage, name='creer_voyage'),
    path('voyages/<int:IDVoyage>/addVoyage', views.ajouterEtape, name='ajouter_etape'),
    path('voyages/<int:voyage_id>/delete', views.supprimerVoyage, name='supprimer_voyage'),
    path('voyages/<int:voyage_id>/update', views.afficherFormulaireModificationVoyage, name='formulaire_modifier_voyage'),
    path('voyages/<int:voyage_id>/updated', views.modifierVoyage, name='modifier_voyage'),
    path('villes/<int:ville_id>/delete', views.supprimerVille, name="supprimer_ville"),
    path('villes/<int:ville_id>/update', views.afficherFormulaireModificationVille, name='formulaire_modifier_ville'),
    path('villes/<int:ville_id>/updated', views.modifierVille, name='modifier_ville'),
    path('voyages/<int:voyage_id>/deleteEtape/<int:etape_id>/delete', views.supprimerEtapeDansVoyage, name='supprimer_etape'),
    path('voyages/<int:voyage_id>/update/<int:etape_id>/', views.afficherFormulaireModificationEtape, name='formulaire_modifier_etape'),
    path('voyages/<int:voyage_id>/updated/<int:etape_id>/', views.ModifierEtapeDansVoyage, name='modifier_etape'),
]