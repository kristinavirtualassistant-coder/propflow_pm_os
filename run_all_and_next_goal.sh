#!/usr/bin/env bash
set -e

echo "🚀 --- 1. VERIFYING ALL SERVICES & EXECUTING DIAGNOSTICS --- 🚀"
python3 scripts/system_diagnostics.py

echo "💾 --- 2. EXPORTING FRESH DATABASE BACKUPS (JSON & SQL) --- 💾"
python3 backend/db_tools.py json
python3 backend/db_tools.py sql

echo "📊 --- 3. CHECKING PM2 PROCESS STATUS --- 📊"
pm2 status

echo "🐳 --- 4. MOVING TO NEXT GOAL: CONTAINERIZING WITH DOCKER & DOCKER-COMPOSE --- 🐳"

# Create Backend Dockerfile
cat << 'INNER_EOF' > backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt reportlab

COPY . /app/backend

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
INNER_EOF

# Create Frontend Dockerfile
cat << 'INNER_EOF' > web/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]
INNER_EOF

# Create Root Docker-Compose Configuration
cat << 'INNER_EOF' > docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./propflow.db:/app/propflow.db
    environment:
      - CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

  frontend:
    build:
      context: ./web
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
INNER_EOF

echo "✅ Docker build configuration created! Dockerfile (Backend), Dockerfile (Frontend), and docker-compose.yml are ready."
echo "🎉 Complete automation cycle finished successfully!"
