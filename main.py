from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from database import get_db
from model import User
from schemas import UserCreate, UserOut

app = FastAPI(title="API Gestion Utilisateurs")

# Type réutilisable pour l'injection en database (évite les warnings Ruff sur Depends)
DBSession = Annotated[Session, Depends(get_db)]


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: DBSession):
    # Vérifier si l'email OU le nom d'utilisateur existe déjà
    stmt = select(User).where(
        or_(User.email == user_in.email, User.name == user_in.name)
    )
    existing_user = db.scalar(stmt)

    if existing_user:
        if existing_user.email == user_in.email:
            detail_msg = "Un utilisateur avec cet email existe déjà."
        else:
            detail_msg = "Ce nom d'utilisateur est déjà pris."

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_msg,
        )

    # TODO : Ajouter un vrai hashage de mot de passe
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=f"hash_{user_in.password}",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: DBSession):
    # Syntax SQLAlchemy 2.0 (select + db.scalar)
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé.",
        )

    return user


@app.get("/users", response_model=list[UserOut])
def list_users(db: DBSession, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    users = db.scalars(stmt).all()
    return users
