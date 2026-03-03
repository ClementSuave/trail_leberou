from django.contrib import admin, messages
from .admin_filters import CategorieAgeFilter
from .models import Course, Coureur, Extract, Edition, Benevole

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import os, csv

def export_csv(modeladmin, request, queryset):
    return download_csv(request, queryset)

export_csv.short_description = "Export to CSV"

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
    actions = (export_csv,)

@admin.register(Extract)
class ExtractAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('annee','participants','benevoles')

@admin.register(Benevole)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','email','ville','telephone','CP','adresse')