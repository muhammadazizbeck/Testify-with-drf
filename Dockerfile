# 1. Pythonni o'rnatish
FROM python:3.12-slim

# 2. Ishlash katalogini o'rnatish
WORKDIR /app

# 3. Kerakli fayllarni konteynerga ko'chirish
COPY requirements.txt /app/

# 4. Sistemaning kerakli kutubxonalarini o'rnatish
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt


# 5. Djangoni ishlatish
COPY . /app/

# 6. Portni ochish
EXPOSE 8000

# 7. Django serverini ishga tushirish
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]



