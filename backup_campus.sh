#!/bin/bash

# === Конфігурація ===
DB_NAME="campus_db"
DB_USER="campus_user"
DB_PASSWORD="836219postgresHelloWorld!"
BACKUP_DIR="/home/oleksandr/projects/nulp/db_backups"

# === Дата для назви файлу ===
DATE=$(date +'%Y-%m-%d_%H-%M')

# === Ім'я файлу ===
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.sql"

# === Створення резервної копії ===
echo "[$(date)] Початок бекапу $DB_NAME..."
export PGPASSWORD=$DB_PASSWORD
pg_dump -U $DB_USER -h localhost $DB_NAME > "$BACKUP_FILE"

# === Перевірка результату ===
if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ Бекап створено: $BACKUP_FILE"
else
    echo "[$(date)] ❌ Помилка при створенні бекапу!"
fi

# === Видалення старих файлів старше 30 днів ===
find "$BACKUP_DIR" -type f -name "*.sql" -mtime +30 -delete

# === Логування ===
echo "[$(date)] Старі бекапи очищено (старше 30 днів)"
