FROM python:3.13-alpine

RUN rm -rf /opt/venv && \
    python -m venv /opt/venv && \
    source /opt/venv/bin/activate

COPY ./src/requirements.txt .
COPY ./src/ .

RUN pip install -r requirements.txt

CMD ["python3.13", "./run.py"]