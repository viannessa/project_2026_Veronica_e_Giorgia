from fastapi import APIRouter
from app.models.user import User, UserPublic
from app.data.db import SessionDep
from sqlmodel import select


router = APIRouter(prefix="/users", tags = ["users"])
@router.get("/")
def get_all_users(session: SessionDep ) -> list[UserPublic]:

    """ Restituisce la lista di tutti gli utenti disponibili"""

    users = session.exec(select(User)).all()
    return users 