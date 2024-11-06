from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):

    place = models.CharField(max_length=100, verbose_name="Место", **NULLABLE)
    first_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата первого выполнения",
        help_text="Укажите дату первого выполнения привычки",
        **NULLABLE,
    )
    time_of_action = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Время выполнения привычки",
        help_text="Укажите время выполнения привычки в секундах",
        **NULLABLE,
    )
    action = models.CharField(max_length=200, verbose_name="Действие")
    is_pleasure = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    bound_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Укажите приятную привычку",
        **NULLABLE,
    )
    frequency = models.SmallIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Укажите периодичность выполнения привычки в днях",
    )
    reward = models.CharField(max_length=200, verbose_name="Вознаграждение", **NULLABLE)
    time_to_perform = models.SmallIntegerField(
        default=120,
        verbose_name="Время на выполнение",
        help_text="Укажите время на выполнение в секундах",
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_habits",
        verbose_name="Пользователь",
    )

    def __str__(self):
        return f"Действие: {self.action} - Место: {self.place} - Время: {self.time_of_action}"

    class Meta:
        verbose_name = "Полезная привычка"
        verbose_name_plural = "Полезные привычки"
        ordering = ["owner"]
