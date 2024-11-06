import sys

from django.apps import AppConfig


class GoodHabitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "good_habit"

    def ready(self):
        if "runserver" in sys.argv:
            from .services import startup

            startup()
        # elif 'worker' in sys.argv:
        #     from .services import delete_tasks
        #     delete_tasks()
