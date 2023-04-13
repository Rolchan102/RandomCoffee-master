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


class Registration:
    allowed_domains = ['syssoft.ru']
    admin_emails = {'a.novoseltsev@syssoft.ru': 'active', 'askerov@syssoft.ru': 'inactive'}
    user_email = {}
    codes = {}
    times = {}

    def __init__(self, user: User):
        self.user = user

    def register_email(message):
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        logging.info(f'{user_id} {user_full_name} {time.asctime()}')
        # Если пользователь только начал общение с ботом, отправляем ему сообщение с просьбой указать свой адрес почты
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        Registration.bot.send_message(message.from_user.id,
                                      f"Привет, {user_full_name}! Укажите свой адрес электронной почты",
                                      reply_markup=markup)

    def check_email(message):
        if message.text.split("@")[-1] not in Registration.allowed_domains:
            Registration.bot.send_message(message.from_user.id, "Домен не разрешен для регистрации!")
            domain_unsuccess = "Домен не разрешен для регистрации!"
            user_id = message.from_user.id
            user_full_name = message.from_user.full_name
            logging.error(f'Пользователь: {user_id} {user_full_name}, '
                          f'Регистрация: {domain_unsuccess}, '
                          f'{time.asctime()}')
            return
        Registration.user_email = message.text.lower()
        if Registration.user_email in Registration.admin_emails and Registration.admin_emails[Registration.user_email] == "active":
            Registration.bot.send_message(message.from_user.id,
                                      "По вашему адресу отправлен код подтверждения, проверьте почту и введите код")
            Registration.send_email(Registration.user_email)
        else:
            Registration.bot.send_message(message.from_user.id,
                                      "Адрес не активен!")
            email_unsuccess = "Адрес не активен!"
            user_id = message.from_user.id
            user_full_name = message.from_user.full_name
            logging.error(f'Пользователь: {user_id} {user_full_name}, '
                          f'Регистрация: {email_unsuccess}, '
                          f'{time.asctime()}')
            return

    def check_code(message):
        if Registration.times[Registration.user_email] + 1200 < time.time():
            Registration.bot.send_message(message.chat.id, "Время жизни кода истекло. Попробуйте еще раз.")
            code_unsuccess = "Код истёк!"
            user_id = message.from_user.id
            user_full_name = message.from_user.full_name
            logging.error(f'Пользователь: {user_id} {user_full_name}, '
                          f'Регистрация: {code_unsuccess}, '
                          f'{time.asctime()}')
            return
        if Registration.codes[Registration.user_email] == message.text:
            Registration.bot.send_message(message.chat.id,
                                      "Поздравляем! Вы зарегистрированы. Правила использования бота вы можете найти в нашем канале @syssoft_random_coffee_bot.")
            result_success = "Регистрация прошла успешно!"
            user_id = message.from_user.id
            user_full_name = message.from_user.full_name
            logging.info(f'Пользователь: {user_id} {user_full_name}, '
                         f'Регистрация: {result_success}, '
                         f'{time.asctime()}')
        else:
            Registration.bot.send_message(message.chat.id, "Неверный код подтверждения")
            result_unsuccess = "Неверный код подтверждения!"
            user_id = message.from_user.id
            user_full_name = message.from_user.full_name
            logging.error(f'Пользователь: {user_id} {user_full_name}, '
                          f'Регистрация: {result_unsuccess}, '
                          f'{time.asctime()}')

    @staticmethod
    def send_email(user_email):
        """Генерирует код и отправляет пользователю на почту"""
        # Генерируем случайный код подтверждения
        code = ''.join(random.choice(string.digits) for _ in range(6))
        # Запоминаем код в словаре codes
        Registration.codes[user_email] = code
        # Запоминаем время отправки кода в словаре times
        Registration.times[user_email] = time.time()

        smtp_username = "novosltsev2010@gmail.com"
        smtp_password = "uvxhzvmfpvdhkhoo"

        smtp_conn = smtplib.SMTP('smtp.gmail.com: 587')
        smtp_conn.starttls()
        smtp_conn.login(smtp_username, smtp_password)

        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = user_email
        message['Subject'] = 'Код подтверждения'

        # Отправляем код на почту пользователя
        code_message = f"Код подтверждения: {code}. Введите его в боте для подтверждения регистрации."
        message.attach(MIMEText(code_message, 'plain'))
        smtp_conn.sendmail(smtp_username, user_email, message.as_string())
        smtp_conn.quit()
