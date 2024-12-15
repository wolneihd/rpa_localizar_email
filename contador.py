import time

def contador_segundos(segundos: int, imprimir: bool = False):
    for index, segundo in enumerate(range(1,segundos+1)):
        time.sleep(1)
        if imprimir:
            print(f'contador: {index+1} de {segundos}')

if __name__ == "__main__":
    contador_segundos(5)