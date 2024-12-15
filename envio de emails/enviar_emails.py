from configurador import instalar_bibliotecas
instalar_bibliotecas()

try:
    import smtplib
    import email.message
    import string
    from dados_para_email import obter_dados
    import pyautogui
    import time
except Exception as error:
    print('Biblioteca faltante para rodar o sistema.')
    input()

pausa = pyautogui.prompt('Digite a quantidade de segundos entre cada envio:')
try:
    pausa = int(pausa)
except Exception as e:
    pausa = 0
    print('Você inseriu um valor incorreto nose segundos')

with open('senha.txt', 'r', encoding='utf-8') as f:
        senha = f.read()

with open('email.txt', 'r', encoding='utf-8') as f:
        remetente = f.read()

def enviar_email(corpo_email: str, assunto: str, destinatario: str):
    try:
        msg = email.message.Message()
        msg['Subject'] = assunto
        msg['From'] = remetente
        msg['To'] = destinatario

        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        s.login(msg['From'], password=senha)
        s.sendmail(msg['FROM'], [msg['To']], msg.as_string().encode('utf-8'))

        print(f'Email enviado com sucesso para: {destinatario}')
    except Exception as error:
         print(f'Erro ao enviar mensagem a pessoa: {destinatario}')

def gerar_texto(dados: dict):
    with open('email_padrao.html', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    template = string.Template(conteudo)
    email = template.substitute(dados)
    return email

if __name__ == "__main__":
    try: 
        dados = obter_dados()
        for pessoa in dados:
            texto_email = gerar_texto(pessoa)
            time.sleep(pausa)
            enviar_email(texto_email, pessoa['titulo'], destinatario=pessoa['email'])
        pyautogui.alert(f'E-mails enviados com sucesso a {len(dados)} destinatários!')
    except Exception as error:
        print('Erro no método de enviar e-mails. Verificar')
        input()
        
