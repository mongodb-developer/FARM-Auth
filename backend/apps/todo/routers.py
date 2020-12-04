from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from apps.user.models import User
from .models import TaskModel, UpdateTaskModel


def get_todo_router(app):

    router = APIRouter()

    @router.post(
        "/",
        response_description="Add new task",
    )
    async def create_task(
        request: Request,
        user: User = Depends(app.fastapi_users.get_current_active_user),
        task: TaskModel = Body(...),
    ):
        task = jsonable_encoder(task)
        new_task = await request.app.db["tasks"].insert_one(task)
        created_task = await request.app.db["tasks"].find_one(
            {"_id": new_task.inserted_id}
        )

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)

    @router.get("/", response_description="List all tasks")
    async def list_tasks(
        request: Request,
        user: User = Depends(app.fastapi_users.get_current_active_user),
    ):
        tasks = []
        for doc in await request.app.db["tasks"].find().to_list(length=100):
            tasks.append(doc)
        return tasks

    @router.get("/{id}", response_description="Get a single task")
    async def show_task(
        id: str,
        request: Request,
        user: User = Depends(app.fastapi_users.get_current_active_user),
    ):
        if (task := await request.app.db["tasks"].find_one({"_id": id})) is not None:
            return task

        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    @router.put("/{id}", response_description="Update a task")
    async def update_task(
        id: str,
        request: Request,
        user: User = Depends(app.fastapi_users.get_current_active_user),
        task: UpdateTaskModel = Body(...),
    ):
        task = {k: v for k, v in task.dict().items() if v is not None}

        if len(task) >= 1:
            update_result = await request.app.db["tasks"].update_one(
                {"_id": id}, {"$set": task}
            )

            if update_result.modified_count == 1:
                if (
                    updated_task := await request.app.db["tasks"].find_one({"_id": id})
                ) is not None:
                    return updated_task

        if (
            existing_task := await request.app.db["tasks"].find_one({"_id": id})
        ) is not None:
            return existing_task

        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    @router.delete("/{id}", response_description="Delete Task")
    async def delete_task(
        id: str,
        request: Request,
        user: User = Depends(app.fastapi_users.get_current_active_user),
    ):
        delete_result = await request.app.db["tasks"].delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    return router
