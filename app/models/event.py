from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

#1. MODELLO BASE: USATO PER DEFINIRE I CAMPI COMUNI
class EventBase(SQLModel):
    title: str
    description: str
    date: datetime
    location: str

#2. MODELLO INPUT: USATO PER POST E PUT (no ID)
class EventCreate (EventBase):
    pass

#3. MODELLO OUTPUT: USATO PER GET (con ID)
class EventPublic(EventBase):
    '''Rappresenta la struttura dei dati che verrano restituiti dalle API'''
    id: int

#4. MODELLO RELAZIONALE (DATABASE): crea la tabella ed è l'ORM vero e proprio
class Event (EventBase, table = True):
    """Rappresenta la tabella 'event' all'interno del database relazionale"""
    id: Optional[int] = Field(default=None, primary_key=True)

'''FINE '''