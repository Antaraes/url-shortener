import pytest
from flask import url_for

def test_full_url_shortening_flow(client):
    """Test the full URL shortening flow from creation to redirection."""
    # Step 1: Create a shortened URL
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
    
    # Extract short_id from the response
    html = response.data.decode()
    short_id_start = html.find('value="http://localhost/') + 21
    short_id_end = html.find('"', short_id_start)
    short_id = html[short_id_start:short_id_end]
    
    # Step 2: Check the stats page
    response = client.get(f'/stats/{short_id}')
    assert response.status_code == 200
    assert b'Total Visits' in response.data
    assert b'0' in response.data  # Visit count should be 0 initially
    
    # Step 3: Access the short URL
    response = client.get(f'/{short_id}', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'https://example.com'
    
    # Step 4: Check the stats page again
    response = client.get(f'/stats/{short_id}')
    assert response.status_code == 200
    assert b'Total Visits' in response.data
    assert b'1' in response.data  # Visit count should be 1 now

def test_api_and_web_integration(client):
    """Test that the API and web interface work together."""
    import json
    
    # Step 1: Create URL via API
    api_response = client.post(
        '/api/v1/shorten',
        data=json.dumps({'url': 'https://example.com/api-test'}),
        content_type='application/json'
    )
    
    assert api_response.status_code == 201
    api_data = json.loads(api_response.data)
    short_id = api_data['short_id']
    
    # Step 2: View stats via web interface
    web_response = client.get(f'/stats/{short_id}')
    assert web_response.status_code == 200
    assert b'https://example.com/api-test' in web_response.data
    
    # Step 3: Access the short URL
    redirect_response = client.get(f'/{short_id}', follow_redirects=False)
    assert redirect_response.status_code == 302
    assert redirect_response.location == 'https://example.com/api-test'

def get_csrf_token(client):
    """Helper function to get CSRF token from the form."""
    response = client.get('/')
    html = response.data.decode()
    
    # Simple way to extract CSRF token
    csrf_token_start = html.find('name="csrf_token" value="') + 24
    csrf_token_end = html.find('"', csrf_token_start)
    return html[csrf_token_start:csrf_token_end]