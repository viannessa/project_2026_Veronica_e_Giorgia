'''FILE PER API CHE SI COLLEGANO ALLA SESSIONE DATABASE'''
from fastapi import APIRouter, Path, HTTPException, Query
from app.models.event import EventCreate, EventPublic, Event
from app.models.registration import Registration
from app.models.user import User, UserCreate
from typing import Annotated
from app.data.db import SessionDep
from sqlmodel import select, delete

router = APIRouter(prefix = "/events", tags = ["Events"])

@router.get("/")
def get_all_events(
        session:SessionDep
) -> list[EventPublic]:
    """Restituisce la lista di tutti gli eventi disponibili"""
    events = session.exec(select(Event)).all()
    return list(events)


@router.post("/")
def create_event(
        session: SessionDep,
        event: EventCreate):
    """Inserisce un nuovo evento nel DB"""
    new_event = Event.model_validate(event)
    session.add(new_event)
    session.commit()
    return "Event created successfully"


@router.get("/{id}")
def get_event(
        session: SessionDep,
        id: Annotated[int, Path (description= "The ID of the event")]
) -> EventPublic:
    """Se l'evento con quel determinato ID esiste, viene restituito
        altrimenti se non esiste, viene restituito un 404"""
    event = session.get(Event, id)
    if event:
        return event
    else:
        raise HTTPException(status_code = 404, detail = "Event not found")


@router.put("/{id}")
def update_event(
        session: SessionDep,
        id: Annotated[int, Path (description= "The ID of the event to update")],
        new_event: EventCreate
):
    """Aggiorna un evento con quel determinato ID,
    se l'evento non esiste viene restituito un 404"""
    event = session.get(Event, id)
    if event:
        event.title = new_event.title
        event.description = new_event.description
        event.date = new_event.date
        event.location = new_event.location
        session.add(event)
        session.commit()
    else:
        raise HTTPException(status_code = 404, detail = "Event not found")

    return "Event update successfully"


@router.post("/{id}/register")
def register_user_to_event(
        session: SessionDep,
        id: Annotated[int, Path (description="The ID of the event to register to")],
        user: UserCreate, #riceve i dati dall'utente dal corpo della richiesta (JSON)
):
    """Registra un utente a un evento con ID specificato,
    se l'evento non esiste restituisce un 404"""

    #CONTROLLO SE L'EVENTO ESISTE
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code = 404,
                            detail = "Evento non trovato")

    #CONTROLLO SE L'UTENTE ESISTE GIA' (la chiave primaria è username)
    db_user = session.get(User, user.username)
    if not db_user:
        #se non esiste lo creiamo automaticamente
        db_user = User.model_validate(user)
        session.add(db_user)
        session.flush()

    #CREO LA REGISTRAZIONE ALL'EVENTO
    #controllo se la registrazione esiste già
    registration = session.get(Registration, (user.username,id))
    if registration:
        return "Utente già registrato a questo evento"
    else:
        new_registration = Registration(username = user.username, event_id= id)
        session.add(new_registration)
        session.commit()

        return "Registrazione completata con successo"

@router.delete("/")
def delete_events(
        session: SessionDep
):
    """Elimina tutti gli eventi e tutte le registrazioni associate"""
    session.exec(delete(Registration))
    session.flush()
    session.exec(delete(Event))
    session.commit()
    return "Tutti gli eventi sono stati eliminati correttamente"


@router.delete("/{id}")
def delete_event(
        session: SessionDep,
        id: Annotated[int, Path (description="The ID of the event to delete")]
):
    """Elimina un evento con ID specificato e tutte le registrazioni associate,
    se l'evento non esiste restituisce un 404"""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code = 404, detail = "Evento non trovato")

    #Rimuovi le registrazioni collegate
    session.exec(delete(Registration).where(Registration.event_id == id))
    session.flush()  # Sincronizza subito la cancellazione nel DB

    session.delete(event)
    session.commit()
    return "Evento eliminato correttamente"

