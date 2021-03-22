FROM python:3.8.5

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]