#!/bin/bash
set -e

echo "🚀 Deploying vacation website..."

# Pull latest images and start
docker compose pull
docker compose up -d

echo "✅ Deployment complete!"
echo ""
echo "🌐 Access at:"
echo "  - Vacation site: http://$(curl -s ifconfig.me || echo "localhost"):8000"
echo "  - Stats dashboard: http://$(curl -s ifconfig.me || echo "localhost"):3000"
echo ""
echo "🔐 Admin login: admin@vacation.com / admin123"