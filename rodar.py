# JÁ TEM AS LIB 
# from configurador import instalar_bibliotecas
# instalar_bibliotecas()

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
    from gerar_csv_nome_proximo_email import gerar_csv_close_name

    import re
    from tkinter import Tk, filedialog, messagebox
    from difflib import SequenceMatcher

    from limpar_email import rodar_limpeza

except Exception as error:
    print('Erro ao importar biblioteca do Python: ', error)
    input('Digite qualquer coisa pra fechar.')

# -----------------------------------
# Ambiente de teste: 2.0
# -----------------------------------

# selecionar arquivo csv:
root = Tk()
root.withdraw()  
caminho_arquivo_selecionado = filedialog.askopenfilenames(title="Selecione o arquivo", filetypes=[("Arquivos de texto", "*csv *.xlsx")])
texto_caminho = str(caminho_arquivo_selecionado)
if '.csv' in texto_caminho:
    tipo = 'csv'
    caminho_arquivo_limpo = caminho_arquivo_selecionado[0].replace('.csv', '').split("/")
else:
    tipo = 'excel'
    caminho_arquivo_limpo = caminho_arquivo_selecionado[0].replace('.xlsx', '').split("/")
nome_arquivo = caminho_arquivo_limpo[-1]

arquivo_sujo = nome_arquivo + '_dados_sujos'
arquivo_limpo = nome_arquivo + '_dados_limpos'

# perguntas genéricas:
dados = perguntas()

# pegar dados no csv:
data_list = obter_objeto(dados['continuar_de_uma_pessoa_especifica'], caminho_arquivo_selecionado[0], tipo)

# Configurações para o Chrome em modo headless
if dados['na_tela'] == False:
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu") 
    driver = webdriver.Chrome(service=Service("./chromedriver.exe")  , options=chrome_options)
else:
    driver = webdriver.Chrome(service=Service("./chromedriver.exe"))

def incluir_dado(linha):
    with open(f'{arquivo_sujo}.csv', 'a', encoding='utf-8') as file:
        file.write(linha + "\n")

def texto_busca(pessoa): # 'a','b','c','d', 'contexto_adicional'
    if pessoa['a'] == None:
        coluna_a = ''
    else:
        coluna_a = pessoa['a']

    if pessoa['b'] == None:
        coluna_b = ''
    else:
        coluna_b = pessoa['b']

    if pessoa['c'] == None:
        coluna_c = ''
    else:
        coluna_c = pessoa['c']

    if pessoa['d'] == None:
        coluna_d = ''
    else:
        coluna_d = pessoa['d']

    if dados['contexto_adicional'] == None:
        contexto_adicional = ''
    else:
        contexto_adicional = dados['contexto_adicional']
    
    return f'"{pessoa['nome']}" {coluna_a} {coluna_b} {coluna_c} {coluna_d} {contexto_adicional}'
    
contador = 0
quantidade = len(data_list)
segundos = dados['tempo']

try:
    for index, pessoa in enumerate(data_list):

        localizado = False
        quantidade -= 1
        contador += 1

        if index == dados['limite']:
            print((f'Você bloqueou em {dados['limite']} pessoas: parou em {pessoa['nome']} '))
            inserir_no_log(f'Você bloqueou em {dados['limite']} pessoas: parou em {pessoa['nome']} ')
            break

        # Acessar o site
        driver.get('https://www.google.com.br')

        # aguardar:
        contador_segundos(segundos)

        # Localizar a barra de pesquisa (campo de entrada)
        search_box = driver.find_element(By.NAME, 'q')  # No Google, o campo de pesquisa tem o nome 'q'

        # Digitar texto no campo de pesquisa
        str_busca = texto_busca(pessoa)
        print(f'{quantidade} | Pagina 01 | {str_busca}')
        search_box.send_keys(f'{str_busca}')

        # Pressionar Enter
        search_box.send_keys(Keys.RETURN)

        contador_segundos(segundos)

        # Salvar o conteúdo HTML da página em uma variável
        html_content = driver.page_source

        contador_segundos(segundos)

        # Salva o conteúdo da página no arquivo
        html_content = driver.page_source        
 
        if 'detectaram tráfego incomum' in html_content:            
            inserir_no_log(f'Google detectou o robô bloqueou acessar a página. Parou na pessoa {pessoa['nome']}')
            break

        # Busca se encontra @ próximo ao nome e salva o index
        index_arrobas = []
        for index, letra in enumerate(html_content):
            if letra == '@':
                index_arrobas.append(index)

        # pega as strings +25 antes e depois do @:
        html_content = html_content.lower()
        resultados = []
        for index in index_arrobas:
            for nome in pessoa['nome'].lower().split(' '):
                if nome in html_content[index-25:index+25] and html_content[index-25:index+25] not in resultados and len(nome)>2:
                    localizado = True
                    resultados.append(html_content[index-25:index+25])

        # salva os resultados no csv de dados:
        if len(resultados) > 0:
            gerar_csv_close_name(pessoa['nome'], resultados, arquivo_sujo)

        # vai a pagina 02:
        contador_segundos(segundos)

        try:

            if localizado == False:

                pagina_02 = driver.find_element(By.XPATH, '//*[@id="botstuff"]/div/div[3]/table/tbody/tr/td[3]/a')
                pagina_02.click()

                print(f'{quantidade} | Pagina 02 | {str_busca}')

                # Busca se encontra @ próximo ao nome e salva o index
                index_arrobas = []
                for index, letra in enumerate(html_content):
                    if letra == '@':
                        index_arrobas.append(index)

                # pega as strings +25 antes e depois do @:
                html_content = html_content.lower()
                resultados = []
                for index in index_arrobas:
                    for nome in pessoa['nome'].lower().split(' '):
                        if nome in html_content[index-25:index+25] and html_content[index-25:index+25] not in resultados and len(nome)>2:
                            resultados.append(html_content[index-25:index+25])

                # salva os resultados no csv de dados:
                if len(resultados) > 0:
                    gerar_csv_close_name(pessoa['nome'], resultados, arquivo_sujo)

        except Exception as error:
            print(f'{quantidade} | Pagina 02 | Google sem segunda página - {pessoa['nome']} ')

except Exception as error:
    inserir_no_log('Erro ao rodar o sistema: ', error)
    input('Digite qualquer coisa pra fechar.')

try:
    # Criar um DataFrame - return: [quantidade_sujo, quantidade_limpo]
    arquivo_limpo_csv = f'{arquivo_limpo}.csv'
    arquivo_sujo_csv = f'{arquivo_sujo}.csv'
    quantidade = rodar_limpeza(arquivo_sujo_csv, arquivo_limpo_csv)
except Exception as error:
    print('Erro ao gerar CSV limpo: ',error)
    input('Digite qualquer coisa pra fechar.')   

pyautogui.alert(f'Total buscado: {contador}, sendo: \nQuantidades (sem tratamento): {quantidade[0]} \n(com tratamento) {quantidade[1]} \nNão limpos: {quantidade[2]}')