FROM python:3.11.4

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV DISCORD_TOKEN=""

COPY . .

CMD ["python", "main.py"]