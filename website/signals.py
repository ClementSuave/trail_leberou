from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Benevole

@receiver(post_save, sender=Benevole)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:  # Only send on the first save
        subject = f"TRAIL DU LEBEROU - Confirmation d'inscription en tant que bénévole"
        message = f"Bonjour {instance.prenom},\n\nMerci de vous être inscrit comme bénévole pour notre course ! Nous reviendrons vers vous bientôt."
        from_email = 'contact@trailduleberou.fr'
        recipient_list = [instance.email]
        
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f"Erreur d'envoi d'email: {e}")