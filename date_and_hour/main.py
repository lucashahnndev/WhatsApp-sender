import time
from datetime import datetime
def date_and_time():
    return datetime.now()


def date_now():
    str_hora = date_and_time().strftime("%d/%m/%y")
    return str_hora


def time_now():
    str_hora = date_and_time().strftime("%H:%M")
    return str_hora


def hour_now():
    str_hora = date_and_time().strftime("%H")
    return str_hora


def date_and_time_now():
    str_hora = date_and_time().strftime("%d/%m/%Y %H:%M")
    return str_hora

def month():
    str_month = date_and_time().strftime("%m")
    return str_month

def day():
    str_hora = date_and_time().strftime("%d")
    return str_hora


def year():
    str_hora = date_and_time().strftime("%y")
    return f'20{str_hora}'


def minutes():
    str_hora = date_and_time().strftime("%M")
    return str_hora


hour = hour_now()


def shift():
    if hour > '0' and hour < '07':
        return 'Madrugada'

    if hour > '06' and hour < '13':
        return 'Manhã'

    if hour > '12' and hour < '19':
        return 'Tarde'

    if hour > '18' and hour < '24' and hour > '00':
        return 'Noite'
