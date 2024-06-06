import os
from date_and_hour import date_and_time_now


def log(error, file):
    error = f"{date_and_time_now()} - {repr(error)}\n"

    # Verifica se o diretório existe, caso contrário, cria-o
    log_directory = os.path.dirname(file)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    with open(file, 'a', encoding='utf8') as log:
        log.write(error)


def csvlog(string, file):
    error = f"{date_and_time_now()},{string}\n"

    # Verifica se o diretório existe, caso contrário, cria-o
    log_directory = os.path.dirname(file)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    with open(file, 'a', encoding='utf8') as log:
        log.write(error)


def csvlog_header(header, file):
    error = f"Data,{header}\n"
    # Verifica se o diretório existe, caso contrário, cria-o
    log_directory = os.path.dirname(file)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    with open(file, 'w', encoding='utf8') as log:
        log.write(error)
