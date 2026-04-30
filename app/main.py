from fastapi import FastAPI

from app.database import Base, engine
from app.routes import routes as tarefas_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Micro-API de Gerenciamento de Tarefas",
    description="API RESTful para gerenciamento de tarefas desenvolvida com auxílio de IA generativa.",
    version="1.0.0"
)

app.include_router(tarefas_router)


@app.get("/")
def read_root():
    return {"mensagem": "Micro-API de Tarefas funcionando!"}