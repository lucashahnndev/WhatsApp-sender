""" from PyQt5.QtGui import QIcon

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog """
import re
import os
import time

import debug
import pickle
import traceback
import pandas as pd
import urllib.parse
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

log_path = 'logs/'
list_file = 'Pasta.xlsx'
file_path = 'cache/number.pkl'
message_file = 'message.txt'

numeros_organizados = []
list_numbers_anterior = []


def execut_command(driver=None, xpath=None, command=None, key=None):
    while True:
        try:
            if command == 'find':
                driver.find_element("xpath", xpath)
            if command == 'click':
                driver.find_element("xpath", xpath).click()
            if command == 'send_keys':
                driver.find_element( "xpath", xpath).send_keys(key)

            time.sleep(1)
            return
        except:
            pass


def get_QRCode(driver):
    qr_code_element = driver.find_element("xpath", '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div')
    qr_code_element.screenshot('qr_code.png')
    print('QR Code saved as qr_code.png')
    return 'qr_code.png'


def get_whatsapp_page(driver):
    driver.get(f'https://web.whatsapp.com')

def register(driver):
    while True:
        try:
            driver.find_element("xpath",'/html/body')
            return
        except:
            pass


def driver_config():
    dir_path = os.getcwd()
    profile = os.path.join(dir_path,"cache", "profile", "wpp")
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir={}".format(profile))
    options.add_argument("--disable-infobars")  # desabilita a barra de informações do Chrome
    options.add_argument("--disable-extensions")  # desabilita as extensões do Chrome
    options.add_argument("--disable-gpu")  # desabilita o uso da GPU para renderização
    options.add_argument("--disable-dev-shm-usage")  # desabilita o uso compartilhado de memória /tmp
    options.add_argument("--no-sandbox")  # desabilita o uso do sandbox de segurança do Chrome
    options.add_argument("--disable-blink-features=AutomationControlled")  # remove a mensagem de aviso
    options.add_argument("--app=https://web.whatsapp.com")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver




def send_message(number, msg, conte):
    driver.execute_script(
        f"window.location.href = `https://web.whatsapp.com/send?phone={number}&text={msg}` ")  # Abre segunda guia

    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.dismiss()
    except:
        pass

    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_3ndVb")))

    time.sleep(5)



    try:
        driver.find_element(
            "xpath", '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]').click()
        debug.log(f'error in number {number} id {conte}',
                  'error_list.txt')
        return
    except:
        pass

    execut_command(driver=driver, xpath='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p', command='click')
    execut_command(driver=driver, xpath='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p', command='send_keys', key=Keys.ENTER)
    debug.log(
        f'sucess in number {number} id {conte}', f'{log_path}log.log')
    return True


def format_phone_number(phone_number):
    phone_number = re.sub(r'[^0-9]', '', phone_number)
    if phone_number == ' ' or phone_number == ''  or phone_number == None:
        return False
    if len(phone_number) == 12:
        if phone_number[4] == '8' or phone_number[4] == '9':
            phone_number = f'{phone_number[:4]}9{phone_number[4:]}'

    if len(phone_number) == 11:
        phone_number = f'55{phone_number}'

    if len(phone_number) == 10:
        if phone_number[2] == '8' or phone_number[2] == '9':
            phone_number = f'55{phone_number[:2]}9{phone_number[2:]}'
        else:
            phone_number = f'55{phone_number}'

    if len(phone_number) == 9:
        phone_number = f'5551{phone_number}'
    if len(phone_number) == 8:
        if phone_number.startswith("8") or phone_number.startswith("9"):
            phone_number = f'55519{phone_number}'
        else:
            phone_number = f'5551{phone_number}'

    return phone_number


def start_whatsapp(driver):
    try:
        if os.path.exists(file_path):
            open_file = open(file_path, "rb")
            list_numbers_anterior = pickle.load(open_file)
            open_file.close()

        df = pd.read_excel(list_file)
        list_number_xls = df['TELEFONE'].tolist()

        for i in list_number_xls:
            nummber_row = str(i)
            nummber_row_list = nummber_row.split('/')
            for cont in nummber_row_list:
                nummber_row_list_space = cont.split('&')
                for phone_number in nummber_row_list_space:
                    numero_organizado = format_phone_number(phone_number)
                    if numero_organizado:
                        if numero_organizado not in numeros_organizados:
                            numeros_organizados.append(numero_organizado)

        list_numbers_anterior = numeros_organizados

        open_file = open(file_path, "wb")
        pickle.dump(numeros_organizados, open_file)
        open_file.close()

        msg_file = open(message_file, 'r', encoding='utf8')
        msg = msg_file.read()
        msg = urllib.parse.quote(msg)

        for conte in range(len(list_numbers_anterior)):
            if os.path.exists('cache/number_list_position.txt'):
                number_list_position = open('cache/number_list_position.txt', 'r')
                number_list_position = number_list_position.read()
                conte = int(number_list_position) + 1
            send_message(list_numbers_anterior[conte], msg, conte)

            with open('cache/number_list_position.txt', 'w', encoding='utf8') as position_file:
                position_file.write(str(conte))

        driver.quit()
    except Exception as error:
        traceback_list = traceback.extract_tb(error.__traceback__)
        filename, line_number, function_name, code = traceback_list[-1]
        debug.log(error, f'{log_path}error.log')
        debug.log(
            f'O erro ocorreu na linha {line_number} do arquivo {filename}', f'{log_path}error.log')


"""
class WhatsAppSender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WhatsApp Sender')
        self.setWindowIcon(QIcon('image/logo.ico'))
        self.initUI()
        self.driver = driver_config()
        get_whatsapp_page(self.driver)



    def initUI(self):

        self.qr_code = QLabel(self)
        self.qr_code.move(20, 5)
        self.qr_code.resize(400, 400)
        self.qr_code.setPixmap(QtGui.QPixmap('qr_code.png'))


        self.label = QLabel('Selecione o arquivo xlsx:')
        self.label.move(20, 20)
        self.label.resize(200, 20)

        self.btn_file = QPushButton('Selecionar arquivo', self)
        self.btn_file.move(20, 50)
        self.btn_file.resize(100, 30)
        self.btn_file.clicked.connect(self.select_file)

        self.btn_start = QPushButton('Start', self)
        self.btn_start.move(20, 100)
        self.btn_start.resize(100, 30)

        self.btn_pause = QPushButton('Pause', self)
        self.btn_pause.move(140, 100)
        self.btn_pause.resize(100, 30)
        #exibir uma imagem do qr code


    def whatsapp_register(self):
        pass

    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Selecionar arquivo', '', 'Arquivo XLSX (*.xlsx)')
        if filename:
            print(f'Selecionado o arquivo: {filename}')
 """

""" if __name__ == '__main__':
    app = QApplication([])
    window = WhatsAppSender()
    window.show()
    app.exec_()
 """


if __name__ == '__main__':
    driver = driver_config()
    print('registrando')
    register(driver)
    print('registrado')
    print('Iniciando envio de mensagens')
    start_whatsapp(driver)
