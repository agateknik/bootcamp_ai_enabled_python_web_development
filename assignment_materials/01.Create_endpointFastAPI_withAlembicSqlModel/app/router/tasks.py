import uuid
from sqlmodel import select
from gc import get_debug
from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.utils.task_schema import TaskRequest, TaskResponse, TaskUpdate
from app.models.database import Task, User
from app.models.engine import get_db

task_router = APIRouter(tags=["Tasks"])

@task_router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(user_id: uuid.UUID = Query(None, description="Filter by user ID") , 
              db = Depends(get_db)):
    
    stmt = select(Task)
    
    if user_id:
        stmt = stmt.where(Task.user_id == user_id)
        
    result = db.exec(stmt)
    tasks = result.all()
    
    return {"data": tasks}



@task_router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(body : TaskRequest, db= Depends(get_db)):
    try:
        #cek dulu user ada tidak
        user = db.exec(select(User).where(User.id == body.user_id)).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User not found")
        
        #create task
        new_task = Task(title = body.title, 
                        user_id=body.user_id)
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        return ({"message": "Task created successfullly !", 
                "data": new_task})
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=str(e))

@task_router.patch("/tasks/{task_id}")
def update_task(task_id: uuid.UUID , body: TaskUpdate, db= Depends(get_db)):
    
    #ambil task
    task = db.exec(select(Task).where(Task.id == task_id)).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task not found")
    
    #update file yang dikirim saja
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
        
@task_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id : uuid.UUID, db=Depends(get_db)):
    
    #cari task
    task = db.exec(
        select(Task).where(Task.id == task_id)
    ).first()
    
    if not task:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Task not found")
    
    #hapus task
    db.delete(task)
    db.commit()
    
        
