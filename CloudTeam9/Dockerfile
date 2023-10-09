FROM python:3.8-slim-buster

WORKDIR /CloudTeam9

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS /app/app-key.json

EXPOSE 0000
CMD ["python3", "main.py"]
