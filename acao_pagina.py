import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def digitar(search_box, texto):
    for letra in texto:
        time.sleep(random.choice([0.1,0.2,0.3]))
        search_box.send_keys(letra)

def rolar_pagina(driver, total_scrolls=random.randint(1,5), pause_range=(0.5, 1.5)):
    """   
    Args:
    - driver: o WebDriver do Selenium.
    - total_scrolls: número de incrementos de rolagem.
    - pause_range: intervalo de tempo (mín, máx) entre as rolagens.
    """
    current_position = 0
    for _ in range(total_scrolls):
        # Incremento aleatório para a rolagem (altura)
        scroll_distance = random.randint(200, 400)
        current_position += scroll_distance
        
        # Rolagem suave
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        
        # Pausa aleatória para imitar comportamento humano
        time.sleep(random.uniform(*pause_range))
    
    # Rolagem até o final como toque final
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def aceitar_termos_bing(driver):
    try:
        aceitar = driver.find_element(By.ID, 'bnp_btn_accept')
        aceitar.click()
    except:
        print('Campo aceitar termos do Google não localizado.')

def aceitar_termos_yahoo(driver):
    try:
        # Executar clique via JavaScript
        button = driver.find_element(By.NAME, 'agree')
        driver.execute_script("arguments[0].click();", button)
    except:
        pass