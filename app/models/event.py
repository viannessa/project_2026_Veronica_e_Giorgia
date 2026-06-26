from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class EventBase(SQLModel):
    """Serve a definire tutti i campi comuni che l'evento
        possiede all'interno del sistema"""
    title: str
    description: str
    date: datetime
    location: str

class Event (EventBase, table = True):
    """Rappresenta la tabella 'event' all'interno del database relazionale"""
    id: Optional[int] = Field(default=None, primary_key=True)


class EventCreate (EventBase):
    """Modello di dati per le API, permette di creare un evento"""
    pass


class EventPublic(EventBase):
    '''Rappresenta la struttura dei dati che verrano restituiti dalle API'''
    id: int



