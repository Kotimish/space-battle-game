#!/bin/bash
set -e

KEYS_DIR="./keys"
PRIVATE="$KEYS_DIR/private.pem"
PUBLIC="$KEYS_DIR/public.pem"

# Убедимся, что если файлы существуют, они не являются директориями
if [ -d "$PRIVATE" ]; then
    echo "Ошибка: $PRIVATE — это директория, а не файл. Удалите её вручную."
    exit 1
fi
if [ -d "$PUBLIC" ]; then
    echo "Ошибка: $PUBLIC — это директория, а не файл. Удалите её вручную."
    exit 1
fi

if [ ! -f "$PRIVATE" ] || [ ! -f "$PUBLIC" ]; then
    mkdir -p "$KEYS_DIR"
    openssl genrsa -out "$PRIVATE" 2048
    openssl rsa -in "$PRIVATE" -pubout -out "$PUBLIC"
    echo "Ключи созданы в $KEYS_DIR"
else
    echo "Ключи уже существуют — пропускаем генерацию"
fi
