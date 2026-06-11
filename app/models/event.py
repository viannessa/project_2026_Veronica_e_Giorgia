from sqlmodel import SQLModel, Field
from datetime import datetime

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
    id: int

#3. MODELLO RELAZIONALE (DATABASE): crea la tabella ed è l'ORM vero e proprio
#è richiesto esplicitamente dall specifiche che si chiami "Event"
class Event (EventBase, table = True):
    id: int = Field(default=None, primary_key=True)