import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield


def test_rota_inicial():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"mensagem": "Micro-API de Tarefas funcionando!"}


def test_criar_tarefa():
    payload = {
        "titulo": "Estudar FastAPI",
        "descricao": "Criar testes automatizados para a API",
        "status": "pendente",
        "prioridade": "alta",
    }

    response = client.post("/tarefas/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["titulo"] == "Estudar FastAPI"
    assert data["status"] == "pendente"
    assert data["prioridade"] == "alta"


def test_listar_tarefas():
    client.post(
        "/tarefas/",
        json={
            "titulo": "Primeira tarefa",
            "descricao": "Descrição da primeira tarefa",
            "status": "pendente",
            "prioridade": "media",
        },
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Segunda tarefa",
            "descricao": "Descrição da segunda tarefa",
            "status": "em_andamento",
            "prioridade": "alta",
        },
    )

    response = client.get("/tarefas/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_buscar_tarefa_por_id():
    tarefa_criada = client.post(
        "/tarefas/",
        json={
            "titulo": "Buscar tarefa",
            "descricao": "Teste de busca por ID",
            "status": "pendente",
            "prioridade": "baixa",
        },
    ).json()

    response = client.get(f"/tarefas/{tarefa_criada['id']}")

    assert response.status_code == 200
    assert response.json()["titulo"] == "Buscar tarefa"


def test_atualizar_tarefa():
    tarefa_criada = client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa antiga",
            "descricao": "Descrição antiga",
            "status": "pendente",
            "prioridade": "media",
        },
    ).json()

    response = client.put(
        f"/tarefas/{tarefa_criada['id']}",
        json={
            "titulo": "Tarefa atualizada",
            "descricao": "Descrição atualizada",
            "status": "em_andamento",
            "prioridade": "alta",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["titulo"] == "Tarefa atualizada"
    assert data["status"] == "em_andamento"
    assert data["prioridade"] == "alta"


def test_concluir_tarefa():
    tarefa_criada = client.post(
        "/tarefas/",
        json={
            "titulo": "Concluir tarefa",
            "descricao": "Teste de conclusão",
            "status": "pendente",
            "prioridade": "media",
        },
    ).json()

    response = client.patch(f"/tarefas/{tarefa_criada['id']}/concluir")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "concluida"
    assert data["data_conclusao"] is not None


def test_excluir_tarefa():
    tarefa_criada = client.post(
        "/tarefas/",
        json={
            "titulo": "Excluir tarefa",
            "descricao": "Teste de exclusão",
            "status": "pendente",
            "prioridade": "media",
        },
    ).json()

    response = client.delete(f"/tarefas/{tarefa_criada['id']}")

    assert response.status_code == 204

    response_busca = client.get(f"/tarefas/{tarefa_criada['id']}")

    assert response_busca.status_code == 404


def test_filtrar_tarefas_por_status():
    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa pendente",
            "descricao": "Teste filtro pendente",
            "status": "pendente",
            "prioridade": "media",
        },
    )

    client.post(
        "/tarefas/",
        json={
            "titulo": "Tarefa concluída",
            "descricao": "Teste filtro concluída",
            "status": "concluida",
            "prioridade": "alta",
        },
    )

    response = client.get("/tarefas/?status_tarefa=concluida")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "concluida"