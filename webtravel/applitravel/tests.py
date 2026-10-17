from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from applitravel.models import Ville, Voyage, Etape


class ModelesTests(TestCase):
    def test_str_etape(self):
        ville = Ville.objects.create(NomVille='Paris', NomPays='France')
        voyage = Voyage.objects.create(Titre='Europe', Prix='999.00')
        etape = Etape.objects.create(voyage=voyage, ville=ville, Nb_Jours=3)
        self.assertEqual(str(etape), 'Paris est une étape de Europe (3 jour(s))')


class AccesEtCrudTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user('staff', password='mdp-Staff-123', is_staff=True)
        self.client_user = User.objects.create_user('client', password='mdp-Client-123')
        self.ville = Ville.objects.create(NomVille='Rome', NomPays='Italie')
        self.voyage = Voyage.objects.create(Titre='Italie', Prix='500.00')
        self.etape = Etape.objects.create(voyage=self.voyage, ville=self.ville, Nb_Jours=2)

    def test_racine_redirige_vers_voyages(self):
        self.assertRedirects(self.client.get('/'), '/voyages/')

    def test_voyage_inexistant_renvoie_404(self):
        self.assertEqual(self.client.get('/voyages/9999').status_code, 404)

    def test_villes_interdites_aux_non_staff(self):
        self.client.force_login(self.client_user)
        self.assertRedirects(self.client.get('/villes/'), '/voyages/', fetch_redirect_response=False)

    def test_suppression_en_get_refusee(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(f'/voyages/{self.voyage.IDVoyage}/delete').status_code, 405)
        self.assertTrue(Voyage.objects.filter(pk=self.voyage.pk).exists())

    def test_suppression_en_post(self):
        self.client.force_login(self.staff)
        self.client.post(f'/voyages/{self.voyage.IDVoyage}/delete')
        self.assertFalse(Voyage.objects.filter(pk=self.voyage.pk).exists())

    def test_creation_ville_invalide_reaffiche_les_erreurs(self):
        self.client.force_login(self.staff)
        response = self.client.post('/villes/create', {'NomVille': '', 'NomPays': 'France'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context['form'].errors)

    def test_modification_voyage_sans_nouvelle_image(self):
        self.client.force_login(self.staff)
        response = self.client.post(f'/voyages/{self.voyage.IDVoyage}/updated', {'Titre': 'Italie 2', 'Prix': '450.00'})
        self.assertRedirects(response, f'/voyages/{self.voyage.IDVoyage}', fetch_redirect_response=False)
        self.voyage.refresh_from_db()
        self.assertEqual(self.voyage.Titre, 'Italie 2')
        self.assertEqual(self.voyage.image.name, 'imagesVoyage/default.jpg')

    def test_prix_negatif_refuse(self):
        self.client.force_login(self.staff)
        response = self.client.post(f'/voyages/{self.voyage.IDVoyage}/updated', {'Titre': 'Italie', 'Prix': '-1'})
        self.assertEqual(response.status_code, 400)

    def test_modification_etape(self):
        self.client.force_login(self.staff)
        url = f'/voyages/{self.voyage.IDVoyage}/update/{self.etape.IDEtape}/'
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(f'/voyages/{self.voyage.IDVoyage}/updated/{self.etape.IDEtape}/',
                                    {'ville': self.ville.IDVille, 'Nb_Jours': 5})
        self.assertRedirects(response, f'/voyages/{self.voyage.IDVoyage}', fetch_redirect_response=False)
        self.etape.refresh_from_db()
        self.assertEqual(self.etape.Nb_Jours, 5)

    def test_modification_etape_vers_ville_deja_utilisee_refusee(self):
        autre = Ville.objects.create(NomVille='Milan', NomPays='Italie')
        Etape.objects.create(voyage=self.voyage, ville=autre, Nb_Jours=1)
        self.client.force_login(self.staff)
        response = self.client.post(f'/voyages/{self.voyage.IDVoyage}/updated/{self.etape.IDEtape}/',
                                    {'ville': autre.IDVille, 'Nb_Jours': 5})
        self.assertEqual(response.status_code, 400)