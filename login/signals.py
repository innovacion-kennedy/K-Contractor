# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from .models import Persona

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def crear_perfil_persona(sender, instance, created, **kwargs):
#     if created:
#         if not hasattr(instance, 'perfil'):
#             Persona.objects.create(usuario=instance)
