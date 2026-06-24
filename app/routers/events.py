'''FILE PER API CHE SI COLLEGANO ALLA SESSIONE DATABASE'''
from fastapi import APIRouter, Path, HTTPException, Query
from app.models.event import EventCreate, EventPublic, Event
from app.models.registration import Registration
from app.models.user import User, UserCreate
from typing import Annotated
from app.data.db import SessionDep
from sqlmodel import select, delete

router = APIRouter(prefix = "/events", tags = ["Events"])

#1. API 1: Restituisce la lista di tutti gli eventi esistenti
@router.get("/")
def get_all_events(
        session:SessionDep
) -> list[EventPublic]:
    """RICHIEDI LA LISTA DI TUTTI GLI EVENTI."""
    events = session.exec(select(Event)).all()
    return list(events)

#2. API 2: Crea un nuovo evento
@router.post("/")
def create_event(
        session: SessionDep,
        event: EventCreate):
    """CREA UN NUOVO EVENTO."""
    new_event = Event.model_validate(event)
    session.add(new_event)
    session.commit()
    return ("Event created successfully")


#3. API 3: Restituisce l'evento con l'id indicato
@router.get("/{id}")
def get_event(
        session: SessionDep,
        id: Annotated[int, Path (description= "The ID of the event")]
) -> EventPublic:
    """FORNISCE I DETTAGLI DI UN SINGOLO EVENTO CERCATO TRAMITE ID."""
    event = session.get(Event, id)
    if event:
        return event
    else:
        raise HTTPException(status_code = 404, detail = "Event not found")

#4. API 4: Aggiorna un evento esistente
@router.put("/{id}")
def update_event(
        session: SessionDep,
        id: Annotated[int, Path (description= "The ID of the event to update")],
        new_event: EventCreate
):
    """AGGIORNA UN EVENTO ESISTENTE."""
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

#5. API 5: Registra un utente all'evento con l'id indicato.
# Se l'utente non esiste ancora nella tabella user, viene creato automaticamente.
@router.post("/{id}/register")
def register_user_to_event(
        session: SessionDep,
        id: Annotated[int, Path (description="The ID of the event to register to")],
        user: UserCreate, #riceve i dati dall'utente dal corpo della richiesta (JSON)
):
    """REGISTRA UN UTENTE A UN EVENTO SPECIFICO"""
    #1. CONTROLLO SE L'EVENTO ESISTE
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code = 404,
                            detail = "Event not found")
    #2. CONTROLLO SE L'UTENTE ESISTE GIA' (la chiave primaria è username)
    db_user = session.get(User, user.username)
    if not db_user:
        #se non esiste lo creiamo automaticamente
        db_user = User.model_validate(user)
        session.add(db_user)
        session.flush()

    #3. CREO LA REGISTRAZIONE ALL'EVENTO
    #controllo se la registrazione esiste già
    registration = session.get(Registration, (user.username,id))
    if registration:
        return "Utente già registrato a questo evento"
    else:
        new_registration = Registration(username = user.username, event_id= id)
        session.add(new_registration)
        session.commit()

        return "Registrazione completata con successo"

#6. API 6: Elimina tutti gli eventi
@router.delete("/")
def delete_events(
        session: SessionDep
):
    """ELIMINA TUTTI GLI EVENTI DEL DATABASE."""
    session.exec(delete(Registration))
    session.flush()
    session.exec(delete(Event))
    session.commit()
    return "All events are deleted successfully"

#7. API 7: Eliminare l'evento con l'id indicato
@router.delete("/{id}")
def delete_event(
        session: SessionDep,
        id: Annotated[int, Path (description="The ID of the event to delete")]
):
    """ELIMINA UN EVENTO SPECIFICO NEL DATABASE."""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code = 404, detail = "Event not found")

    # 1. Rimuovi le registrazioni collegate
    session.exec(delete(Registration).where(Registration.event_id == id))
    session.flush()  # Sincronizza subito la cancellazione nel DB

    session.delete(event)
    session.commit()
    return "Event deleted successfully"
