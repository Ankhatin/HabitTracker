from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from good_habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для работы с данными модели Habit
    """

    def validate(self, attrs):
        """
        Метод проверяет поля экземпляра habit при его создании или обновлении
        на соответствие требованиям
        :param attrs: словарь значений полей
        :return attrs: словарь проверенных значений
        """
        bound_habit = None
        reward = None
        time_to_perform = None
        is_pleasure = None
        frequency = None
        """Если происходит обновление данных экземпляра (методы 'PUT', 'PATCH')
        отсутствующие значения полей получаем из объекта в базе данных"""
        if self.instance:
            bound_habit = getattr(self.instance, "bound_habit")
            reward = getattr(self.instance, "reward")
            time_to_perform = getattr(self.instance, "time_to_perform")
            is_pleasure = getattr(self.instance, "is_pleasure")
            frequency = getattr(self.instance, "frequency")
        """Если в контроллер передаются указанные свойства
        перезаписываем переменные их значениями"""
        if attrs.get("bound_habit"):
            bound_habit = attrs.get("bound_habit")
        if attrs.get("reward"):
            reward = attrs.get("reward")
        if attrs.get("time_to_perform"):
            time_to_perform = attrs.get("time_to_perform")
        if attrs.get("is_pleasure"):
            is_pleasure = attrs.get("is_pleasure")
        if attrs.get("frequency"):
            frequency = attrs.get("frequency")
        # Производим валидацию переданных данных
        if bound_habit and reward:
            raise ValidationError(
                "You cannot set field <bound_habit> and <reward> concurrently"
            )
        if bound_habit:
            if not bound_habit.is_pleasure:
                raise ValidationError(
                    "Bound habit must be with set attribute <is_pleasure"
                )
        if is_pleasure:
            if bound_habit or reward:
                raise ValidationError(
                    "Pleasure habit must not have bound habit or reward"
                )
        if time_to_perform > 120:
            raise ValidationError("Time to perform action must be up to 120 seconds")
        if frequency > 7:
            raise ValidationError(
                "You cannot perform action less often then one time at 7 days"
            )
        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
