import time
import random

# -------------------------------------------
# Edição de periodo de segundos de espera
# -------------------------------------------
inicio = 5
fim = 10

def contador_segundos(imprimir: bool = False):
    segundos = random.uniform(inicio, fim)
    if imprimir:
        print(f'Aguardando {segundos:.2f} segundos (entre {inicio}seg. e {fim}seg.)')
    time.sleep(segundos)

if __name__ == "__main__":
    contador_segundos()