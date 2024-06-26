from django.apps import AppConfig


class ExpertAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expert_app'
    
    def ready(self):
        import expert_app.signals
