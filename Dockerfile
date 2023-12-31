# Usar una imagen base de Python 3.9
FROM python:3.10-slim

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de requisitos y instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el directorio actual al contenedor en /app
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]
