import pytest

def test_home_page(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'URL Shortener' in response.data
    assert b'Create short, easy-to-share links' in response.data

def test_shorten_url_form(client):
    """Test the URL shortening form."""
    response = client.post(
        '/',
        data={
            'url': 'https://example.com',
            'csrf_token': get_csrf_token(client)
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'URL Shortened Successfully' in response.data
    assert b'https://example.com' in response.data

def test_redirect_to_url(client, sample_url):
    """Test URL redirection."""
    response = client.get(f'/{sample_url.short_id}', follow_redirects=False)
    
    assert response.status_code == 302
    assert response.location == sample_url.original_url

def test_nonexistent_short_url(client):
    """Test handling nonexistent short URLs."""
    response = client.get('/nonexistent', follow_redirects=True)
    
    assert response.status_code == 404
    assert b'404' in response.data
    assert b'Page Not Found' in response.data

def test_stats_page(client, sample_url):
    """Test the statistics page."""
    response = client.get(f'/stats/{sample_url.short_id}')
    
    assert response.status_code == 200
    assert b'URL Statistics' in response.data
    assert sample_url.original_url.encode() in response.data
    assert str(sample_url.visit_count).encode() in response.data

def get_csrf_token(client):
    """Helper function to get CSRF token from the form."""
    response = client.get('/')
    html = response.data.decode()
    
    # Simple way to extract CSRF token
    csrf_token_start = html.find('name="csrf_token" value="') + 24
    csrf_token_end = html.find('"', csrf_token_start)
    return html[csrf_token_start:csrf_token_end]