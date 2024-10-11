from random import randint
from django.conf import settings
import smtplib
from email.mime.text import MIMEText


# проверка телефона на валидность
phone_pattern = r'^(\+7|8|7)\d{10}$'

# проверка email на валидность от пользователя
email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'


async def send_verification_email(user_email):
    verification_code = str(randint(100000, 999999))
    msg = MIMEText(
        f'Ваш проверочный код: {verification_code}', 'plain', 'utf-8')
    msg['Subject'] = 'Ваш проверочный код'
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = user_email

    # Подключение к серверу
    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.starttls()

    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Отправляем письмо
    try:
        server.sendmail(settings.DEFAULT_FROM_EMAIL,
                        user_email, msg.as_string())
    except Exception as e:
        print(f'Ошибка при отправке письма: {e}')
        return None

    server.quit()
    print(verification_code)
    return verification_code
