
import shutil
import uuid
from typing import List, Optional
from fastapi import APIRouter, status, Depends, Response, UploadFile, File, Form
from sqlalchemy.orm import Session

from database import get_db
from repository.product import Product as ModelProduct
import schemas
from oauth2 import get_current_user

router = APIRouter(
	prefix="/wishlist",
	tags=["WishList"]
)


def filename(image: UploadFile):
	file_location = ""
	if image:
		file_location = f"media/{uuid.uuid4()}." + image.filename.split(".")[1]
		with open(file_location, "wb+") as file_object:
			shutil.copyfileobj(image.file, file_object)
	return file_location

# sync
# @router.get('/', response_model=List[schemas.ShowProduct],)
# def get_all(db: Session = Depends(get_db), user: schemas.LoginUser = Depends(get_current_user)):
# 	"""
# 	retorna todos os desejos de um usuário ou uma lista vazia.
# 	"""
# 	return ModelProduct.get_all(db, user)


# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowProduct)
# def create(
# 		title: str,
# 		description: Optional[str] = None,
# 		link: Optional[str] = None,
# 		image: UploadFile = File(None),
# 		db: Session = Depends(get_db), user: schemas.LoginUser = Depends(get_current_user)
# ):
# 	"""
# 	criar um item para lista de desejos.
# 	"""
# 	file_location = filename(image)
# 	product = schemas.Product(title=title, description=description, link=link, image=file_location)
# 	return ModelProduct.create(product, db, user)


# @router.get('/{wish_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowProduct)
# def show(wish_id, db: Session = Depends(get_db), user: schemas.LoginUser = Depends(get_current_user)):
# 	"""
# 	retorna o item selecionado pelo id, caso o item não exista retorna 404 not found.
# 	"""
# 	return ModelProduct.show(wish_id, db, user)


# @router.put('/{wish_id}', status_code=status.HTTP_202_ACCEPTED)
# def update(
# 		wish_id, product: schemas.Product,
# 		db: Session = Depends(get_db), user: schemas.LoginUser = Depends(get_current_user)):
# 	"""
# 	atualiza os dados do item selecionado pelo id, caso o item não exista retorna 404 not found.
# 	"""
# 	return ModelProduct.update(wish_id, product, db, user)


# @router.delete('/[wish_id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete(wish_id, db: Session = Depends(get_db), user: schemas.LoginUser = Depends(get_current_user)):
# 	"""
# 	deleta o item pelo id, caso o item não exista retorna 404 not found.
# 	"""
# 	ModelProduct.delete(wish_id, db, user)
# 	return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.patch('/buy/{wish_id}', status_code=status.HTTP_202_ACCEPTED)
# def buy(wish_id, win: bool, db: Session = Depends(get_db), user: schemas.LoginUser = Depends(get_current_user)):
# 	"""
# 	Endpoint para o usuário informar se já comprou o item, passando o id e um valor para buy boolean
# 	(False -> falso, True -> verdadeiro)
# 	"""
# 	return ModelProduct.buy(wish_id, win, db, user)


# @router.get('/wish-random/', response_model=schemas.ShowProduct, status_code=status.HTTP_200_OK)
# def wish_random(db: Session = Depends(get_db), user: schemas.LoginUser = Depends(get_current_user)):
# 	"""
# 	retorna um item da lista de forma aleatória
# 	"""
# 	return ModelProduct.show_random(db, user)


""" usando async """


@router.get("/", response_model=List[schemas.Product], )
async def get_all_async(user: schemas.LoginUser = Depends(get_current_user)):
	"""
	retorna todos os desejos de um usuário ou uma lista vazia.
	"""
	return await ModelProduct.get_all_async(user.id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
async def create_async(
		title: str,
		description: Optional[str] = None,
		link: Optional[str] = None,
		image: UploadFile = File(None),
		user: schemas.LoginUser = Depends(get_current_user)
):
	"""
	criar um item para lista de desejos.
	"""
	file_location = filename(image)
	product = schemas.Product(
		title=title, description=description, link=link, image=file_location)
	return await ModelProduct.create_async(product, user.id)


@router.get("/{wish_id}", status_code=status.HTTP_200_OK, response_model=schemas.Product)
async def show_async(wish_id: int, user: schemas.LoginUser = Depends(get_current_user)):
	"""
	retorna o item selecionado pelo id, caso o item não exista retorna 404 not found.
	"""
	return await ModelProduct.show_async(wish_id, user.id)


@router.put("/{wish_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_async(
		wish_id: int,
		title: str,
		description: Optional[str] = None,
		link: Optional[str] = None,
		image: UploadFile = File(None),
		user: schemas.LoginUser = Depends(get_current_user)
):
	"""
	atualiza os dados do item selecionado pelo id, caso o item não exista retorna 404 not found.
	"""
	
	modelProduct = ModelProduct()
	file_location = filename(image)
	product = schemas.Product(
		title=title, description=description, link=link, image=file_location)
	return await modelProduct.update_async(wish_id, user.id, product)


@router.delete("/[wish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_async(wish_id: int, user: schemas.LoginUser = Depends(get_current_user)):
	"""
	deleta o item pelo id, caso o item não exista retorna 404 not found.
	"""
	modelProduct = ModelProduct()
	await modelProduct.delete_async(wish_id, user.id)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{wish_id}/buy", status_code=status.HTTP_202_ACCEPTED)
async def buy_async(wish_id: int, win: bool, user: schemas.LoginUser = Depends(get_current_user)):
	"""
	Endpoint para o usuário informar se já comprou o item, passando o id e um valor para buy boolean
	(False -> falso, True -> verdadeiro)
	"""
	modelProduct = ModelProduct()
	return await modelProduct.buy_async(wish_id, win, user.id)


@router.get("/wish-random/", response_model=schemas.Product, status_code=status.HTTP_200_OK)
async def wish_random_async(user: schemas.LoginUser = Depends(get_current_user)):
	"""
	retorna um item da lista de forma aleatória
	"""
	return await ModelProduct.show_random_async(user.id)
