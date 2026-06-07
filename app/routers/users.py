from fastapi import APIRouter, HTTPException
from app.models.user import User, UserPublic
from app.data.db import SessionDep
from sqlmodel import select


router = APIRouter(prefix="/users", tags = ["users"])
@router.get("/")
def get_all_users(session: SessionDep ) -> list[UserPublic]:

    """ Restituisce la lista di tutti gli utenti disponibili """

    users = session.exec(select(User)).all()
    return users


@router.post("/")
def add_user (session: SessionDep, user : User)-> UserPublic:

    """ Inserisce un nuovo utente nel DB se non esiste già,
     altrimenti restituisce un 400 """

    user_db = session.get(User, user.username)

    if user_db:
        raise HTTPException(status_code=400, detail= "User already exists")

    session.add(user)
    session.commit()

    return user

@router.get("/{username}")
def get_user_by_username(session: SessionDep, username: str)-> UserPublic:

    """Se l'utente con quel determinato username esiste, viene restituito
    altrimenti se non esiste, viene restituito un 404"""

    user = session.get(User, username)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")

    return user

