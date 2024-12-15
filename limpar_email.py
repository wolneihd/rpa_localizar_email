import re
import pandas as pd
from difflib import SequenceMatcher
from check_nao_verificados import check_nao_limpos

# Função para calcular similaridade entre duas strings
def calculate_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Função para extrair nome e e-mail de uma linha
def extract_name_email(line):
    # Regex para encontrar e-mails
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', line)
    email = '; '.join(emails) if emails else None

    # Heurística para extrair o nome (parte antes do primeiro ponto-e-vírgula ou e-mail)
    name_match = re.match(r'^[^;]+', line)
    name = name_match.group(0).strip() if name_match else None

    return name, email

# Função para selecionar o e-mail com maior similaridade ao nome
def select_most_similar_email(name, emails):
    email_list = emails.split('; ')
    max_similarity = 0
    best_email = None
    for email in email_list:
        similarity = calculate_similarity(name, email.split('@')[0])  # Comparar com a parte antes do '@'
        if similarity > max_similarity:
            max_similarity = similarity
            best_email = email
    return best_email

# Função principal
def process_files(arquivo_sujo_csv: str, arquivo_limpo_csv: str):
    print(' ... GERANDO ARQUIVO LIMPO ... ')

    try:
        quantidade_sujo = 0
        df = pd.read_csv(arquivo_sujo_csv, header=None, names=['Name','Email'], sep=';=@;', engine='python')
        quantidade_sujo = len(df['Name'].value_counts())
        print(f'Quantidade de sujo: ', quantidade_sujo)
    except Exception as error:
        print('Erro ao pegar quantidade de sujos: ', error)        

    if quantidade_sujo == 0:
        return [quantidade_sujo, 0, 0]    
    else:
        all_data = []  # Lista para armazenar os dados processados
        # Processar cada arquivo
        with open(arquivo_sujo_csv, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Processar cada linha para extrair nome e e-mail
        extracted_data = [extract_name_email(line) for line in content]

        # Filtrar linhas onde nome ou e-mail está ausente
        filtered_data = [(name, email) for name, email in extracted_data if name and email]
        all_data.extend(filtered_data)

        # Criar um DataFrame
        df = pd.DataFrame(all_data, columns=['Name', 'Email'])

        # Consolidar e-mails por nome
        df = df.groupby('Name', as_index=False).agg({'Email': lambda x: '; '.join(sorted(set('; '.join(x).split('; '))))})

        # Selecionar o e-mail mais similar ao nome e garantir que cada nome apareça apenas uma vez
        df['Email'] = df.apply(lambda row: select_most_similar_email(row['Name'], row['Email']), axis=1)

        # Salvar os dados processados em um arquivo CSV
        df.to_csv(arquivo_limpo_csv, index=False, encoding='utf-8', header=None)

        df_limpo = pd.read_csv(arquivo_limpo_csv, header=None, names=['Name','Email'])
        quantidade_limpo = len(df_limpo.value_counts('Name').values)
    
        print(f'Quantidade de limpo: ', quantidade_limpo)

        nao_comparados = check_nao_limpos(arquivo_sujo_csv, arquivo_limpo_csv)

        return [quantidade_sujo, quantidade_limpo, nao_comparados]

def rodar_limpeza(arquivo_sujo_csv: str, arquivo_limpo_csv: str):
    quantidade = process_files(arquivo_sujo_csv, arquivo_limpo_csv)
    return quantidade