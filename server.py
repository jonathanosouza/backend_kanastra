from flask import Flask, jsonify, request
from db import conectar_mysql
import csv
from io import StringIO
from flask_cors import CORS
import time
from datetime import datetime


app = Flask(__name__)
CORS(app)

def conectar():
    return conectar_mysql()


@app.route('/salvar_historico_cobranca', methods=['POST'])
def salvar_historico_cobranca(name, size, user, tempo_upload):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            # Extrair os dados enviados na requisição
            nome_arquivo = name
            tamanho = size
            usuario = user
            tempoupload = tempo_upload
            data_upload = datetime.now() 
            
            # Verificar se todos os campos estão presentes
            if nome_arquivo is None or tamanho is None or usuario is None or tempoupload is None:
                return jsonify({"error": "Missing required fields"}), 400
            
            # Inserir os dados na tabela historico_cobranca
            cursor.execute("INSERT INTO historico_cobranca (nome_arquivo, tamanho, usuario, tempo_upload, data_upload) VALUES (%s, %s, %s, %s, %s)", 
                           (nome_arquivo, tamanho, usuario, tempoupload, data_upload))
            
            conexao.commit()
            
            return "Dados salvos com sucesso!"
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conexao.close()

@app.route('/uploadcobranca', methods=['POST'])
def criar_cobranca():
    conexao = conectar()
    if conexao:
        try:
            start_task = time.time()  # Registrar o tempo de início da tarefa
            print("Início da tarefa:", start_task)  # Debugging

            cursor = conexao.cursor()
            # Ler o arquivo CSV enviado no corpo da requisição
            csv_file = request.files['file']
            stream = StringIO(csv_file.stream.read().decode("UTF-8"), newline=None)
            csv_data = csv.reader(stream)

            # Ignorar a primeira linha do CSV (cabeçalho)
            next(csv_data)

            # Preparar os dados para inserção em lote
            batch_size = 1000  # Tamanho do lote
            batch = []

            for row in csv_data:
                batch.append(row)

                if len(batch) >= batch_size:
                    cursor.executemany(
                        "INSERT INTO cobranca (name, governmentId, email, debtAmount, debtDueDate, debtId) VALUES (%s, %s, %s, %s, %s, %s)",
                        batch)
                    conexao.commit()  # Confirmar o lote
                    batch = []  # Limpar o lote

            # Inserir quaisquer linhas restantes no lote final
            if batch:
                cursor.executemany(
                    "INSERT INTO cobranca (name, governmentId, email, debtAmount, debtDueDate, debtId) VALUES (%s, %s, %s, %s, %s, %s)",
                    batch)
                conexao.commit()

            stop_task = time.time()  # Registrar o tempo de término da tarefa
            print("Término da tarefa:", stop_task)  # Debugging
            tempo_upload = (stop_task - start_task) / 60  # Calcular o tempo decorrido em minutos
            print("Tempo de upload:", tempo_upload)

            # Chamar a função para salvar no histórico
            salvar_historico_cobranca(request.form['name'], request.form['size'], 'JonathanSouza', tempo_upload)

            return f"Dados inseridos com sucesso! Tempo de upload: {tempo_upload:.2f} minutos."
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conexao.close()




@app.route('/cobranca', methods=['GET'])
def listar_cobrancas():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            page = int(request.args.get('page', 1)) 
            per_page = int(request.args.get('per_page', 1000))

            # Calcular o índice inicial e final dos registros na página atual
            start_index = (page - 1) * per_page
            end_index = start_index + per_page

            cursor.execute("SELECT * FROM cobranca LIMIT %s OFFSET %s", (per_page, start_index))
            cobrancas = cursor.fetchall()

            # Convertendo a lista de tuplas para uma lista de dicionários
            cobrancas_formatadas = []
            for cobranca in cobrancas:
                cobranca_dict = {
                    "id": cobranca[0],
                    "name": cobranca[1],
                    "governmentId": cobranca[2],
                    "email": cobranca[3],
                    "debtAmount": cobranca[4],
                    "debtDueDate": cobranca[5],
                    "debtId": cobranca[6]
                }
                cobrancas_formatadas.append(cobranca_dict)

            return jsonify(cobrancas_formatadas)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conexao.close()
            

@app.route('/historicocobranca', methods=['GET'])
def listar_historico_cobrancas():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM historico_cobranca")
            cobrancas = cursor.fetchall()

            # Convertendo a lista de tuplas para uma lista de dicionários
            cobrancas_historico = []
            for cobranca in cobrancas:
                cobranca_dict = {
                    "id": cobranca[0],
                    "nome_arquivo": cobranca[1],
                    "tamanho": cobranca[2],
                    "data_upload": cobranca[3],
                    "usuario": cobranca[4],
                    "tempo_upload": cobranca[5],
                }
                cobrancas_historico.append(cobranca_dict)

            return jsonify(cobrancas_historico)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conexao.close()
            

if __name__ == '__main__':
    app.run(debug=True)
