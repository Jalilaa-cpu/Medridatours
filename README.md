# Medridatours - Car Rental Website

A Django-based car rental website for Medridatours, a Moroccan car rental agency located in Essaouira. The website serves as a dynamic catalog for rental cars and routes all bookings to WhatsApp.

## Features

### 🚗 Car Fleet Display
- Dynamic vehicle listing with filtering options
- Vehicle details with specifications
- Featured vehicles highlighting
- Pagination for large inventories

### 🏠 Homepage
- Hero banner with call-to-action
- Featured vehicles preview
- Advantages section with service highlights
- Customer testimonials

### 🌍 Multilingual Support
- French (default language)
- English
- Arabic
- Language switcher in navigation

### 📱 WhatsApp Integration
Direct booking flow to WhatsApp number.

- Touch-friendly interface

### 🔧 Admin Panel
- Vehicle management (CRUD operations)
- Testimonial management
- Featured vehicle marking
- Image upload for vehicles

## Technical Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Django Templates + TailwindCSS
- **Multilingual**: Django i18n framework
- **Media**: Django ImageField for uploads
- **Static Files**: WhiteNoise for production

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd medridatours
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
medridatours/
├── core/                  # Static pages (home, contact, about)
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
├── fleet/                 # Car listings
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│   └── templates/fleet/
├── templates/             # Shared templates
│   └── base.html
├── static/               # CSS/JS/Images
│   └── css/style.css
├── media/                # Uploaded files
├── locale/               # Translation files
├── medridatours/         # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## Models

### Vehicle Model
- `name`: Vehicle name
- `image`: Vehicle image
- `transmission`: Manual/Automatic
- `air_conditioning`: Boolean
- `fuel_type`: Gasoline/Diesel/Hybrid/Electric
- `daily_price`: Daily rental price in MAD
- `year`: Vehicle year
- `featured`: Featured vehicle flag
- `available`: Availability status

### Testimonial Model
- `name`: Customer name
- `location`: Customer location
- `content`: Testimonial content
- `rating`: Rating (1-5 stars)
- `active`: Active status

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
WHATSAPP_NUMBER=+212698927640
```

### Language Settings
The website supports three languages:
- French (fr) - Default
- English (en)
- Arabic (ar)

To generate translation files:
```bash
python manage.py makemessages -l en
python manage.py makemessages -l ar
python manage.py compilemessages
```

## WhatsApp Integration

Each vehicle has a `whatsapp_link()` method that generates pre-filled messages:

```python
def whatsapp_link(self):
    base_url = f"https://wa.me/212698927640"
    message = f"Bonjour Medridatours, je souhaite réserver la {self.name} du [Date début] au [Date fin]."
    return f"{base_url}?text={quote(message)}"
```

## Deployment

### Production Settings
1. Set `DEBUG=False`
2. Configure proper `SECRET_KEY`
3. Update `ALLOWED_HOSTS`
4. Use PostgreSQL database
5. Configure static files with WhiteNoise

### Deployment Platforms
- **Heroku**: Use the included `Procfile`
- **DigitalOcean**: Use App Platform
- **Render**: Configure build and start commands

### Build Commands
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

### Start Command
```bash
python manage.py runserver 0.0.0.0:$PORT
```

## Usage

### Admin Panel
1. Access `/admin/` with superuser credentials
2. Add vehicles with images and specifications
3. Mark featured vehicles
4. Manage testimonials

### Adding Vehicles
1. Go to Admin → Vehicles → Add Vehicle
2. Fill in vehicle details
3. Upload vehicle image
4. Set featured status if needed
5. Save and publish

### Managing Testimonials
1. Go to Admin → Testimonials
2. Add customer testimonials
3. Set rating (1-5 stars)
4. Activate/deactivate testimonials

## SEO Features

- Semantic HTML structure
- OpenGraph meta tags
- Proper heading hierarchy
- Mobile-friendly design
- Fast loading times
- Clean URLs

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is licensed under the MIT License.


- [ ] Implement sitemap.xml
- [ ] Add robots.txt
- [ ] Implement caching
- [ ] Add analytics integration
- [ ] Implement search functionality
- [ ] Add email notifications
