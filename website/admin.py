from django.contrib import admin
from .admin_filters import CategorieAgeFilter
from .models import Course, Coureur

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_course', 'distance', 'deniv')
    search_fields = ('nom',)
    list_filter = ('date_course',)
    empty_value_display = '-vide-'

@admin.register(Coureur)
class CoureurAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'sexe', 'dossard', 'course', 'club', 'temps_course', 'categorie_age', 'position_generale', 'position_par_categorie', 'telephone')
    list_filter = ('sexe','course',CategorieAgeFilter)
    search_fields = ('nom', 'prenom', 'dossard', 'email')
    readonly_fields = ('dossard', 'position_generale', 'position_par_categorie')
    list_editable = ('temps_course',)

    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom','sexe', 'email', 'date_naissance', 'course', 'temps_course')
        }),
        ('Informations de course calculées', {
            'fields': ('dossard', 'position_generale', 'position_par_categorie'),
            'classes': ('collapse',),
            'description': "Ces champs sont calculés automatiquement et ne peuvent pas être modifiés."
        }),
    )