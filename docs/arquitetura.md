# Arquitetura da Micro-API de Gerenciamento de Tarefas

## 1. Visão Geral

A Micro-API de Gerenciamento de Tarefas é uma aplicação RESTful desenvolvida em Python com FastAPI.  
O objetivo do projeto é permitir o cadastro, consulta, atualização, conclusão, exclusão e filtragem de tarefas.

A solução foi desenvolvida como um MVP simples, claro e viável, priorizando organização de código, separação de responsabilidades, testes automatizados e documentação.

---

## 2. Tecnologias Utilizadas

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- HTTPX

---

## 3. Estrutura de Módulos

```text
micro-api-tarefas-jn/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routes.py
│
├── tests/
│   └── test_tarefas.py
│
├── docs/
│   └── arquitetura.md
│
├── requirements.txt
├── .gitignore
└── README.md