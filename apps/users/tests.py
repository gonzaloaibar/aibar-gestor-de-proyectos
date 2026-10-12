from django.test import TestCase
from django.core.cache import cache
from django.urls import reverse #sirve para generar la URL de una vista o ruta a partir de su nombre, evitando escribir rutas fijas (hardcodeadas) en el código
from rest_framework import status #modulo con codigos de estado http mas descriptivos como status.HTTP_404_NOT_FOUND en lugar de solo 404
from rest_framework.test import APITestCase #para probar vistas de API REST de forma declarativa e integrada
from django.contrib.auth import get_user_model

User = get_user_model()
PASSWORD = 'pasa-maestro-922' #clave para el usuario de prueba en los test

class AuthTest(APITestCase):
    #configuracion de urls
    def setUp(self):
        cache.clear()  # el throttling usa cache: evita falsos 429 entre tests

        #creo las url con reverse
        self.register_url=reverse('auth-register')
        self.login_url=reverse('auth-login')
        self.refresh_url=reverse('auth-refresh')
        self.me_url=reverse('auth-me')

    #creo al usuario para los test
    def _create_user(self, email='ana@example.com'):
        return User.objects.create_user(email, email, PASSWORD)

    '''tests del registro de usuario'''

    def test_register_ok(self):
        #creo el registro
        r=self.client.post(self.register_url,{'email': 'Ana@Example.com', 'password': PASSWORD,
        })
        #self.assertEqual() Se utiliza para verificar que dos valores sean exactamente iguales
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['email'], 'ana@example.com')
        #assertNotIn pregunta si password no esta en el registro
        self.assertNotIn('password', r.data)
        #assertTrue chequea si la expresion es verdadera
        self.assertTrue(User.objects.get(email='ana@example.com').check_password(PASSWORD))