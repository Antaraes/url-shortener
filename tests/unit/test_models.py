import pytest
from datetime import datetime, timedelta
from app.models.url import URL
from app.extensions import db

def test_url_model_creation(app):
    """Test creating a URL model."""
    with app.app_context():
        url = URL(
            original_url='https://example.com',
            short_id='test123'
        )
        db.session.add(url)
        db.session.commit()
        
        retrieved = URL.query.filter_by(short_id='test123').first()
        assert retrieved is not None
        assert retrieved.original_url == 'https://example.com'
        assert retrieved.short_id == 'test123'
        assert retrieved.visit_count == 0
        assert retrieved.expires_at is None

def test_url_model_generate_short_id(app):
    """Test auto-generating short IDs."""
    with app.app_context():
        url = URL(original_url='https://example.com')
        db.session.add(url)
        db.session.commit()
        
        assert url.short_id is not None
        assert len(url.short_id) >= 6

def test_url_model_increment_visit_count(app):
    """Test incrementing visit count."""
    with app.app_context():
        url = URL(
            original_url='https://example.com',
            short_id='visit123'
        )
        db.session.add(url)
        db.session.commit()
        
        url.increment_visit_count()
        assert url.visit_count == 1
        
        url.increment_visit_count()
        assert url.visit_count == 2

def test_url_model_is_expired(app):
    """Test URL expiration check."""
    with app.app_context():
        # Create a URL that has already expired
        expired_url = URL(
            original_url='https://example.com/expired',
            short_id='expired',
            expires_at=datetime.utcnow() - timedelta(days=1)
        )
        
        # Create a URL that hasn't expired yet
        active_url = URL(
            original_url='https://example.com/active',
            short_id='active',
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
        
        # Create a URL with no expiration
        permanent_url = URL(
            original_url='https://example.com/permanent',
            short_id='permanent'
        )
        
        db.session.add_all([expired_url, active_url, permanent_url])
        db.session.commit()
        
        assert expired_url.is_expired() is True
        assert active_url.is_expired() is False
        assert permanent_url.is_expired() is False

def test_url_model_to_dict(app):
    """Test URL serialization to dictionary."""
    with app.app_context():
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(days=7)
        
        url = URL(
            original_url='https://example.com',
            short_id='dict123',
            created_at=created_at,
            expires_at=expires_at,
            visit_count=5
        )
        
        url_dict = url.to_dict()
        
        assert url_dict['original_url'] == 'https://example.com'
        assert url_dict['short_id'] == 'dict123'
        assert url_dict['visit_count'] == 5
        assert url_dict['created_at'] == created_at.isoformat()
        assert url_dict['expires_at'] == expires_at.isoformat()