from sqlmodel import SQLModel, Field


class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username")
    event_id: int = Field(primary_key=True, foreign_key="event.id")

class RegistrationPublic(Registration):
    """Modello di dati per le API, permette di restituire le info di una registrazione"""
    pass