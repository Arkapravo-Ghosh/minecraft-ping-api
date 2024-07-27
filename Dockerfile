FROM python:3.12
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
LABEL org.opencontainers.image.source = "https://github.com/Arkapravo-Ghosh/minecraft-ping-api"
LABEL org.opencontainers.image.description="Minecraft Server Status API Server"
LABEL org.opencontainers.image.licenses=MIT