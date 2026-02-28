import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.models.database import User
from app.models.engine import get_db
from app.modules.auth.utils import validate_token

security = HTTPBearer()


def get_current_user(token=Depends(security), db=Depends(get_db)):
    current_user = validate_token(token.credentials)
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.get(User, uuid.UUID(current_user.get("id")))
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
