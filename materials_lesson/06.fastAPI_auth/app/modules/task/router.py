import uuid
from sqlmodel import select
from fastapi import APIRouter, Depends, status, HTTPException
from app.utils.task_schema import TaskRequest, TaskUpdate
from app.models.database import Task, User
from app.models.engine import get_db
from app.modules.auth.service import get_current_user

task_router = APIRouter(tags=["Tasks"])


@task_router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    stmt = select(Task).where(Task.user_id == current_user.id)

    result = db.exec(stmt)
    tasks = result.all()

    return {"data": tasks}


@task_router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(
    body: TaskRequest,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    try:
        new_task = Task(title=body.title, user_id=current_user.id)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return {"message": "Task created successfully !", "data": new_task}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@task_router.patch("/tasks/{task_id}")
def update_task(
    task_id: uuid.UUID,
    body: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    task = db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@task_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    task = db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.delete(task)
    db.commit()
