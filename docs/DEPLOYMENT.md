# Deployment Guide

This document provides instructions for deploying the WebCurso application to production environments.

## Deployment Architecture

WebCurso follows a client-server architecture:
- **Frontend**: Vue.js application served as static files
- **Backend**: Flask API running on a WSGI server
- **Database**: SQLite database file

## Prerequisites

### Production Server Requirements

- Python 3.7 or higher
- Node.js 14 or higher
- Web server (Nginx, Apache, etc.)
- WSGI server (Gunicorn, uWSGI, Waitress, etc.)
- SSL certificate (Let's Encrypt recommended)

### Domain and DNS

- Registered domain name
- DNS records pointing to your server
- SSL certificate for HTTPS

## Backend Deployment

### 1. Server Setup

1. Create a dedicated user for the application:
   ```bash
   sudo useradd -r -s /bin/false webcurso
   ```

2. Create application directory:
   ```bash
   sudo mkdir -p /var/www/webcurso
   sudo chown webcurso:webcurso /var/www/webcurso
   ```

### 2. Application Installation

1. Clone or copy the application files to the server:
   ```bash
   sudo -u webcurso cp -r /path/to/local/webcurso/* /var/www/webcurso/
   ```

2. Install Python dependencies:
   ```bash
   cd /var/www/webcurso/backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

### 3. WSGI Server Configuration

#### Using Gunicorn (Linux/macOS)

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Create a Gunicorn configuration file (`gunicorn.conf.py`):
   ```python
   bind = "127.0.0.1:5000"
   workers = 4
   worker_class = "sync"
   timeout = 30
   max_requests = 1000
   max_requests_jitter = 100
   ```

3. Start Gunicorn:
   ```bash
   gunicorn -c gunicorn.conf.py app:app
   ```

#### Using Waitress (Windows)

1. Install Waitress:
   ```bash
   pip install waitress
   ```

2. Start Waitress:
   ```bash
   waitress-serve --host=127.0.0.1 --port=5000 app:app
   ```

### 4. Systemd Service (Linux)

Create a systemd service file (`/etc/systemd/system/webcurso.service`):

```ini
[Unit]
Description=WebCurso Flask Application
After=network.target

[Service]
User=webcurso
Group=webcurso
WorkingDirectory=/var/www/webcurso/backend
Environment=PATH=/var/www/webcurso/backend/venv/bin
ExecStart=/var/www/webcurso/backend/venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable webcurso
sudo systemctl start webcurso
```

## Frontend Deployment

### 1. Build Production Files

1. Navigate to the frontend directory:
   ```bash
   cd /var/www/webcurso/frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Build production files:
   ```bash
   npm run build
   ```

This will create a `dist/` directory with optimized static files.

### 2. Serve Static Files

The built frontend files need to be served by a web server. Options include:

#### Using Nginx

Create an Nginx configuration file (`/etc/nginx/sites-available/webcurso`):

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect all HTTP requests to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;

    # Serve frontend static files
    location / {
        root /var/www/webcurso/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to Flask backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/webcurso /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Using Apache

Create an Apache virtual host configuration:

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /path/to/ssl/cert.pem
    SSLCertificateKeyFile /path/to/ssl/key.pem

    # Serve frontend static files
    DocumentRoot /var/www/webcurso/frontend/dist

    # Proxy API requests to Flask backend
    ProxyPreserveHost On
    ProxyPass /api/ http://127.0.0.1:5000/api/
    ProxyPassReverse /api/ http://127.0.0.1:5000/api/

    # Handle SPA routing
    <Directory /var/www/webcurso/frontend/dist>
        RewriteEngine On
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteRule ^.*$ /index.html [L,QSA]
    </Directory>
</VirtualHost>
```

## Database Configuration

### Production Database Settings

For production environments, consider using a more robust database solution:

1. **SQLite Optimization**:
   - Ensure proper file permissions
   - Set up regular backups
   - Monitor database size

2. **Migration to PostgreSQL/MySQL** (Optional):
   - Update `config.py` with new database settings
   - Modify `database.py` to support the new database
   - Update `init_db.py` with appropriate schema

### Backup Strategy

Implement a regular backup strategy:

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/webcurso"
DB_FILE="/var/www/webcurso/backend/instance/database.sqlite"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/database_backup_$DATE.sqlite
gzip $BACKUP_DIR/database_backup_$DATE.sqlite

# Keep only last 30 days of backups
find $BACKUP_DIR -name "database_backup_*.sqlite.gz" -mtime +30 -delete
```

Schedule with cron:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

## Security Configuration

### SSL/TLS Setup

1. Obtain SSL certificate using Let's Encrypt:
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

2. Configure automatic renewal:
   ```bash
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

### Firewall Configuration

Configure firewall rules:
```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### Environment Variables

Set environment variables for production:
```bash
# In /etc/environment or application service file
export FLASK_ENV=production
export SECRET_KEY="your-secret-key"
```

## Monitoring and Logging

### Application Logging

Configure logging in `app.py`:
```python
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
```

### Log Rotation

Configure log rotation (`/etc/logrotate.d/webcurso`):
```
/var/log/webcurso/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 webcurso webcurso
}
```

### Monitoring Tools

Consider implementing:
- Application performance monitoring (APM)
- Uptime monitoring
- Error tracking (Sentry, etc.)
- Resource monitoring (CPU, memory, disk)

## Scaling Considerations

### Horizontal Scaling

For high-traffic applications:
1. Use a load balancer
2. Deploy multiple backend instances
3. Use a shared database or database cluster
4. Implement caching (Redis, Memcached)

### Vertical Scaling

For increased capacity on a single server:
1. Add more CPU and memory
2. Optimize database queries
3. Implement caching
4. Use a more powerful WSGI server

## Deployment Validation

### Health Checks

1. Verify backend API is responding:
   ```bash
   curl -f http://localhost:5000/api/health
   ```

2. Verify frontend is serving files:
   ```bash
   curl -f http://yourdomain.com
   ```

3. Test database connectivity:
   ```bash
   # Check if database file exists and is readable
   ls -la /var/www/webcurso/backend/instance/database.sqlite
   ```

### Smoke Tests

Perform basic functionality tests:
1. Create a test course
2. Mark lessons as completed
3. Verify progress tracking
4. Delete the test course

### Performance Testing

Run basic performance tests:
1. Test API response times
2. Verify concurrent user handling
3. Check resource utilization

## Troubleshooting

### Common Issues

1. **Permission Errors**:
   - Ensure proper file ownership and permissions
   - Check directory access rights

2. **Database Connection Issues**:
   - Verify database file permissions
   - Check database path in configuration

3. **API Errors**:
   - Check backend logs
   - Verify WSGI server configuration

4. **Frontend Issues**:
   - Verify static file serving
   - Check browser console for errors

### Log Locations

- Backend logs: `/var/log/webcurso/`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`

### Debugging Steps

1. Check service status:
   ```bash
   sudo systemctl status webcurso
   ```

2. Check application logs:
   ```bash
   sudo journalctl -u webcurso -f
   ```

3. Test API endpoints:
   ```bash
   curl http://localhost:5000/api/health
   ```

## Maintenance

### Regular Tasks

1. **Database backups**: Daily
2. **Log rotation**: Automatic
3. **Security updates**: Weekly
4. **Performance monitoring**: Continuous

### Update Procedure

1. Backup current installation
2. Deploy new code
3. Run database migrations (if any)
4. Restart services
5. Verify functionality

### Rollback Plan

1. Keep previous version backups
2. Document rollback procedures
3. Test rollback process regularly

## Conclusion

This deployment guide provides a comprehensive approach to deploying WebCurso in a production environment. Following these guidelines will help ensure a stable, secure, and performant deployment.

Remember to:
- Test thoroughly in a staging environment first
- Monitor application performance after deployment
- Implement proper backup and recovery procedures
- Keep all components updated with security patches