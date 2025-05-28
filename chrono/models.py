from django.db import models

class coureur(models.Model):
	heure_arrivee = models.DateField(null=True)
	nom = models.TextField(blank=True,null=True)
	prenom = models.TextField(blank=True,null=True)
	dossard = models.IntegerField(blank=True,null=True)

	class Meta:
		verbose_name = "Coureur"
		ordering = ['heure_arrivee']
