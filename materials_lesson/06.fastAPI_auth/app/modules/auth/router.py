from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.user_schema import UserLogin, UserRequest
from app.models.engine import get_db
from app.modules.auth.utils import hash_password, is_password_valid, generate_token
from app.models.database import User

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(body: UserRequest, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(body.password)
        new_user = User(
            name=body.name, email=body.email, password=hashed_password, role=body.role
        )
        db.add(new_user)
        db.commit()
    except IntegrityError as err:
        print(err)
        raise HTTPException(status.HTTP_409_CONFLICT, detail="user already exists !")
    except Exception as err:
        print(err)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Bad request !")

    return {"Message": "User registered success", "Data": new_user}


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: UserLogin, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == body.email)).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credential")

    if not is_password_valid(body.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credential")

    # give token if success login
    token = generate_token({"id": str(user.id)})

    return {"Message": "User login success", "token": token}
