import uuid
from sqlmodel import select
from fastapi import APIRouter, Depends, status, HTTPException
from app.utils.user_schema import UserRequest
from app.models.engine import get_db
from app.models.database import User
from app.modules.auth.service import get_current_user
from app.modules.auth.utils import hash_password


def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


user_router = APIRouter(tags=["Users"])


@user_router.get("/users", status_code=status.HTTP_200_OK)
def get_users(db=Depends(get_db), admin: User = Depends(admin_required)):
    stmt = select(User)
    result = db.exec(stmt)
    users = result.all()

    return {"data": users}


@user_router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserRequest, db=Depends(get_db), admin: User = Depends(admin_required)
):
    try:
        hashed_password = hash_password(body.password)
        new_user = User(
            name=body.name, email=body.email, password=hashed_password, role=body.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "user created successfully !", "data": new_user}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: uuid.UUID, db=Depends(get_db), admin: User = Depends(admin_required)
):
    stmt = select(User).where(User.id == user_id)
    result = db.exec(stmt)
    user = result.one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(user)
    db.commit()
