from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from django.apps import apps

# Este es un ejemplo de cómo usar señales para cargar modelos en el momento adecuado
@receiver(pre_migrate)
def cargar_modelos(sender, **kwargs):
    Persona = apps.get_model('login', 'Persona')
