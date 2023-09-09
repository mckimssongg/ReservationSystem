# Sistema de Reserva de Asientos

## Descripción

Este proyecto implementa un sistema de reserva de asientos para teatros o cines. La API permite a los usuarios reservar, cancelar y consultar el estado de los asientos.

## Estructura del Proyecto

```
.
├── app/                           # Carpeta principal de la aplicación
│   ├── application/               # Lógica de la aplicación
│   ├── domain/                    # Modelos de dominio
│   ├── infrastructure/            # Rutas y controladores
│   ├── repository/                # Repositorio y acceso a la base de datos
│   └── utils/                     # Utilidades como el logger
├── create_app.py                  # Archivo para crear y configurar la aplicación Flask
├── docker-compose.yml             # Archivo de Docker Compose
├── Dockerfile                     # Dockerfile
├── logs/                          # Logs de la aplicación
├── requirements.txt               # Dependencias del proyecto
├── run.py                         # Archivo para ejecutar la aplicación
└── test/                          # Tests de la aplicación
```

## Cómo levantar la API

1. **Construir la imagen de Docker:**

    ```bash
    docker-compose build
    ```

2. **Levantar el contenedor:**

    ```bash
    docker-compose up
    ```

La API debería estar corriendo en `http://localhost:5000`.

## Cómo correr los tests

Para ejecutar los tests, puedes utilizar el siguiente comando desde la raíz del proyecto:

```bash
python -m unittest discover -s test/
```

## Logs

Los logs de la aplicación se guardan en la carpeta "logs/".