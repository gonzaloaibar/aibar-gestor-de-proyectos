from django.urls import path #esta funcion sirve para vincular una ruta (url) con una vista espesifica
from apps.users.api import RegisterView, LoginView, RefreshView, MeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('refresh/', RefreshView.as_view(), name='auth-refresh'),
    path('me/', MeView.as_view(), name='auth-me'),
]

