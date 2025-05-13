import pytest
from app.services.shortener import URLShortenerService
from app.models.url import URL
from app.extensions import db

def test_create_short_url(app):
    """Test creating a shortened URL."""
    with app.app_context():
        service = URLShortenerService('http://localhost:5000')
        result = service.create_short_url('https://example.com')
        
        assert result['original_url'] == 'https://example.com'
        assert result['short_url'].startswith('http://localhost:5000/')
        assert len(result['short_id']) >= 6
        
        # Verify it's in the database
        url = URL.query.filter_by(short_id=result['short_id']).first()
        assert url is not None
        assert url.original_url == 'https://example.com'

def test_create_with_custom_id(app):
    """Test creating a URL with custom ID."""
    with app.app_context():
        service = URLShortenerService('http://localhost:5000')
        result = service.create_short_url('https://example.com', custom_id='custom')
        
        assert result['short_id'] == 'custom'
        assert result['short_url'] == 'http://localhost:5000/custom'

def test_get_original_url(app, sample_url):
    """Test retrieving the original URL."""
    with app.app_context():
        service = URLShortenerService('http://localhost:5000')
        original_url = service.get_original_url('abc123')
        
        assert original_url == 'https://example.com'
        
        # Check that visit count was incremented
        url = URL.query.filter_by(short_id='abc123').first()
        assert url.visit_count == 1

def test_invalid_short_id(app):
    """Test handling invalid short IDs."""
    with app.app_context():
        service = URLShortenerService('http://localhost:5000')
        
        with pytest.raises(ValueError, match="Short URL not found"):
            service.get_original_url('nonexistent')

def test_invalid_url(app):
    """Test handling invalid URLs."""
    with app.app_context():
        service = URLShortenerService('http://localhost:5000')
        
        with pytest.raises(ValueError, match="Invalid URL format"):
            service.create_short_url('not-a-url')