from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class CategorieAgeFilter(admin.SimpleListFilter):
    
    title = _('Catégorie')
    parameter_name = 'categorie_age_filter'

    def lookups(self, request, model_admin):
       
        categories = [
            ("ES Homme", "ES Homme"),
            ("ES Femme", "ES Femme"),
            ("SE Homme", "SE Homme"),
            ("SE Femme", "SE Femme"),
            ("MA Homme", "MA Homme"),
            ("MA Femme", "MA Femme"),
        ]
        
        return categories

    def queryset(self, request, queryset):
        if self.value():
           
            coureur_ids = []
            for coureur in queryset:
                if coureur.categorie_age() == self.value():
                    coureur_ids.append(coureur.id)
            
            return queryset.filter(id__in=coureur_ids)
            
        return queryset
