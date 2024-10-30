FROM python:3.12 as builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./

RUN pip install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

COPY --from=builder /opt/venv/ /opt/venv

EXPOSE 8000

CMD uvicorn --host=0.0.0.0 main:app
