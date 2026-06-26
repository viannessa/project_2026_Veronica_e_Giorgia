from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
# TODO: remember to import all the DB models here
from app.models.registration import Registration  # NOQA
from app.models.user import User # NOQA
from app.models.event import Event # NOQA

sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with (Session(engine) as session):
            # TODO: (optional) initialize the database with fake data
            # creazione dati utenti
                    users = []
                    for o in range(5):
                        user = User(
                            username=f.user_name(),
                            name=f.name(),
                            email=f.email()
                        )
                        session.add(user)
                        users.append(user)

                    # creazione dati eventi
                    events = []
                    for o in range(5):
                        event = Event(
                            title=f.catch_phrase(),
                            description=f.sentence(),
                            date=f.date_this_year(),
                            location = f.city()

                        )
                        session.add(event)
                        events.append(event)

                    # Commit necessario per assegnare gli ID dal DB agli oggetti in memoria
                    session.commit()

                    # creazione dati registrazioni

                    for user in users:
                        # Ogni utente si registra a un numero casuale di eventi (1 o 2)
                        for event in f.random_elements(elements=events, length=f.random_int(1, 2), unique=True):
                            registration = Registration(
                                username=user.username,
                                event_id=event.id
                            )
                            session.add(registration)

                    session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

