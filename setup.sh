#!/bin/bash

# Obtener la ruta absoluta del directorio donde se encuentra este script
SCRIPT_DIR=$(dirname $(readlink -f $0))
REPO_URL="https://github.com/nleea/wh-auto.git"
BRANCH="main"

# Verifica si el directorio del proyecto existe
if [ ! -d "$SCRIPT_DIR/app" ]; then
    echo "El directorio no existe. Clonando el repositorio..."
    git clone -b $BRANCH $REPO_URL "$SCRIPT_DIR/app"
    cd "$SCRIPT_DIR/app"
else
    echo "El directorio existe. Actualizando el repositorio..."
    cd "$SCRIPT_DIR/app"
    git pull origin $BRANCH
fi

# Opcional: Crear y activar un entorno virtual
python3 -m venv app1
source app1/bin/activate

# Instalar las dependencias
pip install -r requirements.txt


# alembic revision --autogenerate -m "Add User model"
# alembic upgrade head
