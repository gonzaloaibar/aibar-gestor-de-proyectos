from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .models import User
from .serializers import UserSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] #doy acceso sin restricciones (cualquiera se puede registrar)
    authentication_classes = [] #DRF no intentará autenticar la petición, no hace falta en esta vista
    throttle_classes = [ScopedRateThrottle]#para limitar la cantidad de peticiones segun un scope
    throttle_scope='auth' #indico el scope que estaba en el settings para registros


#TokenObtainPairView gestiona el inicio de sesion, verificando los datos del usuario
#devuelve un access token para hacer peticiones autenticadas a la api
#y un refresh token para pedir nuevos access token cuando caducan
class LoginView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

#esta vista con TokenRefreshView recibe un Refresh Token válido a través de una petición POST
#luego de validarlo devuelve el access token nuevo (el usuario no se da cuenta de nada)
class RefreshView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

#Datos del usuario autenticado (email no editable)
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    #devuelve una instancia del objeto que debe usarse
    def get_object(self):
        return self.request.user