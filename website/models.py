from django.db import models,transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date, timedelta

class Course(models.Model):
    nom = models.CharField(max_length=200, unique=True, help_text="Nom de la course")
    date_course = models.DateField(help_text="Date")
    description = models.TextField(blank=True, null=True)
    deniv = models.IntegerField(blank=True, null=True, help_text="Dénivelé positif (m)")
    distance = models.IntegerField(blank=True, null=True, help_text="Distance (km)")
    dossard_start = models.IntegerField()
    dossard_end = models.IntegerField()
    heure_depart = models.TimeField(null=True, blank=True, help_text="Heure de départ de la course (HH:MM:SS)")

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
"""
    def position_generale(self):
        if self.temps_course is None:
            return None

        # Get all coureurs for the same course that have a time, ordered by time
        coureurs_classes = Coureur.objects.filter(
            course=self.course,
            temps_course__isnull=False
        ).order_by('temps_course')

        for i, coureur_in_list in enumerate(coureurs_classes):
            if coureur_in_list.pk == self.pk:
                return i + 1
        return None

    @property
    def position_par_categorie(self):
        if self.temps_course is None:
            return None

        # 1. Calculez la catégorie du coureur actuel
        categorie_du_coureur = self.categorie_age

        if categorie_du_coureur in ["Inconnu", "N/A"]:
            return None

        # 2. Récupérez TOUS les coureurs classés de la même course, ordonnés par temps
        coureurs_classes = Coureur.objects.filter(
            course=self.course,
            temps_course__isnull=False
        ).order_by('temps_course')

        position_in_category = 0
        # 3. Itérez et comptez SEULEMENT ceux de la même catégorie
        for coureur_cat in coureurs_classes:
            # Recalculer la catégorie pour chaque coureur
            if coureur_cat.categorie_age == categorie_du_coureur:
                position_in_category += 1
                # 4. Si c'est NOTRE coureur, on retourne le compte actuel
                if coureur_cat.pk == self.pk:
                    return position_in_category
        return None


@receiver(pre_save, sender=Coureur)
def set_dossard(sender, instance, **kwargs):
    if instance._state.adding and instance.dossard is None and instance.course:
        
        max_dossard_for_course_range = Coureur.objects.filter(
            course=instance.course,
            dossard__gte=instance.course.dossard_start,
            dossard__lte=instance.course.dossard_end
        ).aggregate(models.Max('dossard'))['dossard__max']

        if max_dossard_for_course_range is None:
            instance.dossard = instance.course.dossard_start
        else:
            next_dossard = max_dossard_for_course_range + 1
            
            if next_dossard <= instance.course.dossard_end:
                instance.dossard = next_dossard
            else:
                from django.core.exceptions import ValidationError
                raise ValidationError(f"La plage de dossards pour la course '{instance.course.nom}' est pleine (Dossard {instance.course.dossard_start} à {instance.course.dossard_end}). Impossible d'attribuer un nouveau dossard automatiquement.")
"""
class Extract(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='extracts/')

    def __str__(self):
        return f"{self.title}"