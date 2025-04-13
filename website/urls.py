from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("informations/", views.infos, name="infos"),
    path("dix_km/", views.dix_km, name="dix_km"),
    path("trente_km/", views.trente_km, name="trente_km"),
    path("marche/", views.marche, name="marche"),
]
