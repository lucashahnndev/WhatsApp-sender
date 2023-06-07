import os
import json
import time
import urllib.parse
import debug

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unidecode import unidecode
from webdriver_manager.chrome import ChromeDriverManager

log_path = "logs/"  # Substitua pelo caminho correto

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
        except:
            pass

def get_whatsapp_page(driver):
    driver.get('https://web.whatsapp.com')

def register(driver):
    while True:
        try:
            time.sleep(10)
            driver.find_element("xpath", '//*[@id="pane-side"]')
            return
        except:
            pass

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

def send_message(driver, contact, message, conte):
    number = contact['number']
    name = contact['name']

    new_msg = str(message).replace('{nome}', name)
    new_msg = urllib.parse.quote(new_msg)
    print(f'Enviando mensagem para {name}, número {number}, posição {conte}')
    driver.execute_script(
        f"window.location.href = 'https://web.whatsapp.com/send?phone={number}&text={new_msg}'")

    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.dismiss()
    except:
        pass

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_3ndVb")))

    try:
        driver.find_element("xpath", '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]').click()
        debug.log(f'error in number {number} id {conte}', 'logs/error_list.txt')
        return False
    except:
        pass

    execut_command(driver=driver, xpath='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p', command='click')
    execut_command(driver=driver, xpath='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p', command='send_keys', key=Keys.ENTER)
    debug.log(f'success in number {number} id {conte}', f'{log_path}log.log')
    return True

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

def start_whatsapp(driver):
    file_path = "cache/number_list.json"
    file_path_numbers = "cache/numbers.json"
    xlsx_file ='Pasta.xlsx'
    message_file = "message.txt"
    position_fle = 'cache/number_position'


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
            numbers_dict[organized_number] = name_xls[i].split(' ')[0].lower().capitalize()

    with open(file_path, "w") as open_file:
        json.dump(numbers_dict, open_file)

    old_list_of_numbers = [{"number": number, "name": name} for number, name in numbers_dict.items()]

    with open(file_path_numbers, "w") as open_file:
        json.dump(old_list_of_numbers, open_file)

    with open(message_file, 'r', encoding='utf8') as msg_file:
        msg =msg_file.read()


    number_list_position = 0
    if os.path.exists(position_fle):
        with open(position_fle, 'r') as position_file:
            number_list_position = int(position_file.read()) +1

    for conte in range(number_list_position, len(old_list_of_numbers)):
        send_message(driver, old_list_of_numbers[conte], msg, conte)

        with open(position_fle, 'w', encoding='utf8') as position_file:
            position_file.write(str(conte))

    driver.quit()

if __name__ == '__main__':
    driver = driver_config()
    print('registrando')
    register(driver)
    print('registrado')
    print('Iniciando envio de mensagens')
    start_whatsapp(driver)
