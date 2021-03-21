
from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from database import get_db, database
import schemas

from repository.user import User as ModelUser


router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.on_event("startup")
async def startup():
    await database.connect()


@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# @router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.User, db: Session = Depends(get_db)):
#     """
#     criar uma conta de usuário, bas ta informa o nome, email e a senha
#     """
#     return ModelUser.create_sync(user, db)


@router.get("/", response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
async def get_users_async():
    return await ModelUser.get_all_async()


@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user_async(user: schemas.User):
    """
    criar uma conta de usuário, bas ta informa o nome, email e a senha
    """
    await ModelUser.create_async(user)
    return user


@router.get("/{user_id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
async def show_async(user_id: int):
    """
    criar uma conta de usuário, bas ta informa o nome, email e a senha
    """
    return await ModelUser.show_async(user_id)
