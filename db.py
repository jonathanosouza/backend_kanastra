import mysql.connector
from mysql.connector import Error
from datetime import datetime

def conectar_mysql():
    try:
        conexao = mysql.connector.connect(
            port=3306,
            user='root',
            password='kanastra',
            database='kanastra',
            ssl_disabled=False,  
        )
        if conexao.is_connected():
            db_info = conexao.get_server_info()
            print("Conectado ao servidor MySQL versão ", db_info)
            cursor = conexao.cursor()
            cursor.execute("select database();")
            linha = cursor.fetchone()
            print("Conectado ao banco de dados ", linha)
            return conexao
    except Error as e:
        print("Erro ao conectar ao MySQL", e)

# Uso da função
conexao = conectar_mysql()

