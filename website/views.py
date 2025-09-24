from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
import os, csv
from django.conf import settings
from .models import Course, Coureur, Extract
from datetime import datetime, timedelta
from .forms import ExtractChoiceForm
from django.contrib.admin.views.decorators import staff_member_required

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

@staff_member_required
def import_data(request):
    if request.method == 'POST':
        form = ExtractChoiceForm(request.POST)
        if form.is_valid():
            extract_instance = form.cleaned_data['file_to_import']
            file_path = extract_instance.file.path
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')

                for row in reader:
                    try:
                        print(reader.fieldnames)
                        coureur_nom = row.get('NOM')
                        coureur_prenom = row.get('PRENOM')
                        date_naissance_str = row.get('DATENAISSANCE')
                        date_inscription_str = row.get('DATE INSCRIPTION')
                        epreuve = row.get('EPREUVE')
                        print(coureur_nom)
                        print(coureur_prenom)

                        if date_naissance_str:
                            coureur_date_naissance = datetime.strptime(date_naissance_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                        if date_inscription_str:
                            coureur_date_inscription = datetime.strptime(date_naissance_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                        
                        if not coureur_nom or not coureur_prenom:
                            continue
                        if epreuve:
                            course_instance = Course.objects.get(nom=row['EPREUVE'])

                        try:
                            coureur_instance = Coureur.objects.get(nom=coureur_nom, prenom=coureur_prenom)
                            temps_course_str = row.get('TEMPS COURSE')
                            if temps_course_str:
                                try:
                                    h, m, s = map(int, temps_course_str.split(':'))
                                    coureur_instance.temps_course = timedelta(hours=h, minutes=m, seconds=s)
                                except ValueError:
                                    print(f"Warning: Could not parse TEMPS COURSE '{temps_course_str}' for {coureur_nom} {coureur_prenom}. Keeping existing value or None.")
                            coureur_instance.save()
                        except Coureur.DoesNotExist:
                            data = Coureur(
                                nom = coureur_nom,
                                prenom = coureur_prenom,
                                email = row.get('EMAIL'),
                                emailcontact = row.get('EMAIL DE CONTACT'),
                                date_naissance = coureur_date_naissance,
                                sexe = row.get('SEXE'),
                                pays = row.get('NATION'),
                                adresse = row.get('ADRESSE'),
                                CP = row.get('CP'),
                                ville = row.get('VILLE'),
                                course = course_instance,
                                club = row.get('CLUB'),
                                date_inscription = coureur_date_inscription,
                                telephone = row.get('TELEPHONE'),
                                repas = row.get('Repas'),
                            )
                            data.save()

                    except Course.DoesNotExist:
                        print(f"Warning: Course '{row['EPREUVE']}' not found for record: {row}")
                    except KeyError as e:
                        print(f"Skipping row due to missing key: {e} - Row data: {row}")
                    except Exception as e:
                        print(f"Error processing row: {e} - Row data: {row}")

            #return HttpResponse('Data Uploaded and Updated!!')
            return redirect(reverse('admin:index'))

        except FileNotFoundError:
            return HttpResponse('Error: CSV file not found.', status=404)
        except Exception as e:
            return HttpResponse(f'An error occurred: {e}', status=500)
    else:
        form = ExtractChoiceForm()
        return render(request, 'website/import_data.html', {'form': form})