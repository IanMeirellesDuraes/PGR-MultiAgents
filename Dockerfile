#FastAPI Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
WORKDIR /app

# Copie apenas o requirements.txt para o cache de dependências primeiro
COPY ./requirements.txt .

# Instale as dependências do Python
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# Copie o restante do código do app
COPY ./src ./src

EXPOSE 8080

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
