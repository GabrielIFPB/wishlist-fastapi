
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
	
	@staticmethod
	def bcrypt(password: str):
		return pwd_context.hash(password)
	
	@staticmethod
	def verify(user_password, request_password):
		return pwd_context.verify(request_password, user_password)
