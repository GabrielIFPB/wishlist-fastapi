# Wish List wight FastApi

### Projeto foi construído com Python 3.8.5

Para executar o projeto precisa ter o python 3.8 ou superior instalado na maquina.
- download [Python](https://www.python.org/).

## Executando projeto usando virtualenv
### Requisitos
___
- Download [Virtualenv](https://pypi.org/project/virtualenv/).
- Instalação usando pip ```pipx install virtualenv```.
- Verificar a versão ```virtualenv --help```.
- Criar um ambiente virtual ```python3 -m virtualenv venv```, antes de executar o comado escolha um local para criar a pasta do virtualenv.

### Executando o virtualenv
___

- Ativando o virtualenv
```
dell@dell:~$ source source venv/bin/activate
(venv) dell@dell:~$
```

### Instalando dependência
___
No repositório tem um arquivo chamado **_requirements.txt_** com todas as dependências do projeto. Para instalar execute o comando baixo.

```
$ pip install -r requirements.txt
```

### Run 
___
```
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
### Banco de dados
___
No arquivo **_database.py_**, na linha 8 (**_DATABASE_URL_**) deve colocar a conexão com o seu banco.
<br>
Exemplo usando postgresql: "postgresql://usuário:senha@127.0.0.1/wishlist"
- trocar usuário e a senha 
### Imagem
___
Deve haver uma pasta com o nome **media** na raiz para armazenar as imagens.
## Executando projeto usando docker

## Documentação da API
___
Agora vá para [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
![Swagger UI](img/api-docs.png)

## Documentação alternativa
___
Agora vá para [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).
![Swagger UI](img/api-redoc.png)

### Lista das dependências e suas versões
___
Todas estão no arquivo **_requirements.txt_**.
- asyncpg==0.22.0
- bcrypt==3.2.0
- cffi==1.14.5
- click==7.1.2
- cryptography==3.4.6
- databases==0.4.2
- ecdsa==0.14.1
- fastapi==0.63.0
- h11==0.12.0
- passlib==1.7.4
- psycopg2-binary==2.8.6
- pyasn1==0.4.8
- pycparser==2.20
- pydantic==1.8.1
- python-jose==3.2.0
- python-multipart==0.0.5
- rsa==4.7.2
- six==1.15.0
- SQLAlchemy==1.3.23
- starlette==0.13.6
- text-unidecode==1.3
- typing-extensions==3.7.4.3
- uvicorn==0.13.4