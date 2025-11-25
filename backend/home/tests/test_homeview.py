from django.test import TestCase
from users.factories import CustomUserFactory


class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/base.html')

    def test_home_view_content(self):
        response = self.client.get('/')
        self.assertContains(response, 'Bienvenue sur KoobFood')
        self.assertContains(response, "Accueil")
        self.assertContains(response, "Restaurants")

    def test_home_view_user(self):
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertNotContains(response, 'Déconnexion')
        self.assertContains(response, 'Se connecter')
        self.assertContains(response, "S'inscrire")
        self.assertContains(response, 'Restaurants')

        user: CustomUserFactory = CustomUserFactory()
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Déconnexion')


