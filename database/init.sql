-- TODO: Crear la base de datos y configuraciones iniciales
CREATE DATABASE tienda_db

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Configurar zona horaria
SET timezone = 'America/Bogota';