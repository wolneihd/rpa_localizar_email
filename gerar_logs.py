def inserir_no_log(valor):  
    with open('logs.txt', 'a', encoding='utf-8') as file:
            file.write(f'{valor} \n')