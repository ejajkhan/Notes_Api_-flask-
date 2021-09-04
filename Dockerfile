FROM python:3.7-alpine

WORKDIR /program

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY src/ .

CMD ["python3", "./notesapi.py"]