
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    """
    Modello per la tabella 'user'. Serve per memorizzare le info
    degli utenti registrati alla piattaforma
    """
    username: str = Field(primary_key=True, index=True)
    name: str
    email: str