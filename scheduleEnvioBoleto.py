import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from db import conectar_mysql


def conectar():
    return conectar_mysql()


def consultar_cobrancas():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT email FROM cobranca WHERE DATE(debtDueDate) = CURDATE()")
            cobrancas = cursor.fetchall()
            return cobrancas
        except Exception as e:
            print("Erro ao consultar cobranças:", e)
        finally:
            cursor.close()
            conexao.close()


def enviar_email(destinatario, nome_arquivo):
    
    remetente = 'seu_email@gmail.com'  
    senha = 'sua_senha'  
    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587

   
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = 'Boleto para Pagamento'


    mensagem = f'Olá, segue seu boleto para pagamento: {nome_arquivo}'
    msg.attach(MIMEText(mensagem, 'plain'))

 
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)

  
        server.sendmail(remetente, destinatario, msg.as_string())
        print(f"E-mail enviado para {destinatario}")
        
        server.quit()
    except Exception as e:
        print("Erro ao enviar e-mail:", e)


def verificar_cobrancas():
    cobrancas = consultar_cobrancas()
    if cobrancas:
        for cobranca in cobrancas:
            email, nome_arquivo = cobranca
            enviar_email(email, nome_arquivo)

schedule.every(24).hours.do(verificar_cobrancas)

while True:
    schedule.run_pending()
    time.sleep(1)
