
def gerar_csv_close_name(nome:str, lista_localizados: list, nome_arquivo: str):
    print(f'------------ pessoa localizada - {nome}')
    arquivo = f'{nome_arquivo}.csv' 
    for dado in lista_localizados:
        with open(arquivo, 'a', encoding='utf-8') as file:
            file.write(f'{nome};=@;{dado}\n')