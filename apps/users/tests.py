from django.test import TestCase
from django.core.cache import cache
from django.urls import reverse #sirve para generar la URL de una vista o ruta a partir de su nombre, evitando escribir rutas fijas (hardcodeadas) en el código
from rest_framework import status #modulo con codigos de estado http mas descriptivos como status.HTTP_404_NOT_FOUND en lugar de solo 404
from rest_framework.test import APITestCase #para probar vistas de API REST de forma declarativa e integrada
from django.contrib.auth import get_user_model

User = get_user_model()
PASSWORD = 'pasa-maestro-922' #clave para el usuario de prueba en los test

'''si no sabes lo que es client: basicamente simula un navegador dentro de las pruebas
para poder realizar las peticiones de manera automatica en los test, viene en la clase APITestCase'''

#la clase APITestCase sirve para pruebas de requests HTTP contra los endpoints DRF
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
        return User.objects.create_user(email=email, password=PASSWORD)

    '''tests del registro de usuario'''

    #el registro es la creacion en si del usuario, por eso no llamo a _create_user, debo probar el endpoint del registro
    def test_register_ok(self):
        #creo el registro
        r=self.client.post(self.register_url,{'email': 'Ana@Example.com', 'password': PASSWORD,
        })
        #self.assertEqual() Se utiliza para verificar que dos valores sean exactamente iguales
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['email'], 'ana@example.com')
        #assertNotIn pregunta si password no esta en el registro
        self.assertNotIn('password', r.data)
        #assertTrue chequea si la expresion es verdadera, osea pregunta si existe el usuario recien registrado
        self.assertTrue(User.objects.get(email='ana@example.com').check_password(PASSWORD))

    def test_register_duplicate_email(self):
        self._create_user()
        #intento registrar un usuario con el mismo email
        r=self.client.post(self.register_url,{'email': 'ANA@example.com', 'password': PASSWORD})

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


    '''tets login/refresh'''

    def test_login_ok(self):
        self._create_user()
        l= self.client.post(self.login_url,{'email': 'ana@example.com', 'password': PASSWORD})

        self.assertEqual(l.status_code, status.HTTP_200_OK)
        self.assertIn('access', l.data)
        self.assertIn('refresh', l.data)

    def test_login_wrong_password(self):
        self._create_user()
        l=self.client.post(self.login_url,{'email': 'ana@example.com', 'password': 'incorrectaxd'})

        self.assertEqual(l.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_ok(self):
        self._create_user()
        #recordar que al realizar un login exitoso se le brinda un acces token y un refresh token
        tokens = self.client.post(self.login_url,{
        'email':'ana@example.com', 'password': PASSWORD}).data
        r=self.client.post(self.refresh_url,{'refresh':tokens['refresh']})

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn('access', r.data)

    '''tests me, testeo endpoints de solicitud de informacion del usuario'''

    def test_me_required_auth(self):
        r=self.client.get(self.me_url)
        #no estoy logeado no tengo autorizacion para solicitar mi informacion
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_ok(self):
        self._create_user()

        #logeo al usuario y obtengo el acces token
        access = self.client.post(self.login_url,{
        'email':'ana@example.com', 'password': PASSWORD}).data['access']

        #le indico a client que use el acces token obtenido para las consultas
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

        #ahora si client puede realizar consultas con el acces token del usuario
        r=self.client.get(self.me_url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['email'], 'ana@example.com')

    def test_me_cannot_change_email(self):
        user = self._create_user()

        #fuerzo la autenticacion ya que no me interasa eso en este test
        self.client.force_authenticate(user)
        #modifico datos del user, email y nombre
        r = self.client.patch(self.me_url, {
            'email': 'otro@example.com', 'first_name': 'Ana',
        })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        #recordar que el email no se puede modificar, por lo que tecnicamente deberia seguir siendo el mismo que en su creacion
        self.assertEqual(user.email, 'ana@example.com')
        self.assertEqual(user.first_name, 'Ana')