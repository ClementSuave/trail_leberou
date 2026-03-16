from django.db import models,transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date, timedelta

class Course(models.Model):

    TYPE = [
        ('Course', 'Course'),
        ('Marche', 'Marche'),
    ]

    nom = models.CharField(max_length=200, unique=True, help_text="Nom de la course")
    slug = models.SlugField(unique=True)
    date_course = models.DateField(help_text="Date")
    description = models.TextField(blank=True, null=True)
    deniv = models.IntegerField(blank=True, null=True, help_text="Dénivelé positif (m)")
    distance = models.IntegerField(blank=True, null=True, help_text="Distance (km)")
    ravito = models.IntegerField(blank=True, null=True, help_text="Nombre de ravitaillements")
    dossard_start = models.IntegerField()
    dossard_end = models.IntegerField()
    heure_depart = models.TimeField(null=True, blank=True, help_text="Heure de départ de la course (HH:MM:SS)")
    type = models.CharField(choices=TYPE,help_text="Type de course")
    retrait_dossard = models.CharField(blank=True, null=True, max_length=200, help_text="Heure retrait dossards")
    age_limite = models.CharField(blank=True, null=True, max_length=200, help_text="Age limite")
    matos_obligatoire = models.CharField(blank=True, null=True, max_length=500, help_text="Matériel obligatoire")
    matos_conseille = models.CharField(blank=True, null=True, max_length=500, help_text="Matériel conseillé")
    color = models.CharField(blank=True, null=True, max_length=20, help_text="entrer '#fffff' pour la couleur")
    
    map_url = models.URLField(blank=True, null=True)
    gpx_file = models.FileField(blank=True, null=True, upload_to='courses/gpx/')
    video = models.FileField(upload_to='courses/videos/', null=True, blank=True,help_text="Video pour le header de la course")
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', null=True, blank=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-date_course', 'nom']

    def __str__(self):
        return f"{self.nom}"

    def calculer_classements(self):

        with transaction.atomic():
            coureurs = list(self.coureurs.filter(temps_course__isnull=False).order_by('temps_course'))
            cat_counters = {}

            for i, coureur in enumerate(coureurs):
                # Classement Général (Scratch)
                coureur.position_generale = i + 1
                
                # Classement par Catégorie
                cat = coureur.categorie_age
                cat_counters[cat] = cat_counters.get(cat, 0) + 1
                coureur.position_par_categorie = cat_counters[cat]

            # 2. Sauvegarde massive pour la performance
            Coureur.objects.bulk_update(coureurs, ['position_generale', 'position_par_categorie'])
            return len(coureurs)

    def assigner_dossards(self):

        with transaction.atomic():
            # 1. Trouver le dernier dossard déjà attribué pour cette course
            last_coureur = self.coureurs.filter(dossard__isnull=False).order_by('-dossard').first()
            
            next_bib = last_coureur.dossard + 1 if last_coureur else self.dossard_start

            coureurs_a_attribuer = self.coureurs.filter(dossard__isnull=True).order_by('date_inscription','nom','prenom')

            updated_list = []
            for coureur in coureurs_a_attribuer:
                if next_bib <= self.dossard_end:
                    coureur.dossard = next_bib
                    updated_list.append(coureur)
                    next_bib += 1
                else:
                    break
            
            Coureur.objects.bulk_update(updated_list, ['dossard'])
            return len(updated_list)

class Coureur(models.Model):

    SEXE_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    emailcontact = models.EmailField(blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    sexe = models.CharField(max_length=1,choices=SEXE_CHOICES,help_text="Sexe du coureur")
    pays = models.CharField(max_length=100,blank=True, null=True)
    adresse = models.CharField(max_length=100,blank=True, null=True)
    CP = models.IntegerField(blank=True, null=True)
    ville = models.CharField(max_length=100,blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='coureurs',help_text="La course à laquelle ce coureur est inscrit.")
    club = models.CharField(max_length=100,blank=True, null=True)
    date_inscription = models.DateField(blank=True, null=True)
    telephone = models.IntegerField(blank=True, null=True)
    
    dossard = models.IntegerField(null=True, blank=True, help_text="Numéro de dossard pour cette course")
    temps_course = models.DurationField(blank=True, null=True, help_text="Durée de la course (format HH:MM:SS)")

    position_generale = models.IntegerField(null=True, blank=True)
    position_par_categorie = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Coureur"
        verbose_name_plural = "Coureurs"
        ordering = ['nom', 'prenom']
        unique_together = ('course', 'dossard')

    def __str__(self):
        return f"{self.dossard or 'N/A'}: {self.prenom} {self.nom}  - {self.course.nom})"

    @property
    def get_gmcap_category(self):

        if not self.date_naissance:
            return "Inconnu"
        
        age = date.today().year - self.date_naissance.year
        if age < 20: return "JU"
        if age < 23: return "ES"
        if age < 35: return "SE"
        if age < 40: return "M0"
        if age < 45: return "M1"
        if age < 50: return "M2"
        if age < 55: return "M3"
        if age < 60: return "M4"
        if age < 65: return "M5"
        return "M6"

    @property
    def categorie_age(self):
        if not self.date_naissance:
            return "Inconnu"
        
        annee_naissance = self.date_naissance.year
        annee_actuelle = date.today().year
        age = annee_actuelle - annee_naissance

        base_categorie = "N/A"
        if 20 <= age <= 22:
            base_categorie = "ES"  # Espoir
        elif 23 <= age <= 34:
            base_categorie = "SE"  # Senior
        elif age >= 35:
            base_categorie = "MA"  # Master
        
        # Combine base_categorie with sex
        if base_categorie != "N/A" and self.sexe in ['M', 'F']:
            return f"{base_categorie} {self.get_sexe_display()}" # e.g., "ES Homme", "SE Femme"
        return "Inconnu"

class Extract(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='extracts/')

    def __str__(self):
        return f"{self.title}"

class Edition(models.Model):
    annee = models.IntegerField(unique=True, help_text="e.g. 2025")
    poster = models.ImageField(upload_to='website/posters/', blank=True, null=True)
    participants = models.PositiveIntegerField(default=0)
    benevoles = models.PositiveIntegerField(default=0)
    resultats_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-annee']

    def __str__(self):
        return str(self.annee)

class Benevole(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    adresse = models.CharField(max_length=100,blank=True, null=True)
    CP = models.IntegerField(blank=True, null=True)
    ville = models.CharField(blank=True, null=True)
    telephone = models.IntegerField()
    
    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"