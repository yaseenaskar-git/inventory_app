# Docker Setup Guide - Inventory Application

This guide explains how to build and run the Inventory Application using Docker.

## Prerequisites

- Docker (v20.10+)
- Docker Compose (v2.0+)

## Quick Start

### 1. Clone and Setup

```bash
cd inventory_app
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` file with your settings:

```env
DEBUG=False
SECRET_KEY=your-very-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DB_PASSWORD=your-secure-password
```

### 3. Build and Run

```bash
# Build images (first time)
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f web
```

### 4. Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access Application

- **Web Application:** http://localhost:80
- **Admin Panel:** http://localhost/admin/
- **Database:** localhost:5432

## Services

### Web Service
- **Container:** inventory_app_web
- **Port:** 8000 (internal), 80 (external via nginx)
- **Framework:** Django 5.2.8 with Gunicorn

### Database Service
- **Container:** inventory_app_db
- **Image:** PostgreSQL 16
- **Port:** 5432
- **Data Volume:** postgres_data

### Nginx Service
- **Container:** inventory_app_nginx
- **Port:** 80
- **Purpose:** Reverse proxy, static files serving

## Common Commands

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Follow logs in real-time
docker-compose logs -f web
```

### Database Management

```bash
# Create migration
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Access database shell
docker-compose exec db psql -U inventory_user -d inventory_db

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Manage Services

```bash
# Stop all services
docker-compose down

# Stop with volume cleanup
docker-compose down -v

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart web

# View running containers
docker-compose ps
```

### Shell Access

```bash
# Django shell
docker-compose exec web python manage.py shell

# Bash access to web container
docker-compose exec web bash

# Bash access to database container
docker-compose exec db bash
```

## File Structure

```
.
├── Dockerfile              # Multi-stage build configuration
├── docker-compose.yml      # Docker Compose orchestration
├── nginx.conf             # Nginx reverse proxy config
├── .dockerignore           # Files to exclude from Docker build
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database (local development)
├── staticfiles/           # Collected static files
├── media/                 # User uploads
└── inventory_app/         # Main Django project
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | False | Django debug mode |
| `SECRET_KEY` | - | Django secret key (required) |
| `ALLOWED_HOSTS` | localhost,127.0.0.1 | Allowed hostnames |
| `DB_PASSWORD` | change_me_in_production | PostgreSQL password |
| `DATABASE_URL` | Auto-generated | Full database URL |

## Volumes

- **postgres_data:** PostgreSQL database files
- **static_volume:** Collected Django static files
- **media_volume:** User-uploaded media files

## Networks

- **inventory_network:** Internal bridge network connecting all services

## Performance Optimization

### Gunicorn Workers
Currently set to 4 workers. Adjust based on CPU:
```yaml
# In docker-compose.yml
command: gunicorn --workers 8 ...  # For 8-CPU systems
```

### Nginx Caching
- Static files cached for 30 days
- Media files cached for 7 days
- Gzip compression enabled for text assets

## Production Deployment

### Before Production:

1. **Security:**
   ```bash
   # Generate strong SECRET_KEY
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Update .env:**
   - Set `DEBUG=False`
   - Set strong `SECRET_KEY`
   - Update `ALLOWED_HOSTS` with your domain
   - Set strong `DB_PASSWORD`

3. **Database Backup:**
   ```bash
   docker-compose exec db pg_dump -U inventory_user inventory_db > backup.sql
   ```

4. **SSL/TLS:**
   Add SSL certificate configuration to nginx.conf

5. **Scale Gunicorn:**
   ```bash
   # Increase workers for production
   --workers 8  # or based on your CPU cores
   ```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs web

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Database Connection Issues

```bash
# Check database is running
docker-compose ps

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

### Static Files Not Loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Check volume mounts
docker inspect inventory_app_web | grep -A 5 Mounts
```

### Permission Denied Errors

```bash
# Non-root user runs in container (UID: 1000)
# If issues persist, check volume permissions on host

# Fix permissions (Linux/Mac)
sudo chown -R $USER:$USER media/ staticfiles/
```

## Development vs Production

### Development
```bash
docker-compose up  # Use docker-compose.yml
```

### Production
- Use `docker-compose.override.yml` for environment-specific configs
- Use environment variables from `.env` file
- Consider using Docker secrets for sensitive data
- Use a production-grade database

## Backup and Restore

### Backup Database

```bash
docker-compose exec db pg_dump -U inventory_user inventory_db > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker-compose exec -T db psql -U inventory_user inventory_db
```

### Backup Media Files

```bash
docker run --rm -v inventory_app_media_volume:/media -v $(pwd):/backup \
  alpine tar czf /backup/media_backup.tar.gz /media
```

## Health Checks

All services include health checks:

```bash
# View health status
docker-compose ps

# Manual health check
curl http://localhost:80/accounts/login/
```

## License

See LICENSE file in project root.
