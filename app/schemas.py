from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


StatusTarefa = Literal["pendente", "em_andamento", "concluida", "cancelada"]
PrioridadeTarefa = Literal["baixa", "media", "alta"]


class TarefaBase(BaseModel):
    titulo: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Título da tarefa"
    )
    descricao: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Descrição detalhada da tarefa"
    )
    status: StatusTarefa = Field(
        default="pendente",
        description="Status atual da tarefa"
    )
    prioridade: PrioridadeTarefa = Field(
        default="media",
        description="Prioridade da tarefa"
    )


class TarefaCreate(TarefaBase):
    pass


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    descricao: Optional[str] = Field(
        default=None,
        max_length=500
    )
    status: Optional[StatusTarefa] = None
    prioridade: Optional[PrioridadeTarefa] = None


class TarefaResponse(TarefaBase):
    id: int
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)