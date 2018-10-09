from django.apps import AppConfig


class GroupsConfig(AppConfig):
    name = 'entity'
    
    def ready(self):
        import entity.signals
