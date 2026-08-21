from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# Ce que le client envoie pour créer un utilisateur
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Ce que l'API renvoie en réponse (sans le mot de passe !)
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
