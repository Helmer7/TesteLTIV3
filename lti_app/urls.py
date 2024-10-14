from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.lti_login, name='lti_login'),
    path('launch/', views.lti_launch, name='lti_launch'),
    path('jwks/', views.jwks, name='jwks'),
]
