#!/bin/bash

# --- VARIABLES ---
CONTAINER_NAME="xlm_key_generator"
SCRIPT_NAME="generate_xlm_key.py"

echo "Preparando el entorno seguro para generar claves XLM con QR..."
echo "Asegúrate de que estás DESCONECTADO de INTERNET."
sleep 3

# Paso 1: Crear un Dockerfile temporal para instalar dependencias
cat <<EOF > Dockerfile.tmp
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ${SCRIPT_NAME} .
CMD ["python", "./${SCRIPT_NAME}"]
EOF

# Paso 2: Crear el archivo requirements.txt
cat <<EOF > requirements.txt
stellar-sdk
cryptography
qrcode[terminal] # Instala qrcode y la funcionalidad para terminal
EOF

# Paso 3: Construir la imagen del contenedor (sin conexión a internet, usará la imagen base ya descargada)
echo "Construyendo la imagen del contenedor (puede tardar unos segundos)..."
docker build -t ${CONTAINER_NAME}_image -f Dockerfile.tmp .

# Paso 4: Eliminar los archivos temporales de construcción
rm Dockerfile.tmp requirements.txt

# Paso 5: Arrancar el contenedor sin red y en modo interactivo
echo "Lanzando el contenedor en modo seguro (sin red)..."
echo "Sigue las instrucciones dentro del contenedor para generar las claves y los QRs."
docker run --rm -it --network none \
  --name ${CONTAINER_NAME} \
  ${CONTAINER_NAME}_image

echo "El contenedor ha finalizado y se ha borrado."
echo "¡Recuerda que si no has impreso y verificado las claves, tendrás que repetir el proceso!"
