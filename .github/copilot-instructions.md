# Medridatours - Django Car Rental Website# Medridatours - Django Car Rental Website



## Project Overview## Project Overview

This is a Django-based car rental website for Medridatours, a Moroccan car rental agency located in Essaouira. The website serves as a dynamic catalog for rental cars and routes all bookings to WhatsApp.This is a Django-based car rental website for Medridatours, a Moroccan car rental agency located in Essaouira. The website serves as a dynamic catalog for rental cars and routes all bookings to WhatsApp.



## Key Features## Key Features

- Car fleet display with dynamic filtering- Car fleet display with dynamic filtering

- Homepage with hero banner and featured vehicles- Homepage with hero banner and featured vehicles

- Multilingual support (French, English, Arabic)- Multilingual support (French, English, Arabic)

- WhatsApp booking integration- WhatsApp booking integration

- Contact and about pages- Contact and about pages

- Admin panel for vehicle management- Admin panel for vehicle management

- Mobile-responsive design with TailwindCSS- Mobile-responsive design with TailwindCSS



## Technical Stack## Technical Stack

- **Backend**: Django 4.x- **Backend**: Django 4.x

- **Database**: SQLite (development)- **Database**: SQLite (development)

- **Frontend**: Django Templates + TailwindCSS- **Frontend**: Django Templates + TailwindCSS

- **Multilingual**: Django i18n framework- **Multilingual**: Django i18n framework

- **Media**: Django ImageField for vehicle images- **Media**: Django ImageField for vehicle images

- **Static Files**: WhiteNoise for production- **Static Files**: WhiteNoise for production



## Project Structure## Project Structure

- `core/`: Static pages (home, contact, about)- `core/`: Static pages (home, contact, about)

- `fleet/`: Car listings (models, views, templates)- `fleet/`: Car listings (models, views, templates)

- `templates/`: Shared templates with base.html- `templates/`: Shared templates with base.html

- `static/`: CSS/JS/Images- `static/`: CSS/JS/Images

- `media/`: Uploaded car images- `media/`: Uploaded car images

- `locale/`: Translation files- `locale/`: Translation files



## WhatsApp Integration## WhatsApp Integration

- Each vehicle has a `whatsapp_link()` method that generates pre-filled booking messages- Each vehicle has a `whatsapp_link()` method that generates pre-filled booking messages

- WhatsApp number: +212629473725- WhatsApp number: +212629473725

- Floating WhatsApp button on all pages- Floating WhatsApp button on all pages



## Development Guidelines## Development Guidelines

- Use Django best practices- Use Django best practices

- Follow French as default language- Follow French as default language

- Implement responsive design- Implement responsive design

- Use TailwindCSS for styling- Use TailwindCSS for styling

- Ensure SEO-friendly URLs and meta tags- Ensure SEO-friendly URLs and meta tags

- Include proper error handling- Include proper error handling



## Models## Models

- `Vehicle`: Main model for car listings with fields for name, image, transmission, fuel type, price, year, etc.- `Vehicle`: Main model for car listings with fields for name, image, transmission, fuel type, price, year, etc.

- `Testimonial`: Customer testimonials with rating system- `Testimonial`: Customer testimonials with rating system



## Admin Configuration## Admin Configuration

- Vehicle management with list display, filters, and editing- Vehicle management with list display, filters, and editing

- Testimonial management- Testimonial management

- Featured vehicle marking- Featured vehicle marking



## Translation## Translation

- Use `{% trans %}` tags in templates- Use `{% trans %}` tags in templates

- Use `gettext_lazy` in models and forms- Use `gettext_lazy` in models and forms

- Support for French, English, and Arabic languages- Support for French, English, and Arabic languages



## Deployment Considerations## Deployment Considerations

- Configure for production with proper SECRET_KEY- Configure for production with proper SECRET_KEY

- Use PostgreSQL for production database- Use PostgreSQL for production database

- Set up proper ALLOWED_HOSTS and CSRF settings- Set up proper ALLOWED_HOSTS and CSRF settings

- Use environment variables for sensitive data- Use environment variables for sensitive data
