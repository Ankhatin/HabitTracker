import os
from threading import Lock, Thread

import telebot
from users.models import User


def run_telebot(lock: Lock):
    """
    Метод создает и запускает экземпляр бота Телеграм
    Бот постоянно находится в режиме ожидания активации бота пользователем
    путем ввода предопределенных команд ("/start", "/help")
    В этом случае бот находит данного пользователя в базе данных
    по его username в Телеграм и записывает в поле id_telegram актуальный
    id пользователя в системе Телеграм, для последующий отправки уведомлений
    :param lock:
    :return:
    """
    bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

    @bot.message_handler(commands=["start", "help"])
    def send_message(message):
        bot.reply_to(
            message,
            "Привет, это бот полезных привычек. "
            "Я буду уведомлять тебя о всех запланированных тобой привычках",
        )
        lock.acquire()
        if message.from_user.username:
            if User.objects.filter(tg_username=message.from_user.username).exists():
                current_user = User.objects.get(tg_username=message.from_user.username)
                if not current_user.tg_id:
                    current_user.tg_id = message.from_user.id
                current_user.save()
        lock.release()

    bot.polling(none_stop=True, interval=0)


def startup():
    """
    Метод вызывается при инициализации приложения,создает и запускает поток,
    в котором выполняется код взаимодействия телеграм бота с пользователем
    :return: None
    """
    lock = Lock()
    telethread = Thread(target=run_telebot, args=(lock,), daemon=True)
    telethread.start()


#
# def delete_tasks():
#     tasks = PeriodicTask.objects.exclude(id=1)
#     for task in tasks:
#         task.delete()
