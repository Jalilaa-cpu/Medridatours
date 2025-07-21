<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Medridatours - Django Car Rental Website

## Project Overview
This is a Django-based car rental website for Medridatours, a Moroccan car rental agency located in Essaouira. The website serves as a dynamic catalog for rental cars and routes all bookings to WhatsApp.

## Key Features
- Car fleet display with dynamic filtering
- Homepage with hero banner and featured vehicles
- Multilingual support (French, English, Arabic)
- WhatsApp booking integration
- Contact and about pages
- Admin panel for vehicle management
- Mobile-responsive design with TailwindCSS

## Technical Stack
- **Backend**: Django 4.x
- **Database**: SQLite (development)
- **Frontend**: Django Templates + TailwindCSS
- **Multilingual**: Django i18n framework
- **Media**: Django ImageField for vehicle images
- **Static Files**: WhiteNoise for production

## Project Structure
- `core/`: Static pages (home, contact, about)
- `fleet/`: Car listings (models, views, templates)
- `templates/`: Shared templates with base.html
- `static/`: CSS/JS/Images
- `media/`: Uploaded car images
- `locale/`: Translation files

## WhatsApp Integration
- Each vehicle has a `whatsapp_link()` method that generates pre-filled booking messages
- WhatsApp number: +212629473725
- Floating WhatsApp button on all pages

## Development Guidelines
- Use Django best practices
- Follow French as default language
- Implement responsive design
- Use TailwindCSS for styling
- Ensure SEO-friendly URLs and meta tags
- Include proper error handling

## Models
- `Vehicle`: Main model for car listings with fields for name, image, transmission, fuel type, price, year, etc.
- `Testimonial`: Customer testimonials with rating system

## Admin Configuration
- Vehicle management with list display, filters, and editing
- Testimonial management
- Featured vehicle marking

## Translation
- Use `{% trans %}` tags in templates
- Use `gettext_lazy` in models and forms
- Support for French, English, and Arabic languages

## Deployment Considerations
- Configure for production with proper SECRET_KEY
- Use PostgreSQL for production database
- Set up proper ALLOWED_HOSTS and CSRF settings
- Use environment variables for sensitive data
