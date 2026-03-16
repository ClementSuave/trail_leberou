from django.contrib import admin, messages
from .admin_filters import CategorieAgeFilter
from .models import Course, Coureur, Extract, Edition, Benevole

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import os, csv

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_course', 'distance', 'deniv')
    search_fields = ('nom',)
    list_filter = ('date_course',)
    empty_value_display = '-vide-'
    actions = ['attribuer_dossards_action', 'calculer_classements_action']

    @admin.action(description="Calculer les rangs (Général et Catégorie)")
    def calculer_classements_action(self, request, queryset):
        for course in queryset:
            count = course.calculer_classements()
            self.message_user(request, f"Classement effectué pour {count} coureurs ({course.nom}).")

    @admin.action(description="Attribuer les dossards manquants (par ordre d'inscription)")
    def attribuer_dossards_action(self, request, queryset):
        for course in queryset:
            count = course.assigner_dossards()
            self.message_user(request, f"{count} dossards attribués pour {course.nom}.", messages.SUCCESS)

@admin.register(Coureur)
class CoureurAdmin(admin.ModelAdmin):
    list_display = ('dossard','prenom', 'nom', 'temps_course', 'categorie_age', 'position_generale', 'position_par_categorie','sexe','course', 'club', 'telephone')
    list_filter = ('sexe','course',CategorieAgeFilter)
    search_fields = ('nom', 'prenom', 'dossard', 'email')
    readonly_fields = ('dossard', 'position_generale', 'position_par_categorie')
    list_editable = ('temps_course',)

    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom','sexe', 'email', 'date_naissance', 'course', 'temps_course','club')
        }),
        ('Informations de course calculées', {
            'fields': ('dossard', 'position_generale', 'position_par_categorie'),
            'classes': ('collapse',),
            'description': "Ces champs sont calculés automatiquement et ne peuvent pas être modifiés."
        }),
    )
    actions = ['export_csv','export_as_gmcap']

    @admin.action(description="Exporter la sélection au format GmCap")
    def export_as_gmcap(modeladmin, request, queryset):
        # Create the response
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="export_gmcap.txt"'
        
        writer = csv.writer(response, delimiter='\t')
        
        header = [
            "PerfAthlete", "Qualif", "Nom", "Prenom", "STRCODNUMClubAthlete", 
            "DateNaissance", "Sexe", "Categorie", "InformationLibre", 
            "STRCODNUMClubEquipe", "LettreEquipe", "ChallengeEquipe", "CodeAppel", 
            "NomEpreuve", "OrdreEditionEpreuve", "CategorieEp", "SexeEpreuve", 
            "CommentaireEpreuve", "CodeAppelSousEpreuve", "NomSousEpreuve", 
            "TypeCross", "NomInterClub", "CodeSexeInterClub", "CategorieInterClub", 
            "OrdreRelaiAthlete"
        ]
        writer.writerow(header)

        for c in queryset:
            temps = ""
            if c.temps_course:
                total_seconds = int(c.temps_course.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                temps = f"{hours:02}:{minutes:02}:{seconds:02}"

            # Build the row
            row = [
                c.position_generale or "",      # PerfAthlete
                "",                             # Qualif
                c.nom.upper(),                  # Nom
                c.prenom.capitalize(),          # Prenom
                c.club,                         # STRCODNUMClubAthlete
                c.date_naissance.strftime('%Y-%m-%d') if c.date_naissance else "",
                c.sexe,                         # Sexe
                c.get_gmcap_category,           # Categorie
                "",                             # InformationLibre
                "",                             # STRCODNUMClubEquipe
                "",                             # LettreEquipe
                "",                             # ChallengeEquipe
                "",                             # CodeAppel
                c.course.nom,                     # NomEpreuve
                "",                             # OrdreEditionEpreuve
                "",                             # CategorieEp
                "",                             # SexeEpreuve
                "Trail du Lébérou",             # CommentaireEpreuve
                c.dossard or "",                # CodeAppelSousEpreuve (Dossard)
                temps,                          # NomSousEpreuve (Temps 1)
                temps,                          # TypeCross (Temps 2/Réel)
                # ... fill the rest with empty strings to match header length
            ]
            # Ensure row length matches header length
            while len(row) < len(header):
                row.append("")
                
            writer.writerow(row)
        return response

        @admin.action(description="Exporter la sélection au format CSV")
        def export_csv(modeladmin, request, queryset):
            return download_csv(request, queryset)

@admin.register(Extract)
class ExtractAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('annee','participants','benevoles')

@admin.register(Benevole)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','email','ville','telephone','CP','adresse')

def download_csv(request, queryset):
  if not request.user.is_staff:
    raise PermissionDenied

  model = queryset.model
  model_fields = model._meta.fields + model._meta.many_to_many
  field_names = [field.name for field in model_fields]
  custom_header_names = ['ID', 'NOM', 'PRENOM', 'EMAIL','EMAIL DE CONTACT', 'DATENAISSANCE', 'SEXE', 'NATION','ADRESSE', 'CP', 'VILLE', 'EPREUVE','CLUB', 'DATE INSCRIPTION', 'TELEPHONE', 'REPAS','DOSSARD', 'TEMPS COURSE']

  response = HttpResponse(content_type='text/csv', charset='utf-8-sig')
  response['Content-Disposition'] = 'attachment; filename="export.csv"'

  writer = csv.writer(response, delimiter=";")
  writer.writerow(custom_header_names)

  for row in queryset:
      values = []
      for field in field_names:
          value = getattr(row, field)
          if callable(value):
              try:
                  value = value() or ''
              except:
                  value = 'Error retrieving value'
          if value is None:
              value = ''
          values.append(value)
      writer.writerow(values)
  return response