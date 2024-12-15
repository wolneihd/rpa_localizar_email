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
except Exception as error:
    print('Erro ao importar biblioteca do Python: ', error)
    input('Digite qualquer coisa pra fechar.')

# -----------------------------------
# Ambiente de teste: 2.0
# -----------------------------------
dados = perguntas()
data_list = obter_objeto(dados['continuar_de_uma_pessoa_especifica'])

# Configurações para o Chrome em modo headless
if dados['na_tela'] == False:
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu") 
    driver = webdriver.Chrome(service=Service("./chromedriver.exe")  , options=chrome_options)
else:
    driver = webdriver.Chrome(service=Service("./chromedriver.exe"))

def incluir_dado(linha):
    with open(f'{dados['nome_arquivo']}.csv', 'a', encoding='utf-8') as file:
        file.write(linha + "\n")

def texto_busca(pessoa): # 'a','b','c','d'
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
    
    return f'"{pessoa['nome']}" {coluna_a} {coluna_b} {coluna_c} {coluna_d}'
    
contador = 0
quantidade = len(data_list)
segundos = dados['tempo']

try:
    for index, pessoa in enumerate(data_list):

        quantidade -= 1

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
        print(f'{quantidade} | {str_busca}')
        search_box.send_keys(f'{str_busca}')

        # Pressionar Enter
        search_box.send_keys(Keys.RETURN)

        contador_segundos(segundos)

        # Salvar o conteúdo HTML da página em uma variável
        html_content = driver.page_source

        contador_segundos(segundos)

        # # Define o nome do arquivo
        # nome = pessoa['nome'].lower()
        # arquivo = f'paginas\\{nome}.txt'

        # # Garante que a pasta 'paginas' existe
        # os.makedirs(os.path.dirname(arquivo), exist_ok=True)

        # Salva o conteúdo da página no arquivo
        html_content = driver.page_source
        
        # # DESABILITADO PARA EVITAR MUITOS ARQUIVOS NO PROD.
        # with open(arquivo, 'w', encoding='utf-8') as file:
        #     file.write(html_content)
    
        if 'detectaram tráfego incomum' in html_content:            
            inserir_no_log(f'Google detectou o robô bloqueou acessar a página. Parou na pessoa {pessoa['nome']}')
            break

        # Usando o método find para encontrar a posição do texto
        for nome in pessoa['nome'].split(' '): #['fulano','da','silva'] fulano@, da@, silva@
            contador_segundos(1)
            index = html_content.find(f'{nome.lower()}@')
            if index > 1:
                contador += 1
                texto_fatiado = html_content[index-50:index+50:]
                print(f'------------ pessoa localizada - {pessoa['nome']}')
                linha = f'{pessoa['nome']};-;{texto_fatiado}'
                incluir_dado(linha)

except Exception as error:
    inserir_no_log('Erro ao rodar o sistema: ', error)
    input('Digite qualquer coisa pra fechar.')

porcentagem = round((contador/len(data_list))*100, 2)
pyautogui.alert(f'E-mails localizados: {contador} - sucesso de {porcentagem} %')