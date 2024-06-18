#!/bin/bash

# Charger les variables d'environnement depuis .env
export $(grep -v '^#' .env | xargs)

# Extraire les informations de connexion de DATABASE_URL
DB_PROTOCOL=$(echo $DATABASE_URL | grep -o '^[^:]*')
DB_USER=$(echo $DATABASE_URL | sed -e 's,.*//\(.*\):.*@.*,\1,g')
DB_PASSWORD=$(echo $DATABASE_URL | sed -e 's,.*//.*:\(.*\)@.*,\1,g')
DB_HOST=$(echo $DATABASE_URL | sed -e 's,.*@\(.*\):.*,\1,g')
DB_PORT=$(echo $DATABASE_URL | sed -e 's,.*:\([0-9]*\)\/.*,\1,g')
DB_NAME=$(echo $DATABASE_URL | sed -e 's,.*\/\(.*\),\1,g')

# Définir les variables d'environnement pour pg_dump
export PGHOST=$DB_HOST
export PGPORT=$DB_PORT
export PGDATABASE=$DB_NAME
export PGUSER=$DB_USER
export PGPASSWORD=$DB_PASSWORD

# Assurez-vous que l'environnement utilise UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Exécuter pg_dump avec le format plain text
pg_dump --encoding=UTF8 -Fp -v -f ventalis_backup1806.sql
