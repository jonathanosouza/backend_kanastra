import mysql.connector

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kanastra",
    database="kanastra"
)

# Criar cursor para executar comandos SQL
cursor = conexao.cursor()

# Comandos SQL para criar as tabelas
comando_criar_cobranca = """
CREATE TABLE cobranca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    governmentId VARCHAR(20),
    email VARCHAR(255),
    debtAmount DECIMAL(10, 2),
    debtDueDate DATE,
    debtId VARCHAR(255)
)
"""

comando_criar_historico_cobranca = """
CREATE TABLE historico_cobranca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_arquivo VARCHAR(255),
    tamanho INT,
    data_upload DATETIME,
    usuario VARCHAR(100),
    tempo_upload INT
)
"""

# Executar os comandos SQL
cursor.execute(comando_criar_cobranca)
cursor.execute(comando_criar_historico_cobranca)

# Confirmar a execução dos comandos
conexao.commit()

# Fechar cursor e conexão
cursor.close()
conexao.close()

print("Tabelas criadas com sucesso!")
