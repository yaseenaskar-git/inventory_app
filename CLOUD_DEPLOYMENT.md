# Cloud Deployment Guide - Inventory App

This guide explains how to deploy your Inventory App to Google Cloud.

## Prerequisites

- Google Cloud Project (with billing enabled)
- `gcloud` CLI installed
- Docker installed locally

## Option 1: Cloud Run (Easiest - Recommended)

### 1. Setup GCP Project

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable sql.googleapis.com
```

### 2. Create Cloud SQL Database

```bash
# Create PostgreSQL instance
gcloud sql instances create inventory-db \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create inventory_db \
  --instance=inventory-db

# Create user
gcloud sql users create inventory_user \
  --instance=inventory-db \
  --password=YOUR_SECURE_PASSWORD
```

### 3. Update Django Settings

Edit `inventory_app/settings.py` to detect Cloud Run environment:

```python
import os

# Cloud SQL connection
if os.getenv('CLOUD_SQL_CONNECTION_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'inventory_db'),
            'USER': os.getenv('DB_USER', 'inventory_user'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': f'/cloudsql/{os.getenv("CLOUD_SQL_CONNECTION_NAME")}',
            'PORT': '5432',
        }
    }
else:
    # Local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Allowed hosts for Cloud Run
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    os.getenv('ALLOWED_HOST', 'localhost'),
]

# Debug mode
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Secret key from environment
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
```

### 4. Create `.env.production` (for local reference)

```bash
DEBUG=False
SECRET_KEY=your-very-secure-key-here
ALLOWED_HOST=your-app-name.run.app
DB_NAME=inventory_db
DB_USER=inventory_user
DB_PASSWORD=your-secure-password
CLOUD_SQL_CONNECTION_NAME=project-id:region:instance-name
```

### 5. Deploy to Cloud Run

```bash
# Deploy using gcloud
gcloud run deploy inventory-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated \
  --set-env-vars=DEBUG=False \
  --set-env-vars=SECRET_KEY=your-secret-key \
  --set-env-vars=ALLOWED_HOST=your-app-name.run.app \
  --set-env-vars=DB_NAME=inventory_db \
  --set-env-vars=DB_USER=inventory_user \
  --set-env-vars=DB_PASSWORD=your-password \
  --set-env-vars=CLOUD_SQL_CONNECTION_NAME=project-id:region:inventory-db
```

### 6. Run Migrations

```bash
gcloud run tasks create migrate-task \
  --service=inventory-app \
  --command='python manage.py migrate'
```

## Option 2: Kubernetes on GKE

### 1. Create GKE Cluster

```bash
gcloud container clusters create inventory-cluster \
  --zone=us-central1-a \
  --num-nodes=2 \
  --machine-type=n1-standard-1
```

### 2. Deploy using cloudbuild.yaml

```bash
gcloud builds submit --config cloudbuild.yaml
```

### 3. Get Service IP

```bash
kubectl get service inventory-app-service
```

## Option 3: Manual Docker Push & Deploy

### 1. Build and Push Image

```bash
# Build image
docker build -t gcr.io/$PROJECT_ID/inventory-app .

# Configure Docker authentication
gcloud auth configure-docker

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/inventory-app
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy inventory-app \
  --image gcr.io/$PROJECT_ID/inventory-app \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars=CLOUD_SQL_CONNECTION_NAME=project:region:db
```

## Environment Variables

Set these via Cloud Run console or gcloud:

| Variable | Description |
|----------|-------------|
| `DEBUG` | Set to `False` for production |
| `SECRET_KEY` | Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ALLOWED_HOST` | Your Cloud Run URL |
| `CLOUD_SQL_CONNECTION_NAME` | Format: `project:region:instance` |
| `DB_NAME` | `inventory_db` |
| `DB_USER` | `inventory_user` |
| `DB_PASSWORD` | Your secure password |

## Monitoring

```bash
# View logs
gcloud run logs read inventory-app

# View service details
gcloud run services describe inventory-app

# View metrics
gcloud monitoring dashboards list
```

## Cleanup

```bash
# Delete Cloud Run service
gcloud run services delete inventory-app

# Delete Cloud SQL instance
gcloud sql instances delete inventory-db

# Delete GKE cluster (if using)
gcloud container clusters delete inventory-cluster
```

## Security Best Practices

1. **Never commit secrets** - Use Cloud Secret Manager
2. **Enable VPC connectors** - Secure database access
3. **Use managed SSL** - Cloud Run provides free SSL
4. **Enable Cloud Armor** - DDoS protection
5. **Set up monitoring & alerts** - Track errors and performance

## Cost Estimation

- **Cloud Run:** ~$0.00002/request + compute time
- **Cloud SQL:** ~$10-50/month for micro instance
- **Cloud Storage:** ~$0.02/GB/month for backups

## Troubleshooting

### Database Connection Issues
```bash
gcloud sql connect inventory-db \
  --user=inventory_user
```

### View Build Logs
```bash
gcloud builds log --stream
```

### Check Cloud Run Logs
```bash
gcloud run logs read inventory-app --limit 50
```

## Next Steps

1. Set up Cloud SQL backups
2. Configure Cloud Monitoring
3. Set up CI/CD pipeline with Cloud Build
4. Enable Cloud Armor for DDoS protection
5. Configure custom domain
