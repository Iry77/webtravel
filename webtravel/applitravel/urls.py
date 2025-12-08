from django.contrib import admin
from django.urls import path
from applitravel import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('voyages/', views.voyages),
    path('villes/', views.villes, name = 'villes'),
    path('voyages/<int:voyage_id>', views.voyage),
    path('villes/add', views.formulaireCreationVille),
    path('villes/create', views.CreerVille),
    path('voyages/add', views.formulaireCreationVoyage),
    path('voyages/create', views.CreerVoyage),
    path('voyages/<int:IDVoyage>/addVoyage', views.ajouterEtape),
    path('voyages/<int:voyage_id>/delete', views.supprimerVoyage),
    path('voyages/<int:voyage_id>/update', views.afficherFormulaireModiﬁcationVoyage),
    path('voyages/<int:voyage_id>/updated', views.modifierVoyage),
    path('villes/<int:ville_id>/delete', views.supprimerVille, name="supprimer_ville"),
    path('villes/<int:ville_id>/update', views.afficherFormulaireModiﬁcationVille),
    path('villes/<int:ville_id>/updated', views.modifierVille),
    path('voyages/<int:voyage_id>/deleteEtape/<int:etape_id>/delete', views.supprimerEtapeDansVoyage, name='supprimer_etape'),
    path('voyages/<int:voyage_id>/update/<int:etape_id>/', views.afficherFormulaireModiﬁcationEtape),
    path('voyages/<int:voyage_id>/updated/<int:etape_id>/', views.ModifierEtapeDansVoyage)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)