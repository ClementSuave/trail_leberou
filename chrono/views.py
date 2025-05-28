from django.shortcuts import render, get_object_or_404
from .forms import ChronoForm


def Chrono(request):

	if request.method == 'POST':

		form = ChronoForm(request.POST)
		
		if form.is_valid():
			data = form.cleaned_data
			ID = get_object_or_404(coureur, dossard=data["dossard"])
			form.fields["heure_arrivee"].initial = datetime.datetime.now()
			form.save()
			messages.success(request, message)
	else:
		form = ChronoForm()
		form.fields["heure_arrivee"].initial = datetime.datetime.now()
	return render(request, 'chrono/chrono.html', {'form': form})
