import re
import os
import ast
import json
import time
import debug
import pickle
import traceback
import urllib.parse
import configparser
import pandas as pd
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

config = configparser.ConfigParser()
config.read('config.ini')
numbers = int(config['MESSAGES']['numbers'])
timeout = int(config['MESSAGES']['timeout'])
messages_files = ast.literal_eval(config['MESSAGES']['messages_file'])
file_path = config['SYSTEM']['file_path']
file_path_numbers = config['SYSTEM']['file_path_numbers']
xlsx_file = config['SYSTEM']['xlsx_file']
message_file = config['SYSTEM']['message_file']
position_file = config['SYSTEM']['position_file']
message_position_file = config['SYSTEM']['message_position_file']
log_path = config['SYSTEM']['log_path']


def update_position():
    # Verifica se o arquivo existe
    if os.path.exists(position_file):
        # Se existir, abre o arquivo em modo leitura e escrita binária
        with open(position_file, "rb+") as opened_file:
            # Carrega a posição atual do arquivo pickle
            position = pickle.load(opened_file)
            # Atualiza a posição e salva no arquivo
            opened_file.seek(0)
            pickle.dump(int(position) + 1, opened_file)
    else:
        # Se o arquivo não existir, cria um novo com o valor 0
        with open(position_file, "wb") as opened_file:
            pickle.dump(0, opened_file)
    opened_file.close()


def get_position():
    position = 0
    # Verifica se o arquivo existe
    if os.path.exists(position_file):
        # Se existir, abre o arquivo em modo leitura e escrita binária
        with open(position_file, "rb") as opened_file:
            position = pickle.load(opened_file)

    else:
        # Se o arquivo não existir, cria um novo com o valor 0
        with open(position_file, "wb") as opened_file:
            pickle.dump(0, opened_file)
    opened_file.close()
    return position


def message_reset_position():
    # Se o arquivo não existir, cria um novo com o valor 0
    with open(message_position_file, "wb") as opened_file:
        pickle.dump(0, opened_file)
    return 0


def message_update_position():
    # Verifica se o arquivo existe
    if os.path.exists(message_position_file):
        # Se existir, abre o arquivo em modo leitura e escrita binária
        with open(message_position_file, "rb+") as opened_file:
            # Carrega a posição atual do arquivo pickle
            position = pickle.load(opened_file)
            # Atualiza a posição e salva no arquivo
            opened_file.seek(0)
            pickle.dump(int(position) + 1, opened_file)
    else:
        # Se o arquivo não existir, cria um novo com o valor 0
        with open(message_position_file, "wb") as opened_file:
            pickle.dump(0, opened_file)
    opened_file.close()


def message_get_position():
    position = 0
    # Verifica se o arquivo existe
    if os.path.exists(message_position_file):
        # Se existir, abre o arquivo em modo leitura e escrita binária
        with open(message_position_file, "rb") as opened_file:
            position = pickle.load(opened_file)

    else:
        # Se o arquivo não existir, cria um novo com o valor 0
        with open(message_position_file, "wb") as opened_file:
            pickle.dump(0, opened_file)
    opened_file.close()
    return position


def execut_command(driver, xpath, command, key=None):
    while True:
        try:
            if command == 'find':
                driver.find_element("xpath", xpath)
            elif command == 'click':
                driver.find_element("xpath", xpath).click()
            elif command == 'send_keys':
                driver.find_element("xpath", xpath).send_keys(key)
            time.sleep(1)
            return

        except Exception as e:
            handle_exception(e, "execut_command")


def handle_exception(e, file):
    traceback_list = traceback.extract_tb(e.__traceback__)
    filename, line_number, function_name, code = traceback_list[-1]
    debug.log(e, f'{log_path}{file}.log')
    debug.log(
        f'O erro ocorreu na linha {line_number} do arquivo {filename}', f'{log_path}{file}.log')


def get_whatsapp_page(driver):
    driver.get('https://web.whatsapp.com')


def register(driver):
    while True:
        try:
            time.sleep(10)
            driver.find_element("xpath", '//*[@id="pane-side"]')
            return

        except Exception as e:
            handle_exception(e, 'wa_login')


def driver_config():
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "cache", "profile", "wpp")
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir={}".format(profile))
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--app=https://web.whatsapp.com")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def format_phone_number(phone_number):
    phone_number = str(phone_number)
    if not phone_number or not bool(phone_number.strip()):
        return False

    phone_number = ''.join(filter(str.isdigit, phone_number))

    if len(phone_number) == 12:
        if phone_number[4] in ['8', '9']:
            phone_number = f'{phone_number[:4]}9{phone_number[4:]}'
    elif len(phone_number) == 11:
        phone_number = f'55{phone_number}'
    elif len(phone_number) == 10:
        if phone_number[2] in ['8', '9']:
            phone_number = f'55{phone_number[:2]}9{phone_number[2:]}'
        else:
            phone_number = f'55{phone_number}'
    elif len(phone_number) == 9:
        phone_number = f'5551{phone_number}'
    elif len(phone_number) == 8:
        if phone_number.startswith(("8", "9")):
            phone_number = f'55519{phone_number}'
        else:
            phone_number = f'5551{phone_number}'

    return phone_number


def analyze_list():
    numbers_dict = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as open_file:
            numbers_dict = json.load(open_file)

    df = pd.read_excel(xlsx_file)
    list_number_xls = df['TELEFONE'].tolist()
    name_xls = df['NOME'].tolist()

    for i, phone_number in enumerate(list_number_xls):
        organized_number = format_phone_number(phone_number)

        if organized_number and organized_number not in numbers_dict:
            names = name_xls[i].strip().split(' ')
            first_name = names[0].lower().capitalize() if names else ""
            print(f"Original: {name_xls[i]}, Processado: {first_name}")
            numbers_dict[organized_number] = first_name

    with open(file_path, "w") as open_file:
        json.dump(numbers_dict, open_file, indent=4)

    old_list_of_numbers = [{"number": number, "name": name}
                           for number, name in numbers_dict.items()]

    with open(file_path_numbers, "w") as open_file:
        json.dump(old_list_of_numbers, open_file, indent=4)


def start_whatsapp(driver):
    # update_position()
    print('Lendo lista de destinatários...')
    with open(file_path_numbers, "r") as opened_file:
        list_of_recipients = json.load(opened_file)

    position = get_position()
    for recipient_position in range(position, len(list_of_recipients)):
        recipient = list_of_recipients[recipient_position]
        print(recipient['name'])
        debug.log(
            f"Enviando mensagem para {recipient['name']}, número {recipient['number']}, posição {recipient_position}", f'{log_path}message_status.log')


        msg_position = message_get_position()
        if msg_position == len(messages_files):
            msg_position = message_reset_position()

        for msg_position_for in range(msg_position, len(messages_files)):
            msg_file = messages_files[msg_position_for]
            msg = ''
            with open(msg_file, 'r', encoding='utf8') as msg_file_opened:
                msg = msg_file_opened.read()

            response = send_message(driver, recipient, msg, position)
            message_update_position()

            result = 'Falha'
            if response:
                debug.log(
                    f"sucesso ao enviar mensagem {msg_file}", f'{log_path}message_status.log')
                result = 'Sucesso'
                time.sleep(timeout)
            else:
                debug.log(
                    f"Erro ao enviar mensagem {msg_file}", f'{log_path}message_status.log')
                result = 'Falha'

            debug.csvlog(
                f"{recipient_position},{recipient['number']},{recipient['name']},{msg_file},{result}", f'{log_path}result.csv')
            if msg_position_for == len(messages_files):
                message_reset_position()
        update_position()


'''
1 - carregar arquivo json com nome numero de telefones
2 - começar a ler a lista apartir da ultima posição
3 - mandar para função que envia mensagem
4 - marcar no json se aquele objeto já teve suas mensagens enviadas
'''


def send_message(driver, contact, message, conte):
    number = contact['number']
    name = contact['name']

    new_msg = str(message).replace('{nome}', name)

    new_msg = urllib.parse.quote(new_msg)

    print(f'Enviando mensagem para {name}, número {number}, posição {conte}')

    message_url = F'https://web.whatsapp.com/send?phone={number}&text={new_msg}'

    driver.get(message_url)

    debug.log(
        message_url, f'{log_path}message_url.log')

    try:
        alert = WebDriverWait(driver, 30).until(EC.alert_is_present())
        alert.dismiss()

    except Exception as e:
        handle_exception(e, "send_message")

    execut_command(
        driver=driver, xpath='/html/body/div[1]/div/div/div[2]/div[3]/header', command='find')

    try:
        driver.find_element(
            "xpath", "/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div")
        return False

    except Exception as e:
        handle_exception(e, "send_message")

    execut_command(
        driver=driver, xpath='/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button', command='click')
    return True


if __name__ == '__main__':
    debug.csvlog_header(f"ID,Numero,Nome,Mensagem,status",
                        f'{log_path}result.csv')
    print('Analisando lista de destino')
    analyze_list()
    print('Lista de destino analisada')
    driver = driver_config()
    print('Registrando')
    register(driver)
    print('Registrado')
    print('Iniciando envio de mensagens')
    start_whatsapp(driver)
    driver.quit()
