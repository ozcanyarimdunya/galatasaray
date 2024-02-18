FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade poetry

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install --no-dev

COPY . .

CMD ["poetry", "run", "python", "-m", "galatasaray"]
