from django.apps import AppConfig


class bookinventeryConfig(AppConfig):
    name = 'bookinventery'

    def ready(self):
        from bookinventery import signals
