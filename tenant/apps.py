from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tenant'
    verbose_name = _('Gestión de Clientes')
