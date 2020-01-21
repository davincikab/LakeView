from django.apps import AppConfig


class CitizensConfig(AppConfig):
    name = 'citizens'
    
    def ready(self):
        import citizens.signals
