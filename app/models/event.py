from sqlmodel import SQLModel, Field
from datetime import datetime

'''Rappresenta un evento nel sistema.
Contiene informazioni su titolo, descrizione, data e luogo.
'''
class Event(SQLModel, table = True):
    event_id: int = Field(default = None, primary_key = True)
    title: str
    description: str
    date: datetime
    location: str