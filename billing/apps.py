from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billing'


class BillingConfig(AppConfig):
    name = 'billing'

    def ready(self):
        # This ensures that the management commands can be found
        import billing.management.commands