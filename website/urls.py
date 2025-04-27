from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("dix_km/", views.dix_km, name="dix_km"),
    path("trente_km/", views.trente_km, name="trente_km"),
    path("marche/", views.marche, name="marche"),
    path("politiquedeconfidentialite/", views.RGPD, name="RGPD"),
    path("conditionsgeneralesdutilisation/", views.CGU, name="CGU"),
    path("mentionslegales/", views.mentions_legales, name="mentions_legales"),
    path("reglement/", views.reglement, name="reglement"),
    path("association/", views.association, name="association"),
    path("sponsors/", views.sponsors, name="sponsors"),
    path("galerie/", views.galerie, name="galerie"),
    path("resultats/", views.resultats, name="resultats"),
]
