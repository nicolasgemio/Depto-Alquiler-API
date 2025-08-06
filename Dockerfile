# 1. Imagen base de Python
FROM python:3.11-slim

# 2. Instalar dependencias de sistema, gpg y driver ODBC para SQL Server
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      gnupg \
      apt-transport-https \
      ca-certificates \
      unixodbc-dev && \
    \
    # 2.1. Descarga y desarma la clave GPG de Microsoft
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc \
      | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg && \
    \
    # 2.2. Añade el repositorio de paquetes de Microsoft firmado
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
      > /etc/apt/sources.list.d/microsoft-prod.list && \
    \
    # 2.3. Instala el driver msodbcsql17
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
      msodbcsql17 && \
    \
    # 2.4. Limpia cachés de apt
    rm -rf /var/lib/apt/lists/*

# 3. Directorio de trabajo
WORKDIR /app

# 4. Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código de la aplicación
COPY . .

# 6. Exponer el puerto de Uvicorn
EXPOSE 8000

# 7. Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
