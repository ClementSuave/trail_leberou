from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
import os, csv
from django.conf import settings
from .models import Course, Coureur, Extract, Edition
from datetime import datetime, timedelta, date
from .forms import ExtractChoiceForm
from django.contrib.admin.views.decorators import staff_member_required
from PIL import Image
from django.contrib import messages
from .forms import ResultUpdateForm, BenevoleForm

def accueil(request):
    return render(request, "website/accueil.html")
def engagements(request):
    return render(request, "website/engagements.html")
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, 'website/course_template.html', {'course': course})
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
def galerie(request):
    years_queryset = Edition.objects.all()
    gallery_data = []

    static_photos_root = os.path.join(settings.BASE_DIR, "website/static/website/photos")

    for year_obj in years_queryset:
        year_str = str(year_obj.annee)
        year_path = os.path.join(static_photos_root, year_str)
        photos = []

        if os.path.exists(year_path):
            files = sorted(os.listdir(year_path))
            for fl in files:
                if fl.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Just calculate orientation once for layout
                    full_path = os.path.join(year_path, fl)
                    try:
                        with Image.open(full_path) as img:
                            w, h = img.size
                            col_class = 'col-md-4' if w >= h else 'col-md-3'
                    except:
                        col_class = 'col-md-4'

                    photos.append({
                        'static_path': f'website/photos/{year_str}/{fl}',
                        'col_class': col_class
                    })

        gallery_data.append({
            'info': year_obj,
            'photos': photos
        })

    return render(request, "website/galerie.html", {'gallery_data': gallery_data})

@staff_member_required
def update_race_result(request):
    if request.method == 'POST':
        form = ResultUpdateForm(request.POST)
        if form.is_valid():
            dossard_saisi = form.cleaned_data['dossard']
            
            try:
                # Find the runner across ALL courses
                # Note: If two different races use the same bib number, 
                # this will need a filter for 'active' races.
                coureur = Coureur.objects.get(dossard=dossard_saisi)
                course = coureur.course # Get the specific race for this runner

                if coureur.temps_course:
                    messages.warning(request, f"Dossard {dossard_saisi} ({coureur.prenom}) a déjà un temps.")
                
                elif not course.heure_depart:
                    messages.error(request, f"L'heure de départ pour '{course.nom}' n'est pas définie.")
                
                else:
                    # Calculation logic
                    now = datetime.now()
                    start_dt = datetime.combine(course.date_course, course.heure_depart)
                    duration = now - start_dt
                    duration_clean = timedelta(seconds=int(duration.total_seconds()))
                    
                    # Remove microseconds for a cleaner display (HH:MM:SS)
                    coureur.temps_course = duration_clean
                    coureur.save()
                    
                    messages.success(request, f"{coureur.prenom} {coureur.nom} ({course.nom}) : {str(duration).split('.')[0]}")

                    return redirect('finish_line')
            
            except Coureur.DoesNotExist:
                messages.error(request, f"Dossard {dossard_saisi} introuvable.")
    else:
        form = ResultUpdateForm()

    # Get the last 15 recorded times to show on the dashboard
    recent_arrivals = Coureur.objects.filter(temps_course__isnull=False).order_by('-temps_course')[:15]

    return render(request, 'website/arrivées.html', {
        'form': form, 
        'recent_arrivals': recent_arrivals
    })

def resultats(request):
    courses_chrono = Course.objects.all().order_by('-date_course').filter(type="Course")

    for course in courses_chrono:
        course.ordered_participants = Coureur.objects.filter(course=course,temps_course__isnull=False).order_by('temps_course')

    context = {
        'courses_chrono': courses_chrono,
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
                            coureur_date_inscription = datetime.strptime(date_inscription_str, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d')
                        
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

def inscription_benevole(request):
    if request.method == 'POST':
        form = BenevoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Merci de votre inscription en tant que bénévole ! Un email de confirmation vous a été envoyé.")
            return redirect('accueil')
    else:
        form = BenevoleForm()
    return render(request, 'website/benevoles.html', {'form': form})