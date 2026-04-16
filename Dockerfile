FROM python:3.11-slim

# Встановлюємо ffmpeg (важливо для відео)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код
COPY . .

# Railway використовує PORT, але нам він не потрібен (polling)
CMD ["python", "main.py"]
