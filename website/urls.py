from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("le-tour-des-fontaines/", views.dix_km, name="dix_km"),
    path("les-trois-clochers/", views.trente_km, name="trente_km"),
    path("balade-au-clair-de-lune/", views.marche, name="marche"),
    path("politique-de-confidentialite/", views.RGPD, name="RGPD"),
    path("conditions-generales-d-utilisation/", views.CGU, name="CGU"),
    path("mentions-legales/", views.mentions_legales, name="mentions_legales"),
    path("reglement/", views.reglement, name="reglement"),
    path("association/", views.association, name="association"),
    path("sponsors/", views.sponsors, name="sponsors"),
    path("galerie/", views.galerie, name="galerie"),
    path("resultats/", views.resultats, name="resultats"),
]
