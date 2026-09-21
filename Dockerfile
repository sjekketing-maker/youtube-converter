FROM python:3.11

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y ffmpeg wget
RUN wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
RUN chmod a+rx /usr/local/bin/yt-dlp

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "server.py"]
