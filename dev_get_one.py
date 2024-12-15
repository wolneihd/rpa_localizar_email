try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from contador import contador_segundos
    import pandas as pd
    import pyautogui
    from gerar_json import obter_objeto
    from perguntas import perguntas
    import os
    from gerar_logs import inserir_no_log
except Exception as error:
    print('Erro ao importar biblioteca do Python: ', error)
    input('Digite qualquer coisa pra fechar.')

# -----------------------------------
# código para teste
# -----------------------------------

driver = webdriver.Chrome(service=Service("./chromedriver.exe"))

def incluir_dado(linha):
    with open(f'dev_get_one.csv', 'a', encoding='utf-8') as file:
        file.write(linha + "\n")

driver.get('https://www.google.com.br')

contador_segundos(2)

search_box = driver.find_element(By.NAME, 'q')

texto_buscar = f'"VIVIANE COLARES SOARES DE ANDRADE AMORIM" DPTO CLINICA E ODONTOL PREVENTIVA - CCS    contato mail'

search_box.send_keys(texto_buscar)

search_box.send_keys(Keys.RETURN)

contador_segundos(2)

html_content = driver.page_source

with open(f'resposta.txt', 'a', encoding='utf-8') as file:
    file.write(html_content)

index_arrobas = []
for index, letra in enumerate(html_content):
    if letra == '@':
        index_arrobas.append(index)

html_content = html_content.lower()
resultados = []
for index in index_arrobas:
    for nome in texto_buscar.lower().split(' '):
        if nome in html_content[index-25:index+25] and html_content[index-25:index+25] not in resultados and len(nome) > 2:
            resultados.append(html_content[index-25:index+25])
            
for respostas in resultados:
    print(respostas)

try:
    pagina_02 = driver.find_element(By.XPATH, '//*[@id="botstuff"]/div/div[3]/table/tbody/tr/td[3]/a')
    pagina_02.click()
except:
    print('pagina 2 não localizada')