from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
#from .tasks import scrape_dev_to


class CryptobrechaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cryptobrecha'

 