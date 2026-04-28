from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


routes = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"]
)


@routes.post(
    "/",
    response_model=schemas.TarefaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_tarefa(
    tarefa: schemas.TarefaCreate,
    db: Session = Depends(get_db)
):
    return crud.criar_tarefa(db=db, tarefa=tarefa)


@routes.get(
    "/",
    response_model=list[schemas.TarefaResponse]
)
def listar_tarefas(
    status_tarefa: Optional[schemas.StatusTarefa] = None,
    prioridade: Optional[schemas.PrioridadeTarefa] = None,
    db: Session = Depends(get_db)
):
    return crud.listar_tarefas(
        db=db,
        status=status_tarefa,
        prioridade=prioridade
    )


@routes.get(
    "/{tarefa_id}",
    response_model=schemas.TarefaResponse
)
def buscar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db)
):
    tarefa = crud.buscar_tarefa_por_id(db=db, tarefa_id=tarefa_id)

    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )

    return tarefa


@routes.put(
    "/{tarefa_id}",
    response_model=schemas.TarefaResponse
)
def atualizar_tarefa(
    tarefa_id: int,
    tarefa_atualizada: schemas.TarefaUpdate,
    db: Session = Depends(get_db)
):
    tarefa = crud.atualizar_tarefa(
        db=db,
        tarefa_id=tarefa_id,
        tarefa_atualizada=tarefa_atualizada
    )

    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )

    return tarefa


@routes.patch(
    "/{tarefa_id}/concluir",
    response_model=schemas.TarefaResponse
)
def concluir_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db)
):
    tarefa = crud.concluir_tarefa(db=db, tarefa_id=tarefa_id)

    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )

    return tarefa


@routes.delete(
    "/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db)
):
    tarefa = crud.excluir_tarefa(db=db, tarefa_id=tarefa_id)

    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )

    return None