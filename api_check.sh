#!/bin/zsh
# Примеры проверки API из Terminal на macOS.
BASE="http://127.0.0.1:8000/api"

echo "1. Список товаров, 3 записи на странице"
curl -s "$BASE/products/?page_size=3"

echo "\n\n2. Поиск товара по названию"
curl -s "$BASE/products/?search=Nova"

echo "\n\n3. Детали товара №1"
curl -s "$BASE/products/1/"

echo "\n\nДля POST/PUT/PATCH/DELETE используйте сотрудника Django:"
echo "curl -u admin:ПАРОЛЬ -X POST ..."
