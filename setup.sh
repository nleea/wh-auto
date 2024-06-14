#!/bin/bash

# Obtener la ruta absoluta del directorio donde se encuentra este script
SCRIPT_DIR=$(dirname $(readlink -f $0))

# Navegar al directorio del proyecto
cd $SCRIPT_DIR

# Actualizar el repositorio
git pull origin main

# Opcional: Crear y activar un entorno virtual
python3 -m venv app1
source app1/bin/activate

# Instalar las dependencias
pip install -r requirements.txt
