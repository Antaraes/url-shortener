from datetime import datetime
from app.extensions import db
import string
import random


class URL(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_id = db.Column(db.String(10), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    visit_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def __init__(self, original_url, short_id=None, expires_at=None, user_id=None):
        self.original_url = original_url
        self.short_id = short_id if short_id else self._generate_short_id()
        self.expires_at = expires_at
        self.user_id = user_id

    def _generate_short_id(self, length=6):
        """Generate a random short ID if not provided."""
        chars = string.ascii_letters + string.digits
        while True:
            short_id = ''.join(random.choice(chars) for _ in range(length))
            if not URL.query.filter_by(short_id=short_id).first():
                return short_id

    def increment_visit_count(self):
        """Increment the visit counter for this URL."""
        self.visit_count += 1
        db.session.commit()

    def is_expired(self):
        """Check if the URL has expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        """Convert the URL object to a dictionary."""
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_id': self.short_id,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'visit_count': self.visit_count
        }