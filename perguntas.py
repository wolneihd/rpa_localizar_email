import pyautogui

def perguntas():

    limite = pyautogui.prompt('Quantos deseja fazer? "todos" ou "t" para todos.')
    contexto_adicional = pyautogui.prompt('Incluir contexto adicional: ')
    na_tela = pyautogui.confirm('Deseja a pesquisa rodar na tela ou em off? ', buttons=['aberto','off'])
    continuar_de_uma_pessoa_especifica = pyautogui.confirm('Deseja continuar de uma pessoa especifica? ', buttons=['sim','nao'])
    site = pyautogui.confirm('Escolha em qual site deseja que o robô rode: ', buttons=['Google','Bing', 'Yahoo'])

    try:
        if continuar_de_uma_pessoa_especifica == 'sim':
            continuar_de_uma_pessoa_especifica = True
        else:
            continuar_de_uma_pessoa_especifica = False

        if na_tela == 'aberto':
            na_tela = True
        else:
            na_tela = False
    
        if limite.lower() == 'todos' or limite.lower() == 't' or limite == None or limite == '':
            limite = 50_000
        else:
            limite  = int(limite)

    except Exception as error:
        limite = 50
        
    dados = {
        #'nome_arquivo': nome_arquivo,
        'limite': limite,
        'na_tela': na_tela,
        'continuar_de_uma_pessoa_especifica': continuar_de_uma_pessoa_especifica,
        'contexto_adicional': contexto_adicional,
        'site': site,
    }

    with open('logs.txt', 'a', encoding='utf-8') as file:
        file.write(f'\n----------------------------------- \n')
        file.write(f'Campos utilizandos na busca: \n')
        file.write(f'limite_50: {limite}\n')
        file.write(f'na_tela: {na_tela}\n')
        file.write(f'continuar_de_uma_pessoa_especifica: {continuar_de_uma_pessoa_especifica}\n')
        file.write(f'site: {site}\n')
        file.write(f'----------------------------------- \n')
    
    return dados

if __name__ == "__main__":
    perguntas()



