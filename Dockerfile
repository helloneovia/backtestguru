# Build stage pour le frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage final avec backend Python
FROM python:3.11-slim
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code backend
COPY backend/ .

# Créer le dossier static dans backend et copier le frontend buildé
RUN mkdir -p static
COPY --from=frontend-builder /app/frontend/dist ./static

# Exposer le port
EXPOSE 8000

# Démarrer l'application
CMD ["python", "main.py"]