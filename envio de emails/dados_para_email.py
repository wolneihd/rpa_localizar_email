import pandas as pd
import json

def obter_dados():
    dados = pd.read_excel('texto_email.xlsx')
    json_data = dados.to_json(orient='records')
    dados = json.loads(json_data)
    return dados

if __name__ == "__main__":
    dados = obter_dados()
    print(dados)
