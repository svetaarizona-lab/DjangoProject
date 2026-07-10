FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gettext

COPY . .

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

CMD ["sh", "docker-entrypoint.sh"]