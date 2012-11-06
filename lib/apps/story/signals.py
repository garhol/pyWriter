from django.models.signals import pre_save
from django.dispatch import receiver
from .models import Character, Scene


@receiver(pre_save, Scene)
def create_narrator(instance, **kwargs):
    if not instance.pk:
        narrator, created = Character.objects.get_or_create(user=user, firstname='John', nicknames='Narrator')
        if not instance.perspective:
            instance.perspective = narrator
    

