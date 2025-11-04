from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('import-data/', views.import_data, name='import_data'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)