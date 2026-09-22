#!/bin/sh
set -e

echo "1. Containers"
docker compose ps

echo "2. Home page"
curl -fI http://localhost/

echo "3. Admin page"
curl -fI http://localhost/admin/login/

echo "4. Static file"
curl -fI http://localhost/static/css/site.css

echo "5. API"
curl -fI http://localhost/api/products/

echo "Release check completed"
