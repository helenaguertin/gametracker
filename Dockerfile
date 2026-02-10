FROM python:3.11-slim

# 1. Installation des dépendances système
RUN apt-get update && apt-get install -y \
    bash \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# 2. Dossier de travail
WORKDIR /app

# 3. Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie du projet
COPY . .

# 5. Permissions et commande de lancement
RUN chmod +x scripts/*.sh || true

CMD ["bash"]