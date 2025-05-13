import validators
from datetime import datetime, timedelta
from app.models.url import URL
from app.extensions import db
from urllib.parse import urlparse
import string
import random


class URLShortenerService:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_short_url(self, original_url, custom_id=None, expiration_days=None, user_id=None):
        """
        Create a shortened URL from the original URL.
        
        Args:
            original_url (str): The URL to be shortened
            custom_id (str, optional): Custom short ID for the URL
            expiration_days (int, optional): Number of days until URL expires
            user_id (int, optional): ID of the user creating the URL
            
        Returns:
            dict: Information about the created short URL
            
        Raises:
            ValueError: If the URL is invalid or custom ID is already taken
        """
        # Validate URL
        if not self._is_valid_url(original_url):
            raise ValueError("Invalid URL format")

        # Ensure URL has a scheme
        if not urlparse(original_url).scheme:
            original_url = f"http://{original_url}"

        # Calculate expiration date if provided
        expires_at = None
        if expiration_days:
            expires_at = datetime.utcnow() + timedelta(days=expiration_days)

        # Check if custom ID is provided and available
        if custom_id:
            existing_url = URL.query.filter_by(short_id=custom_id).first()
            if existing_url:
                raise ValueError("Custom short ID is already taken")
            short_id = custom_id
        else:
            # Check if URL already exists for this user
            existing_url = URL.query.filter_by(original_url=original_url, user_id=user_id).first()
            if existing_url and not existing_url.is_expired():
                return self._format_url_response(existing_url)
            
            # Generate a new short ID
            short_id = self._generate_short_id()

        # Create new URL object
        url = URL(
            original_url=original_url,
            short_id=short_id,
            expires_at=expires_at,
            user_id=user_id
        )
        
        db.session.add(url)
        db.session.commit()
        
        return self._format_url_response(url)

    def get_original_url(self, short_id):
        """
        Get the original URL from a short ID.
        
        Args:
            short_id (str): The short ID to look up
            
        Returns:
            str: The original URL
            
        Raises:
            ValueError: If the short ID doesn't exist or has expired
        """
        url = URL.query.filter_by(short_id=short_id).first()
        
        if not url:
            raise ValueError("Short URL not found")
        
        if url.is_expired():
            raise ValueError("Short URL has expired")
        
        url.increment_visit_count()
        return url.original_url

    def get_url_stats(self, short_id):
        """
        Get statistics for a shortened URL.
        
        Args:
            short_id (str): The short ID to look up
            
        Returns:
            dict: URL statistics
            
        Raises:
            ValueError: If the short ID doesn't exist
        """
        url = URL.query.filter_by(short_id=short_id).first()
        
        if not url:
            raise ValueError("Short URL not found")
        
        return url.to_dict()

    def _is_valid_url(self, url):
        """Validate if the provided string is a valid URL."""
        return validators.url(url) or validators.domain(url)

    def _generate_short_id(self, length=6):
        """Generate a random short ID."""
        chars = string.ascii_letters + string.digits
        while True:
            short_id = ''.join(random.choice(chars) for _ in range(length))
            if not URL.query.filter_by(short_id=short_id).first():
                return short_id

    def _format_url_response(self, url):
        """Format URL object as a response dictionary."""
        return {
            'short_url': f"{self.base_url}/{url.short_id}",
            'original_url': url.original_url,
            'short_id': url.short_id,
            'created_at': url.created_at.isoformat(),
            'expires_at': url.expires_at.isoformat() if url.expires_at else None,
            'visit_count': url.visit_count
        }