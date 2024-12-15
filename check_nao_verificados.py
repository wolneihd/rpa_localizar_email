import pandas as pd
import time

def check_nao_limpos(arquivo_sujo_csv: str, arquivo_limpo_csv: str):
    print('... Fazendo comparação dos não limpos: ')

    try:
        df = pd.read_csv(arquivo_sujo_csv, header=None, names=['Name','Email'], sep=';=@;', engine='python')
        quantidade_sujos = df['Name'].values

        df_limpo = pd.read_csv(arquivo_limpo_csv, header=None, names=['Name','Email'])
        quantidade_limpos = df_limpo['Name'].values     

        nao_localizados = []
        for nome in quantidade_sujos:
            if nome not in quantidade_limpos:
                nao_localizados.append(nome)

        timestamp = int(time.time())

        if nao_localizados != 0:
            print('Lista de não localizados: ')
            for dado in nao_localizados:
                with open(f'nao_comparados_{timestamp}.txt', 'a', encoding='utf-8') as file:
                    file.write(dado + "\n")    
            return len(nao_localizados)
        else:
            return 0

    except Exception as error:
        print('Não foi possível verificar a quantidade de diferença entre limpos e sujos.', error)
        return 0