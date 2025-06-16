from django.shortcuts import render, get_object_or_404
import os
from django.conf import settings
from .models import Course, Coureur

def accueil(request):
	return render(request, "website/accueil.html")
def dix_km(request):
	return render(request, "website/dix_km.html")
def trente_km(request):
	return render(request, "website/trente_km.html")
def marche(request):
	return render(request, "website/marche.html")
def RGPD(request):
	return render(request, "website/politique_de_confidentialité.html")
def CGU(request):
	return render(request, "website/conditions_générales_utilisation.html")
def mentions_legales(request):
	return render(request, "website/mentions_légales.html")
def reglement(request):
	return render(request, "website/reglement.html")
def association(request):
	return render(request, "website/association.html")
def sponsors(request):
	return render(request, "website/sponsors.html")
def galerie(request):
    context = {}
    flags = os.listdir(os.path.join(settings.STATIC_ROOT, "website/photos/"))
    flags = ['website/photos/'+ fl for fl in flags]
    context['flags'] = flags
    
    return render(request, "website/galerie.html", context)

def resultats(request):
    courses = Course.objects.all().order_by('-date_course')

    for course in courses:
        course.ordered_participants = Coureur.objects.filter(
            course=course,
            temps_course__isnull=False
        ).order_by('temps_course')

    context = {
        'courses': courses,
    }
    
    return render(request, 'website/resultats.html', context)