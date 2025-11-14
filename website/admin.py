from django.contrib import admin
from .admin_filters import CategorieAgeFilter
from .models import Course, Coureur, Extract

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

@admin.register(Coureur)
class CoureurAdmin(admin.ModelAdmin):
    list_display = ('dossard','prenom', 'nom', 'temps_course', 'categorie_age', 'position_generale', 'position_par_categorie','sexe','course', 'club', 'telephone','repas')
    list_filter = ('sexe','course',CategorieAgeFilter)
    search_fields = ('nom', 'prenom', 'dossard', 'email')
    readonly_fields = ('dossard', 'position_generale', 'position_par_categorie')
    list_editable = ('temps_course',)

    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom','sexe', 'email', 'date_naissance', 'course', 'temps_course','repas','club')
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