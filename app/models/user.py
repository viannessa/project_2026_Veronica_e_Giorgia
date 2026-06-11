from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """
    Serve a definire tutti i campi comuni che l'utente
    possiede all'interno del sistema
    """
    username: str = Field(primary_key=True, index=True)
    name: str
    email: str


class User(UserBase, table = True):
    """Rappresenta la tabella 'user' all'interno del database relazionale"""
    pass

class UserPublic(UserBase):
    """Modello di dati per le API, permette di restituire le info di un utente"""
    pass

class Usercreate(UserBase):
    pass
