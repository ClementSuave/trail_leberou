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