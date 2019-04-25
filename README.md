
# **Sistema de Presentación de Declaraciones Patrimonial y de Intereses la Ciudad de México y demás Sujetos Obligados**
El Sistema de Presentación de Declaraciones Patrimonial y de Intereses de la Ciudad de México y demás sujetos obligados, es una herramienta de software desarrollada por la Agencia Digital de Innovación Pública de la CDMX, con el fin de ayudar a cumplir a todo funcionario público –independientemente del Poder y ámbito en el que se desempeñe– con su obligación de presentar sus declaraciones en el tiempo y forma que indica la Ley.
## Inicio
Instalar Docker Engine
<https://docs.docker.com/engine/installation/>.</br>
Instalar Docker Compose
<https://docs.docker.com/compose/install/>.</br>

Obtener la última versión del proyecto:
```bash
$ git clone https://github.com/adip-cdmx/adip-declaraciones-django.git
```

## Instalación
Crear y editar los archivos de configuración.

Variables de Docker  
 ```bash
 $ cp .env.example .env
 ```

Docker Compose
```bash
$ cp docker-compose.yml.example docker-compose.yml
```

Nginx
```bash
$ cp nginx/conf/default.conf.example nginx/conf/default.conf
```

Django
```bash
$ cp declaraciones/.env.example declaraciones/.env
```

Ejecutar docker-compose para iniciar los contenedores:
```bash
$ docker-compose up -d
```
## Webpack
Requerimientos

 - [Node JS](https://nodejs.org/en/)

Entrar al directorio del proyecto
```bash
$ cd declaraciones
```
Instalar dependencias
```bash
$ npm install
```
Compilar proyecto
```bash
$ npm run build
```
Mostrar los cambios en el proyecto
```bash
$ docker-compose restart
```


## Referencia de imágenes de Docker

| Nombre   | Imagen                             |
| -------- | ---------------------------------- |
| Nginx    | <https://hub.docker.com/_/nginx/>  |
| MySQL    | <https://hub.docker.com/_/mysql/>  |
| Redis    | <https://hub.docker.com/_/redis/>  |
| Python   | <https://hub.docker.com/_/python/> |
