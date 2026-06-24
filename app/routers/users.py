from fastapi import APIRouter, HTTPException
from app.models.user import User, UserPublic, UserCreate
from app.models.registration import Registration
from app.data.db import SessionDep
from sqlmodel import select, delete


router = APIRouter(prefix="/users", tags = ["users"])
@router.get("/")
def get_all_users(session: SessionDep ) -> list[UserPublic]:

    """ Restituisce la lista di tutti gli utenti disponibili """

    users = session.exec(select(User)).all()
    return users


@router.post("/", response_model = UserPublic)
def add_user (session: SessionDep, user : UserCreate):

    """ Inserisce un nuovo utente nel DB se non esiste già,
     altrimenti restituisce un 400 """

    user_in = session.get(User, user.username)

    if user_in:
        raise HTTPException(status_code=400, detail= "User already exists")

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return user

@router.get("/{username}")
def get_user_by_username(session: SessionDep, username: str)-> UserPublic:

    """Se l'utente con quel determinato username esiste, viene restituito
    altrimenti se non esiste, viene restituito un 404"""

    user = session.get(User, username)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")

    return user

@router.delete("/")
def delete_all_users(session: SessionDep):

    """Elimina tutti gli utenti registrati"""

    #si eliminano prima tutte le registrazioni
    session.exec((delete(Registration)))

    #si eliminano poi tutti gli utenti
    session.exec(delete(User))
    session.commit()
    return {"message" : "All users successfully deleted"}


@router.delete("/{username}")
def delete_user(username: str, session: SessionDep):

    """Elimina l'utente con lo username indicato e tutte le sue registrazioni"""

    #si ricerca come prima cosa l'utente specifico
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    #se l'utente non esiste, si solleva l'eccezione
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #si eliminiamo prima tutte le registrazioni associate a questo username
    registration_statement = delete(Registration).where(Registration.username == username)
    session.exec(registration_statement)

    #infine si elimina l'utente
    session.delete(user)
    session.commit()

    return {"message": f"User {username} deleted successfully"}

'''FINE '''