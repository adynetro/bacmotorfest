# BAC Motorfest - Deployment Guide

## Overview
This guide covers deploying BAC Motorfest on a Debian LXC container on Proxmox.

## System Requirements
- Debian 12 or later
- Python 3.9+
- SQLite3 (included with Python)
- Nginx (reverse proxy)
- Gunicorn (WSGI application server)

## Installation Steps

### 1. System Preparation

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev \
                     nginx supervisor git curl
```

### 2. Clone Repository and Setup

```bash
cd /opt
sudo git clone <repository_url> bacmotorfest
cd bacmotorfest
sudo python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Django Configuration

```bash
# Create production settings
cp motorfest/settings.py motorfest/settings_local.py

# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Update settings_local.py:
# - Set SECRET_KEY to the generated value
# - Set DEBUG = False
# - Set ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
# - Configure static files: STATIC_ROOT = '/var/www/bacmotorfest/static'
# - Configure media files: MEDIA_ROOT = '/var/www/bacmotorfest/media'
```

### 4. Database and Static Files

```bash
python manage.py migrate --settings=motorfest.settings_local
python manage.py collectstatic --noinput --settings=motorfest.settings_local
python manage.py createsuperuser --settings=motorfest.settings_local
```

### 5. Gunicorn Configuration

Create `/etc/systemd/system/gunicorn-bacmotorfest.service`:

```ini
[Unit]
Description=gunicorn daemon for BAC Motorfest
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/bacmotorfest
Environment="PATH=/opt/bacmotorfest/venv/bin"
ExecStart=/opt/bacmotorfest/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8001 \
          --timeout 60 \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          motorfest.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 6. Nginx Configuration

Create `/etc/nginx/sites-available/bacmotorfest`:

```nginx
upstream bacmotorfest {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect to HTTPS (recommended)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL certificates (configure with Let's Encrypt or your cert provider)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/bacmotorfest/static/;
        expires 30d;
    }

    location /media/ {
        alias /var/www/bacmotorfest/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://bacmotorfest;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/bacmotorfest /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Start Services

```bash
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/www/bacmotorfest

sudo systemctl daemon-reload
sudo systemctl enable gunicorn-bacmotorfest
sudo systemctl start gunicorn-bacmotorfest
sudo systemctl status gunicorn-bacmotorfest
```

### 8. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

## Production Checklist

- [ ] Update `ALLOWED_HOSTS` in settings
- [ ] Generate new `SECRET_KEY`
- [ ] Set `DEBUG = False`
- [ ] Configure database backups
- [ ] Set up SSL certificate
- [ ] Configure email for notifications
- [ ] Set up log rotation
- [ ] Configure backup strategy for media files
- [ ] Test admin panel access
- [ ] Test registration and contact forms

## Maintenance

### Database Backups
```bash
# Daily backup
0 2 * * * cd /opt/bacmotorfest && sqlite3 db.sqlite3 ".backup '/backups/bacmotorfest_$(date +\%Y\%m\%d).db'"
```

### Log Rotation
Create `/etc/logrotate.d/gunicorn-bacmotorfest`:
```
/var/log/gunicorn/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload gunicorn-bacmotorfest > /dev/null 2>&1 || true
    endscript
}
```

## Troubleshooting

### Check Gunicorn status
```bash
systemctl status gunicorn-bacmotorfest
tail -f /var/log/gunicorn/error.log
```

### Check Nginx
```bash
nginx -t
systemctl status nginx
tail -f /var/log/nginx/error.log
```

### Update code
```bash
cd /opt/bacmotorfest
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=motorfest.settings_local
python manage.py collectstatic --noinput --settings=motorfest.settings_local
systemctl restart gunicorn-bacmotorfest
```
