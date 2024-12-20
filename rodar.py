try:
    import os
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("O módulo 'bs4' não está instalado. Instalando agora...")
        os.system("pip install beautifulsoup4")
        from bs4 import BeautifulSoup

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
    from gerar_logs import inserir_no_log
    from gerar_csv_nome_proximo_email import gerar_csv_close_name

    import re
    from difflib import SequenceMatcher
    from tkinter import Tk, filedialog

    from buscador import get_data_buscador
    from limpar_email import rodar_limpeza
    from acao_pagina import digitar, rolar_pagina, aceitar_termos_bing, aceitar_termos_yahoo

except Exception as error:
    print('Erro ao importar biblioteca do Python: ', error)
    input('Digite qualquer coisa pra fechar.')

# -----------------------------------
# Versão Final 1.0
# -----------------------------------

# Selecionar arquivo CSV:
root = Tk()
root.withdraw()
caminho_arquivo_selecionado = filedialog.askopenfilenames(title="Selecione o arquivo", filetypes=[("Arquivos de texto", "*.csv *.xlsx")])
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

# Perguntas genéricas:
dados = perguntas()

# Pegar dados no CSV:
data_list = obter_objeto(dados['continuar_de_uma_pessoa_especifica'], caminho_arquivo_selecionado[0], tipo)

def gerar_driver():
    # Configurações para o Chrome em modo headless:
    if not dados['na_tela']:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        return webdriver.Chrome(service=Service("./chromedriver.exe"), options=chrome_options)
    # Configurações para o Chrome em modo aberto:
    else:
        return webdriver.Chrome(service=Service("./chromedriver.exe"))

def incluir_dado(linha):
    with open(f'{arquivo_sujo}.csv', 'a', encoding='utf-8') as file:
        file.write(linha + "\n")

def texto_busca(pessoa):
    contexto_adicional = dados.get('contexto_adicional', '') or ''
    partes_busca = [f'"{pessoa["nome"]}"']
    
    # Adiciona somente colunas que tenham valores
    for coluna in ['a', 'b', 'c', 'd']:
        valor = pessoa.get(coluna)
        if valor:  # Ignora valores vazios ou None
            partes_busca.append(valor)
    
    if contexto_adicional:
        partes_busca.append(contexto_adicional)
    
    return ' '.join(partes_busca)

def limpar_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def encontrar_emails(html, pessoa):
    nome = pessoa['nome'].lower()
    palavras_nome = nome.split()

    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
    emails_similares = []

    for email in emails:
        nome_local = email.split('@')[0]
        similaridade = max(SequenceMatcher(None, nome_local, palavra).ratio() for palavra in palavras_nome)
        if similaridade > 0.5:
            emails_similares.append(email)

    return emails_similares

# Dados para inicialização do loop for:
contador = 0
quantidade = len(data_list)
rodada = 0
driver = gerar_driver()
refresh = True
imprimir_tempo = False

try:
    for index, pessoa in enumerate(data_list):

        localizado = False
        quantidade -= 1
        contador += 1

        if index == dados['limite']:
            mensagem = f'Você bloqueou em {dados["limite"]} pessoas: parou em {pessoa["nome"]} '
            print(mensagem)
            inserir_no_log(mensagem)
            break

        if refresh:
            # Acessar o site
            site = get_data_buscador(dados['site'])
            driver.get(site['url'])

        # Aguardar:
        contador_segundos(imprimir_tempo)

        try:
            # Localizar a barra de pesquisa (campo de entrada)
            search_box = driver.find_element(By.NAME, site['campo_busca'])
        except:
            print(f'Erro ao buscar campo de busca: {dados['site']}')

        # aceitar termos do BING:
        if dados['site'] == 'Bing':
            aceitar_termos_bing(driver)
        if dados['site'] == 'Yahoo':
            aceitar_termos_yahoo(driver)

        # Digitar texto no campo de pesquisa
        str_busca = texto_busca(pessoa)
        print(f'{quantidade} | Pagina 01 - site: {dados['site']} | {str_busca}')
        digitar(search_box, str_busca)

        # Pressionar Enter
        search_box.send_keys(Keys.RETURN)

        contador_segundos(imprimir_tempo)

        # Salvar o conteúdo HTML da página em uma variável
        html_content = driver.page_source
        html_limpo = limpar_html(html_content)

        # Verificar bloqueio do Google
        if 'detectaram tráfego incomum' in html_content:
            inserir_no_log(f'Google detectou o robô e bloqueou o acesso. Parou na pessoa {pessoa["nome"]}')
            break

        rolar_pagina(driver)

        # Encontrar emails semelhantes ao nome da pessoa
        resultados = encontrar_emails(html_limpo, pessoa)

        # Salvar resultados no CSV
        if resultados:
            gerar_csv_close_name(pessoa['nome'], resultados, arquivo_sujo)

        # Tentativa de acessar página 2
        try:
            if not localizado:
                print(f'{quantidade} | Pagina 02 - site: {dados['site']} | {str_busca}')
                pagina_02 = driver.find_element(By.XPATH, site['xpath'])
                pagina_02.click()

                rolar_pagina(driver)
                contador_segundos(imprimir_tempo)

                html_content = driver.page_source
                html_limpo = limpar_html(html_content)
                resultados_pagina_2 = encontrar_emails(html_limpo, pessoa)

                if resultados_pagina_2:
                    gerar_csv_close_name(pessoa['nome'], resultados_pagina_2, arquivo_sujo)

        except Exception:
            print(f'{quantidade} | Pagina 02 site: {dados['site']} não localizado')
            refresh = True       

        try:
            search_delete = driver.find_element(By.XPATH, site['limpar_busca'])
            search_delete.click()
            refresh = False
        except Exception:
            print(f'Robô não conseguiu encontrar o campo "X" de limpar pesquisa. Tentando opção 02 - recarregar página do {dados['site']}')
            refresh = True    

except Exception as error:
    inserir_no_log(f'Erro ao rodar o sistema: {error}')
    input('Digite qualquer coisa pra fechar.')

try:
    # Criar um DataFrame - return: [quantidade_sujo, quantidade_limpo]
    arquivo_limpo_csv = f'{arquivo_limpo}.csv'
    arquivo_sujo_csv = f'{arquivo_sujo}.csv'
    quantidade = rodar_limpeza(arquivo_sujo_csv, arquivo_limpo_csv)
except Exception as error:
    print('Erro ao gerar CSV limpo: ', error)
    input('Digite qualquer coisa pra fechar.')

pyautogui.alert(f'Total buscado: {contador}, sendo:\nQuantidades (sem tratamento): {quantidade[0]}\n(com tratamento): {quantidade[1]}\nNão limpos: {quantidade[2]}')