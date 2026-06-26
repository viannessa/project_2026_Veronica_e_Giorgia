from fastapi import APIRouter, HTTPException
from app.models.registration import Registration, RegistrationPublic
from app.models.user import User
from app.models.event import Event
from app.data.db import SessionDep
from sqlmodel import select


router = APIRouter(prefix="/registrations")
@router.get("/")
def get_all_registrations(session: SessionDep ) -> list[RegistrationPublic]:
    """ Restituisce la lista di tutte le registrazioni esistenti """
    registration = session.exec(select(Registration)).all()
    return registration

@router.delete("/")
def delete_registration(username: str, event_id: int, session: SessionDep):
    """Elimina una singola registrazione identificata tramite query parameter.
    Si verifica come prima cosa che l'utente e l'evento esistano, se esistono
    si procede a cercare la registrazione in questione e se anche quest'ultima
    esiste, si procede a eliminarla"""
    if not session.get(User, username):
        raise HTTPException(status_code=404, detail="Utente non trovato")

    if not session.get(Event, event_id):
        raise HTTPException(status_code=404, detail="Evento non trovato")

    statement = select(Registration).where(
        Registration.username == username,
        Registration.event_id == event_id
    )
    registration = session.exec(statement).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registrazione non trovata")

    session.delete(registration)
    session.commit()

    return "Registrazione eliminata correttamente"