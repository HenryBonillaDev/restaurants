# Sistema de Gestión de Pedidos para Restaurantes

Este es un proyecto Django configurado para ejecutarse en contenedores Docker con PostgreSQL y Redis, además de integrar un trabajador de Celery para tareas asincrónicas.

## Requisitos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

- Docker
- Docker Compose

## Pasos para ejecutar la aplicación en local

### 1. Clonar el repositorio

Primero, clonar o descargar zip de este repositorio en tu máquina local si aún no lo has hecho:

```bash
https://github.com/HenryBonillaDev/restaurants.git
```

### 2. Construir y ejecutar los contenedores

```bash
docker compose up --build
```

### 3. Migrar la base de datos

```bash
docker compose exec web python manage.py migrate
```

### 4. Verifica que todo esté funcionando

[Swagger Docs](http://localhost:8000/api/docs/) en http://localhost:8000/api/docs/

### 5. Revisar y Probar

https://www.postman.com/hb1112/workspace/quick-restaurants

app logs:
```bash
docker logs django_rest -f
```

worker:
```bash
docker logs celery_worker -f
```
