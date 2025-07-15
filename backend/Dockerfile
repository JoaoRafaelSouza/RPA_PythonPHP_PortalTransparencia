FROM python:3.11

ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ca-certificates wget curl gnupg unzip xvfb tesseract-ocr \
    libnss3 libxss1 libappindicator1 libgbm1 fonts-liberation \
    libasound2 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libu2f-udev \
    libvulkan1 xdg-utils gnupg2 software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable net-tools

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

ENV PYTHONPATH="/app"

COPY chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver