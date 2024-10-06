FROM python:3.12.2
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

WORKDIR /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser
USER appuser

COPY --chown=appuser src/. .

CMD ["python", "main.py"]
