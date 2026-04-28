from fastapi import FastAPI

app = FastAPI(
    title="Micro-API de Gerenciamento de Tarefas",
    description="API RESTful para gerenciamento de tarefas desenvolvida com auxílio de IA generativa.",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"mensagem": "Micro-API de Tarefas funcionando!"}