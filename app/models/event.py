from sqlmodel import SQLModel, Field

class Event(SQLModel, table = True):
    event_id: int = Field(default = None, primary_key = True)