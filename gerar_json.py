import questionary
import pandas as pd
import json

def obter_objeto(continuar_de_uma_pessoa_especifica: bool, caminho_arquivo: str, tipo: str):

    if tipo == 'csv':
        df = pd.read_csv(caminho_arquivo, header=None, names=['nome','a','b','c','d'],sep=r'[;,]', engine='python')
    else:
        df = pd.read_excel(caminho_arquivo, header=None, names=['nome','a','b','c','d'])

    if continuar_de_uma_pessoa_especifica:

        lista_opcoes = df['nome'].values
        nome = questionary.select(
            "Escolha o nome desejado:",
            choices=lista_opcoes
        ).ask()

        index = df[df['nome'] == nome].index
        json_data = df.loc[index[0]:].to_json(orient='records')
        data_list = json.loads(json_data)
        return data_list
    
    else:
        json_data = df.to_json(orient='records')
        return json.loads(json_data)

if __name__ == "__main__":
    dados = obter_objeto(continuar_de_uma_pessoa_especifica=True)
    print(dados)
    print(len(dados))