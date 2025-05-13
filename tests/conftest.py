import pytest
from app import create_app
from app.extensions import db
from app.models.url import URL

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def sample_url(app):
    """Create a sample URL in the database."""
    with app.app_context():
        url = URL(
            original_url='https://example.com',
            short_id='abc123'
        )
        db.session.add(url)
        db.session.commit()
        return url