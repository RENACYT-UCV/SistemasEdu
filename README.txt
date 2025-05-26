Sistemaedu

Es un Sistema hecho en python-django, para propósitos educativo, que permite subir videos para extraer el audio y el texto. a su vez utiliza AI para resumir el texto extraido. la AI utiliza transformer que engloba un conjunto de herramientas como pytorch, tensorflow y JAX, entre otros.

Tecnologías Usada: lenguaje de programación : python3.10 framework : django5.0.6 base de datos : mysql8 modelos preentrenados

Paquetes: Se especifica en el archivo requirements.txt

Despliegue:

Descarga e instala python3.10 Enlace web oficial: https://www.python.org/downloads/windows/ Enlace directo: https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe

Crea el entorno virtual si estas en windows: abre terminal cmd de windows python -m venv sistemaedu_env Ingresa a la carpeta(sistemaedu_env) y Activa el entorno virtual, con el siguiente comando: .\Scripts\Activate

Clona el repositorio: git clone https://github.com/Alexiotovv/sistemaedu.git

Instalar las depencias del archivo requirements.txt Ingresa a la carpeta raiz del proyecto con cd sistemaedu y ejecuta pip install -r requirements.txt Nota Importante, si tienes errores al instalar las dependecias, abre el archivo requirements y deja solamente las dependencias: asgiref==3.8.1 certifi==2024.2.2 charset-normalizer==3.3.2 crispy-bootstrap5==2024.2 decorator==4.4.2 Django==5.0.6 django-crispy-forms==2.1 filelock==3.14.0 fsspec==2024.6.0 huggingface-hub==0.23.3 idna==3.7 imageio==2.34.1 imageio-ffmpeg==0.4.9 Jinja2==3.1.4 lxml==5.2.2 MarkupSafe==2.1.5 moviepy==1.0.3 mpmath==1.3.0 mysqlclient==2.2.4 networkx==3.3 numpy==1.26.4 ..... packaging==24.1 pillow==10.3.0 proglog==0.1.10 python-docx==1.1.2 PyYAML==6.0.1 regex==2024.5.15 requests==2.32.3 safetensors==0.4.3 sentencepiece==0.2.0 SpeechRecognition==3.10.4 sqlparse==0.5.0 sympy==1.12.1 tokenizers==0.19.1 torch==2.3.1 tqdm==4.66.4 transformers==4.41.2 triton==2.3.1 typing_extensions==4.11.0 urllib3==2.2.1

Esto es porque las dependencias de AI tienen incompatibilidades en diferentes sistemas operativos, al momento de ejecutar el proyecto python te pedirá paquetes adicionales para instalar, esto lo harás con "pip install nombre_del_paquete_solicitado_por_python==version"

Terminado de instalar crear tu base de datos en el servidor hosting: con el nombre de dbsistemaedu(o el que deseas).

Hasta aquí debes tener instalados las dependencias necesarias

Te ubicas en la raiz de la carpeta donde se encuentra el archivo manage.py:

Crear archivo settings.py y copiar el contenido del archivo setting_example.py, colocar el nombre de la base de datos y las credenciales de tu base de datos, y pedir configuraciones adicionales al admin del proyecto:

11.Crear las tablas en la base de datos ejecutando: python manage.py makemigrations python manage.py migrate

Crear superusuario con el comando: python manage.py createsuperuser Te pedirá datos: nombreusuario, correo, contraseña, nuevamente contraseña
Crear procedimiento almacenado en la db: CREATE PROCEDURE spReproducciones() BEGIN SELECT cv.nombre as 'nombre', sum(cv.reproducciones) as 'reproducciones' from cargarcontenido_video cv group by cv.nombre; END
Ejecutar el servidor django, con el comando: python manage.py runserver
abrir el proyecto en un navegador en la url: Para administrador: localhost:8000/login Para estudiantes: localhost:8000/login_estudiante
url para superusuario: localhost:8000/admin
Crear Grupos de usuarios y agregar usuarios a los grupos en el django admin: Grupos: Admin y Estudiante También puedes usar la opción de gestión de usuarios.
Notas Importantes: Para correr el servidor e instalar todas las dependencias, debe estar activado el entorno virtual. Los vídeos cargados no deben superar los 4 minutos, por motivos de recursos de hardware, si se desea subir videos más grandes se debe ajustar los parámetros del modelo usado. Dado la naturaleza del proyecto educativo, el procesamiento de videos más grandes consume más recursos, y toma mucho más tiempo de procesar(extraer textos, resumir con la AI, etc), pudiendo llevar a errores.