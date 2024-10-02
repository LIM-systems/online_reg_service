from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+7\d{10}$',
    message='Номер должен быть в формате +79001112233')
email_regex = RegexValidator(
    regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
    message='Введите корректный адрес электронной почты'
)

START_WORK_TIME_DEFAULT = '10:00:00'
END_WORK_TIME_DEFAULT = '21:00:00'
