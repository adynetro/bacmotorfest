# BAC Motorfest

A modern, responsive website for BAC Motorfest motorcycle event featuring event information, photo galleries, registration, and contact functionality.

## Features

- **Event Management**: Display event details, date, and location
- **Photo Galleries**: Browse photos from previous editions with lightbox viewer
- **Event Registration**: Form-based registration with database storage and admin confirmation
- **Contact Forms**: Get in touch with automatic message storage
- **Admin Panel**: Manage all content through Django admin interface
  - Upload and organize gallery photos
  - Manage event registrations and status
  - View contact messages
  - Edit event information
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **Production Ready**: Configured for deployment on Debian/Proxmox with Nginx + Gunicorn

## Technology Stack

- **Backend**: Django 5.0.6 (Python)
- **Frontend**: Bootstrap 5 with Lightbox2 for galleries
- **Database**: SQLite3
- **Server**: Gunicorn + Nginx
- **OS**: Debian 12+

## Quick Start (Development)

### Prerequisites
- Python 3.9+
- pip and venv

### Installation

```bash
# Clone repository
git clone <repository_url>
cd bacmotorfest

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit:
- Home: http://localhost:8000
- Gallery: http://localhost:8000/gallery
- Registration: http://localhost:8000/registration
- Contact: http://localhost:8000/contact
- Admin: http://localhost:8000/admin

## Admin Credentials

Default superuser created during setup:
- Username: `admin`
- Password: Set during `createsuperuser` command
- URL: `/admin`

## Admin Tasks

### Adding Events
1. Go to Admin → Events
2. Click "Add Event"
3. Fill in title, description, date, location, and contact info
4. Toggle "Registration Open" to enable/disable registrations

### Managing Photo Galleries
1. Go to Admin → Galleries
2. Click "Add Gallery"
3. Set title and year, add description (optional)
4. In "Images" section, click "Add another Image"
5. Upload photo, add caption (optional), set order
6. Check "Published" to make gallery visible on website

### Managing Registrations
1. Go to Admin → Registrations
2. View all registrations with name, email, status
3. Click to edit and change status (Pending, Confirmed, Cancelled)
4. Search by name or email

### Managing Messages
1. Go to Admin → Messages
2. View contact form submissions
3. Mark as read/unread
4. Delete old messages as needed

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

### Quick Overview
- Deploy on Debian LXC with Nginx + Gunicorn
- SQLite database (backed up regularly)
- SSL certificate (Let's Encrypt recommended)
- Automatic service management with systemd

## File Structure

```
bacmotorfest/
├── manage.py
├── requirements.txt
├── DEPLOYMENT.md
├── README.md
├── motorfest/              # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin customization
│   ├── urls.py            # URL routing
│   ├── templates/         # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── gallery.html
│   │   ├── registration.html
│   │   └── contact.html
│   └── static/            # CSS, JS, images
├── media/                 # User-uploaded files (galleries)
└── venv/                  # Virtual environment
```

## Customization

### Edit Event Information
All content is editable through the admin panel:
- Go to Admin → Events
- Update title, description, date, location
- Changes appear immediately on website

### Customize Design
- Main styles in `core/templates/base.html` (CSS section)
- Bootstrap 5 classes used throughout
- Modify colors by changing CSS variables: `--primary-color`, `--secondary-color`

### Add New Pages
1. Create new template in `core/templates/`
2. Create view in `core/views.py`
3. Add URL pattern in `core/urls.py`

## Support

For deployment help or questions, see DEPLOYMENT.md or check the admin panel documentation.

---

**Note**: This project uses SQLite by default. For large-scale production, consider PostgreSQL. Contact information is available through the admin panel.
