FROM python:3.11-slim

# Installer ffmpeg + nodejs
RUN apt-get update && apt-get install -y ffmpeg curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "server.py"]
