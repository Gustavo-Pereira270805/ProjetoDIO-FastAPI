# tests/atleta/test_atleta.py
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAtleta:
    async def test_create_atleta_deve_retornar_201(
        self, client: AsyncClient, categoria_db, centro_treinamento_db
    ):
        atleta_data = {
            "nome": "Atleta Teste", "cpf": "12345678900", "idade": 30, "peso": 80.5, "altura": 1.75, "sexo": "M",
            "categoria": categoria_db.nome,
            "centro_treinamento": centro_treinamento_db.nome
        }

        response = await client.post('/atletas/', json=atleta_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['nome'] == atleta_data['nome']
        assert 'pk_id' in data

    async def test_get_atleta_por_pk_id_deve_retornar_200(
        self, client: AsyncClient, categoria_db, centro_treinamento_db
    ):
        atleta_data = {"nome": "Atleta GET", "cpf": "11122233300", "idade": 25, "peso": 70.0, "altura": 1.70, "sexo": "F", "categoria": categoria_db.nome, "centro_treinamento": centro_treinamento_db.nome}
        response_post = await client.post('/atletas/', json=atleta_data)
        atleta_pk_id = response_post.json()['pk_id']

        response_get = await client.get(f'/atletas/{atleta_pk_id}')

        assert response_get.status_code == status.HTTP_200_OK
        assert response_get.json()['nome'] == atleta_data['nome']

    async def test_get_atleta_id_nao_encontrado_deve_retornar_404(self, client: AsyncClient):
        response = await client.get(f'/atletas/{uuid4()}')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_all_atletas_deve_retornar_200_e_lista(
        self, client: AsyncClient, categoria_db, centro_treinamento_db
    ):
        atleta_data = {"nome": "Atleta All", "cpf": "44455566600", "idade": 28, "peso": 65.0, "altura": 1.65, "sexo": "F", "categoria": categoria_db.nome, "centro_treinamento": centro_treinamento_db.nome}
        await client.post('/atletas/', json=atleta_data)

        response = await client.get('/atletas/')

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    async def test_update_atleta_deve_retornar_200(
        self, client: AsyncClient, categoria_db, centro_treinamento_db
    ):
        atleta_data = {"nome": "Atleta Update", "cpf": "77788899900", "idade": 35, "peso": 90.0, "altura": 1.85, "sexo": "M", "categoria": categoria_db.nome, "centro_treinamento": centro_treinamento_db.nome}
        response_post = await client.post('/atletas/', json=atleta_data)
        atleta_pk_id = response_post.json()['pk_id']

        atleta_update_data = {'idade': 36, 'peso': 91.0}
        response = await client.patch(f'/atletas/{atleta_pk_id}', json=atleta_update_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['idade'] == atleta_update_data['idade']

    async def test_delete_atleta_deve_retornar_204(
        self, client: AsyncClient, categoria_db, centro_treinamento_db
    ):
        atleta_data = {"nome": "Atleta Delete", "cpf": "10120230300", "idade": 40, "peso": 100.0, "altura": 1.90, "sexo": "M", "categoria": categoria_db.nome, "centro_treinamento": centro_treinamento_db.nome}
        response_post = await client.post('/atletas/', json=atleta_data)
        atleta_pk_id = response_post.json()['pk_id']

        response = await client.delete(f'/atletas/{atleta_pk_id}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
