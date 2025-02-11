FROM python:3.11.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

RUN pip install poetry==1.8.3

COPY src ./src
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
