
import uvicorn
from fastapi import FastAPI

from database import Base, engine
from routers.user import router as router_user
from routers.product import router as router_product
from routers.authentication import router as router_auth


app = FastAPI(
	title="Wish List",
	description="Permita que seus clientes acompanhem seus produtos favoritos, adicionando-os a uma lista de desejos.",
	version="1.0.0",
)

Base.metadata.create_all(engine)


@app.get('/')
def index():
	"""
	"welcome": "Wish List",
		"documentation": "127.0.0.1:8000/docs ou 127.0.0.1:8000/redoc"
	"""
	return {
		"welcome": "Wish List",
		"documentation": "127.0.0.1:8000/docs ou 127.0.0.1:8000/redoc"
		
	}


app.include_router(router_auth)
app.include_router(router_product)
app.include_router(router_user)


if __name__ == "__main__":
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
