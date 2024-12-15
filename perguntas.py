import pyautogui

def perguntas():

    #nome_arquivo = pyautogui.prompt('Digite o nome do arquivo CSV de resultado: ')
    limite = pyautogui.prompt('Quantos deseja fazer?')
    tempo = pyautogui.prompt('Digite o tempo entre as pesquisas: ')
    contexto_adicional = pyautogui.prompt('Incluir contexto adicional: ')
    na_tela = pyautogui.confirm('Deseja a pesquisa rodar na tela ou em off? ', buttons=['aberto','off'])
    continuar_de_uma_pessoa_especifica = pyautogui.confirm('Deseja continuar de uma pessoa especifica? ', buttons=['sim','nao'])

    try:
        # if nome_arquivo == '' or nome_arquivo == None:
        #     nome_arquivo = 'arquivo'

        if continuar_de_uma_pessoa_especifica == 'sim':
            continuar_de_uma_pessoa_especifica = True
        else:
            continuar_de_uma_pessoa_especifica = False

        if na_tela == 'aberto':
            na_tela = True
        else:
            na_tela = False
    
        if limite.lower() == 'todos' or limite.lower() == 't':
            limite = 50_000
        else:
            limite  = int(limite)

    except Exception as error:
        limite = 50
        
    try:
        if tempo == '' or tempo == None:
            tempo = 5
        else:
            tempo = int(tempo)

    except Exception as error:
        tempo = 5

    dados = {
        #'nome_arquivo': nome_arquivo,
        'limite': limite,
        'tempo': tempo,
        'na_tela': na_tela,
        'continuar_de_uma_pessoa_especifica': continuar_de_uma_pessoa_especifica,
        'contexto_adicional': contexto_adicional
    }

    with open('logs.txt', 'a', encoding='utf-8') as file:
        file.write(f'\n----------------------------------- \n')
        file.write(f'Campos utilizandos na busca: \n')
        #file.write(f'nome_arquivo: {nome_arquivo}\n')
        file.write(f'limite_50: {limite}\n')
        file.write(f'tempo: {tempo}\n')
        file.write(f'na_tela: {na_tela}\n')
        file.write(f'continuar_de_uma_pessoa_especifica: {continuar_de_uma_pessoa_especifica}\n')
        file.write(f'----------------------------------- \n')
    
    return dados

if __name__ == "__main__":
    perguntas()



