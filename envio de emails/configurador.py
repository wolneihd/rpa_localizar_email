import subprocess
import sys

def instalar_bibliotecas():
    # Lista de bibliotecas a serem instaladas
    bibliotecas = ["pandas", "pyautogui", 'openpyxl']
    try:
        for biblioteca in bibliotecas:
            print(f"Instalando '{biblioteca}'...")
            subprocess.run([sys.executable, "-m", "pip", "install", biblioteca], check=True)
            print(f"'{biblioteca}' instalada com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar '{biblioteca}': {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
