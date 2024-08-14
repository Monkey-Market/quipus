# Usa una imagen base de Python
FROM python:3.12.2-alpine3.19

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente al directorio de trabajo
COPY . .

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]
