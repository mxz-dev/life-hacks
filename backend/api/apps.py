from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    # comment if you want to use the tests in the api app 🔻
    # def ready(self):
    #     import api.signals
