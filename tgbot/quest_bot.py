# -*- coding: utf-8 -*-

"""Головная логика бота."""
import telebot
from telebot import types
import logging
import random
import string
import time
import smtplib
import re
from typing import Iterable, Optional

from tgbot.models import Favourite, Poem, User

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger('default')


class Questionnaire:
    allowed_domains = ['syssoft.ru']
    admin_emails = {'a.novoseltsev@syssoft.ru': 'active', 'askerov@syssoft.ru': 'inactive'}
    user_email = {}
    codes = {}
    times = {}

    def __init__(self, user: User):
        self.user = user

    def send_poll(chat_id):
        for user_id in registered_users:
            try:
                # Отправка рассылки
                question1 = "1: Состоялась встреча?"
                options1 = ["Да", "Нет"]
                question2 = "2: Как все прошло?"
                options2 = ["Хорошо", "Плохо"]
                question3 = "3: На следующей неделе участвуешь?"
                options3 = ["Да", "Нет"]

                poll = Questionnaire.bot.send_poll(chat_id, question1, options1, is_anonymous=False)
                Questionnaire.bot.send_poll(chat_id, question2, options2, is_anonymous=False,
                                       reply_to_message_id=poll.message_id)
                Questionnaire.bot.send_poll(chat_id, question3, options3, is_anonymous=False,
                                       reply_to_message_id=poll.message_id)
            except Exception as e:
                logging.error(f"Ошибка отправки рассылки пользователю: {user_id} ({Questionnaire.get_full_name(user_id)}) ({time.asctime()}): {str(e)}")
            # Ожидание ответа пользователя
            time.sleep(5)
            # Получение ответа пользователя на последний вопрос
            last_answer = Questionnaire.bot.poll_answer_handlers[-1].last_answer
            # Проверка ответа на последний вопрос
            if last_answer and last_answer.user.id == user_id:
                if last_answer.option_ids[0] == 1:
                    # Обработка ответа "Нет"
                    # Удаление пользователя из списка зарегистрированных
                    Questionnaire.user_email.pop(user_id, None)
                    logging.info(f"Пользователь {user_id} ({Questionnaire.get_full_name(user_id)}) удален из списка зарегистрированных пользователей ({time.asctime()})")

    # Обработка ответов на опрос
    def handle_poll_answer(poll_answer):
        # Отправляем сообщение с результатами опроса
        Questionnaire.bot.send_message(poll_answer.user.id, "Спасибо за ваш ответ! Результаты опроса:")
        for option in poll_answer.option_ids:
            Questionnaire.bot.send_message(poll_answer.user.id, f"{option=}")

    # Обработка рассылки
    def start_newsletter(message):
        # Запускаем рассылку каждую пятницу в 17:00
        schedule.every().friday.at("17:00").do(Questionnaire.send_poll, Questionnaire.chat_id)

        # Цикл для выполнения расписания
        while True:
            schedule.run_pending()
            time.sleep(1)
