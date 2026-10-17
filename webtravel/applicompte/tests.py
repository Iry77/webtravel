from django.contrib.auth.models import User
from django.test import TestCase


class AuthentificationTests(TestCase):
    def test_page_login_en_get(self):
        self.assertEqual(self.client.get('/login/').status_code, 200)

    def test_login_reussi_redirige_vers_voyages(self):
        User.objects.create_user('client', password='mdp-Client-123')
        response = self.client.post('/login/', {'username': 'client', 'password': 'mdp-Client-123'})
        self.assertRedirects(response, '/voyages/', fetch_redirect_response=False)

    def test_login_echoue_affiche_erreur(self):
        response = self.client.post('/login/', {'username': 'x', 'password': 'y'})
        self.assertContains(response, 'Identifiant ou mot de passe incorrect')

    def test_logout_en_post(self):
        User.objects.create_user('client', password='mdp-Client-123')
        self.client.login(username='client', password='mdp-Client-123')
        self.assertEqual(self.client.get('/logout/').status_code, 405)
        self.assertEqual(self.client.post('/logout/').status_code, 200)

    def test_inscription(self):
        response = self.client.post('/register/', {'username': 'nouveau', 'password1': 'Un-Mot-De-Passe-42', 'password2': 'Un-Mot-De-Passe-42'})
        self.assertRedirects(response, '/voyages/', fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username='nouveau').exists())