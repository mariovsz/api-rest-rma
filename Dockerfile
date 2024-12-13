# Dockerfile
# Usar la imagen oficial de PostgreSQL 17
FROM postgres:17

# Cargar variables de entorno del archivo .env
COPY .env .env
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}

# Exponer el puerto de PostgreSQL
EXPOSE 5432

