from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas


def criar_tarefa(db: Session, tarefa: schemas.TarefaCreate):
    nova_tarefa = models.Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        status=tarefa.status,
        prioridade=tarefa.prioridade,
    )

    if tarefa.status == "concluida":
        nova_tarefa.data_conclusao = datetime.now(timezone.utc)

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return nova_tarefa


def listar_tarefas(
    db: Session,
    status: Optional[str] = None,
    prioridade: Optional[str] = None,
):
    consulta = db.query(models.Tarefa)

    if status:
        consulta = consulta.filter(models.Tarefa.status == status)

    if prioridade:
        consulta = consulta.filter(models.Tarefa.prioridade == prioridade)

    return consulta.order_by(models.Tarefa.id).all()


def buscar_tarefa_por_id(db: Session, tarefa_id: int):
    return db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()


def atualizar_tarefa(
    db: Session,
    tarefa_id: int,
    tarefa_atualizada: schemas.TarefaUpdate,
):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)

    if tarefa is None:
        return None

    dados_atualizados = tarefa_atualizada.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        setattr(tarefa, campo, valor)

    if dados_atualizados.get("status") == "concluida":
        tarefa.data_conclusao = datetime.now(timezone.utc)

    if dados_atualizados.get("status") in ["pendente", "em_andamento", "cancelada"]:
        tarefa.data_conclusao = None

    db.commit()
    db.refresh(tarefa)

    return tarefa


def concluir_tarefa(db: Session, tarefa_id: int):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)

    if tarefa is None:
        return None

    tarefa.status = "concluida"
    tarefa.data_conclusao = datetime.now(timezone.utc)

    db.commit()
    db.refresh(tarefa)

    return tarefa


def excluir_tarefa(db: Session, tarefa_id: int):
    tarefa = buscar_tarefa_por_id(db, tarefa_id)

    if tarefa is None:
        return None

    db.delete(tarefa)
    db.commit()

    return tarefa