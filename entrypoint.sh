#!/bin/bash

set -e

# Esperar a la base de datos con wait-for-it
echo "Esperando a la base de datos..."
/app/wait-for-it.sh $DB_HOST:$DB_PORT --timeout=30 --strict -- echo "Base de datos disponible"

echo "Base de datos disponible."

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Crear superusuario si no existe
echo "Creando superusuario si no existe..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='mmc').exists():
    User.objects.create_superuser('mmc', 'mmc@admin.com', 'admin123')
EOF

# Crear procedimiento almacenado si no existe
echo "Verificando existencia del procedimiento almacenado..."
EXISTS=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -sse "
  SELECT COUNT(*) FROM information_schema.routines
  WHERE routine_schema = '$DB_NAME'
    AND routine_name = 'spReproducciones'
    AND routine_type = 'PROCEDURE';
")

if [ "$EXISTS" -eq 0 ]; then
  echo "Creando procedimiento almacenado..."
  mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" <<'SQL'
  DELIMITER //
  CREATE PROCEDURE spReproducciones()
  BEGIN
    SELECT cv.nombre AS nombre, SUM(cv.reproducciones) AS reproducciones
    FROM cargarcontenido_video cv
    GROUP BY cv.nombre;
  END //
  DELIMITER ;
SQL
else
  echo "El procedimiento almacenado ya existe. No se crea nuevamente."
fi

# Ejecutar el comando original (por defecto: runserver)
echo "Iniciando servidor Django..."
exec "$@"
