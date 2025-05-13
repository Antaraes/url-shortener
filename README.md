# URL Shortener Service

A modern, scalable URL shortener service built with Flask.

## Features

- Shorten long URLs to easy-to-share links
- Custom short IDs
- URL expiration settings
- Click tracking and analytics
- RESTful API for integrations
- Dockerized deployment

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Deployment**: Docker, Nginx
- **Testing**: PyTest

## Installation

### Local Development Setup

1. Clone the repository:
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install development dependencies:
   pip install -r requirements/dev.txt

4. Set up environment variables (copy from example):
   cp .env.example .env

5. Initialize the database:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

6. Run the development server:
   flask run

### Docker Setup

1. Clone the repository:
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener

2. Build and run the containers:
   docker-compose -f docker/docker-compose.yml up -d

3. Initialize the database:
   docker-compose -f docker/docker-compose.yml exec web flask db upgrade

## Usage

### Web Interface

Access the web interface by visiting `http://localhost:5000` in your browser.

### API Usage

#### Shorten a URL

POST /api/v1/shorten
{
"url": "https://example.com/very/long/url/that/needs/shortening",
"custom_id": "custom", // Optional
"expiration_days": 30 // Optional
}

Response:
{
"short_url": "http://localhost:5000/custom",
"original_url": "https://example.com/very/long/url/that/needs/shortening",
"short_id": "custom",
"created_at": "2025-05-13T14:30:00",
"expires_at": "2025-06-12T14:30:00",
"visit_count": 0
}

#### Get URL Statistics

GET /api/v1/urls/{short_id}

Response:
{
"original_url": "https://example.com/very/long/url/that/needs/shortening",
"short_id": "custom",
"created_at": "2025-05-13T14:30:00",
"expires_at": "2025-06-12T14:30:00",
"visit_count": 42
}

## Testing

Run the test suite:
pytest

For coverage report:
pytest --cov=app

## Deployment

### Production Deployment

1. Update your production environment variables:
   cp .env.example .env
   Edit .env with your production settings

2. Run with production Docker Compose:
   docker-compose -f docker/docker-compose.prod.yml up -d

3. Set up SSL (if using the included Nginx configuration):
   docker-compose -f docker/docker-compose.prod.yml run --rm certbot certonly --webroot -w /var/www/certbot -d yourdomain.com

## Project Structure

The project follows a modular structure:

- `app/`: Main application package
- `__init__.py`: Application factory
- `config.py`: Configuration settings
- `extensions.py`: Flask extensions
- `models/`: Database models
- `api/`: API blueprint and routes
- `web/`: Web UI blueprint and routes
- `services/`: Business logic
- `utils/`: Helper utilities
- `migrations/`: Database migrations
- `tests/`: Test suite
- `docker/`: Docker configuration

## License

MIT License
