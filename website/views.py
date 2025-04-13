from django.shortcuts import render, get_object_or_404

def accueil(request):
	return render(request, "website/accueil.html")
def infos(request):
	return render(request, "website/infos.html")
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