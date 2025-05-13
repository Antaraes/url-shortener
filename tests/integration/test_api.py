import json
import pytest

def test_shorten_url_api(client):
    """Test the API endpoint for shortening URLs."""
    response = client.post(
        '/api/v1/shorten',
        data=json.dumps({'url': 'https://example.com'}),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'short_url' in data
    assert data['original_url'] == 'https://example.com'
    assert 'short_id' in data

def test_shorten_url_with_custom_id(client):
    """Test shortening URLs with custom IDs."""
    response = client.post(
        '/api/v1/shorten',
        data=json.dumps({
            'url': 'https://example.com',
            'custom_id': 'custom123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['short_id'] == 'custom123'

def test_shorten_url_with_expiration(client):
    """Test shortening URLs with expiration."""
    response = client.post(
        '/api/v1/shorten',
        data=json.dumps({
            'url': 'https://example.com',
            'expiration_days': 7
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['expires_at'] is not None

def test_shorten_invalid_url(client):
    """Test handling invalid URLs."""
    response = client.post(
        '/api/v1/shorten',
        data=json.dumps({'url': 'not-a-valid-url'}),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_url_stats(client, sample_url):
    """Test retrieving URL statistics."""
    response = client.get(f'/api/v1/urls/{sample_url.short_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['short_id'] == sample_url.short_id
    assert data['original_url'] == sample_url.original_url
    assert data['visit_count'] == sample_url.visit_count

def test_get_nonexistent_url_stats(client):
    """Test retrieving stats for nonexistent URLs."""
    response = client.get('/api/v1/urls/nonexistent')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data