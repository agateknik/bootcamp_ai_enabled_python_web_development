import uuid
from sqlmodel import select
from fastapi import APIRouter, Depends, status, HTTPException
from app.utils.user_schema import UserRequest, UserResponse
from app.models.engine import get_db
from app.models.database import User, Task


user_router = APIRouter(tags=["Users"])

@user_router.get("/users", status_code=status.HTTP_200_OK)
def get_users(db = Depends(get_db)):
    stmt = select(User)
    result = db.exec(stmt)
    users = result.all()
    
    return {"data": users}



@user_router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(body: UserRequest,  db= Depends(get_db)):
    try:      
        new_user = User(name= body.name, email= body.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return({"message": "user created successfully !",
            "data": new_user})
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail= str(e))
        

    
    
    
    
    
    
    
    
    
        
    