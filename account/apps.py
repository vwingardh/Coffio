from django.apps import AppConfig
import os
from django.conf import settings


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    path = os.path.join(settings.BASE_DIR, 'account')
