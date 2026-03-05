from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Benevole

@receiver(post_save, sender=Benevole)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = f"TRAIL DU LEBEROU - Confirmation d'inscription en tant que bénévole"
        
        context = {
            'prenom': instance.prenom,
        }
        
        html_message = render_to_string('emails/confirmation_benevole.html', context)
        plain_message = strip_tags(html_message)
        
        from_email = 'contact@trailduleberou.fr'
        to = [instance.email]

        send_mail(
            subject, 
            plain_message, 
            from_email, 
            to, 
            html_message=html_message,
            fail_silently=False
        )