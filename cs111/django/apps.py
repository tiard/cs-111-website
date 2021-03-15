from django.apps import AppConfig

class CS111Config(AppConfig):
    name = 'cs111.django'
    verbose_name = 'CS 111'
    label = 'cs111'

    def ready(self):
        import cs111.django.signals
