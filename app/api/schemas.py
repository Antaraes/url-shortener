from marshmallow import Schema, fields, validate

class CreateURLSchema(Schema):
    """Schema for URL creation request."""
    url = fields.URL(required=True, description="URL to be shortened")
    custom_id = fields.String(validate=validate.Length(min=3, max=20), description="Custom short ID (optional)")
    expiration_days = fields.Integer(validate=validate.Range(min=1, max=365), description="Days until expiration (optional)")
    user_id = fields.Integer(description="User ID for authenticated users (optional)")

class URLResponseSchema(Schema):
    """Schema for URL response."""
    short_url = fields.String(description="Complete shortened URL")
    original_url = fields.String(description="Original URL")
    short_id = fields.String(description="Short ID")
    created_at = fields.DateTime(description="Creation timestamp")
    expires_at = fields.DateTime(allow_none=True, description="Expiration timestamp")
    visit_count = fields.Integer(description="Number of visits")