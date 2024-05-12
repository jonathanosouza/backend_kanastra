import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_listar_cobrancas(client):
    response = client.get('/cobranca')
    assert response.status_code == 200
    data = response.json  
    assert isinstance(data, list)   
    assert all(isinstance(item, dict) for item in data)  
    assert all(key in data[0] for key in ['id', 'name', 'governmentId', 'email', 'debtAmount', 'debtDueDate', 'debtId'])  



def test_salvar_historico_cobranca(client):
    # Dados de exemplo a serem enviados na requisição POST
    data = {
        'name': 'example.csv',
        'size': '1024',
        'user': 'test_user',
        'tempo_upload': 5.0
    }

    # Envia uma solicitação POST para a rota '/salvar_historico_cobranca' com os dados
    response = client.post('/salvar_historico_cobranca', json=data)

    # Verifica se a resposta é bem-sucedida (código de status 200)
    assert response.status_code == 200

    # Verifica se a resposta contém a mensagem de sucesso
    assert b'Dados salvos com sucesso!' in response.data


def test_listar_historico_cobrancas(client):
    response = client.get('/historicocobranca')
    assert response.status_code == 200
    assert b'id' in response.data
    assert b'nome_arquivo' in response.data
    assert b'tamanho' in response.data
    assert b'data_upload' in response.data
    assert b'usuario' in response.data
    assert b'tempo_upload' in response.data


def test_upload_arquivo(client):
    csv_file = open('input.csv', 'rb')
    response = client.post('/uploadcobranca', data={'file': csv_file})
    csv_file.close()
    assert response.status_code == 200
    # Verifica se a resposta contém a mensagem de sucesso
    assert b'Dados inseridos com sucesso!' in response.data