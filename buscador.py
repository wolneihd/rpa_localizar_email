def get_data_buscador(site: str):
    if site == 'Google':
        google = {
            'url': 'https://www.google.com.br/',
            'campo_busca': 'q',
            'xpath': '//*[@id="botstuff"]/div/div[3]/table/tbody/tr/td[3]/a',
            'limpar_busca': '//*[@id="tsf"]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]/div' 
        }
        return google
    elif site == 'Bing':
        bing = {
            'url': 'https://www.bing.com/?cc=br',
            'campo_busca': 'q',
            'xpath': '//*[@id="b_results"]/li[13]/nav/ul/li[2]/a'
        }
        return bing
    elif site == 'Yahoo':
        yahoo = {
            'url': 'https://br.search.yahoo.com/?fr2=p:fprd,mkt:br',
            'campo_busca': 'p',
            'xpath': '//*[@id="left"]/div/ol/li[1]/div/div/div/a[1]',
            'limpar_busca': '//*[@id="sbq-clear"]/span[1]'
        }
        return yahoo
