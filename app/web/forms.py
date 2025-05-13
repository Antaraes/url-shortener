from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, Length, NumberRange

class URLForm(FlaskForm):
    """Form for URL shortening."""
    url = StringField('URL to Shorten', validators=[
        DataRequired(),
        URL(message="Please enter a valid URL")
    ])
    custom_id = StringField('Custom Short ID (optional)', validators=[
        Optional(),
        Length(min=3, max=20, message="Custom ID must be between 3 and 20 characters")
    ])
    expiration_days = IntegerField('Expiration (days, optional)', validators=[
        Optional(),
        NumberRange(min=1, max=365, message="Expiration must be between 1 and 365 days")
    ])
    submit = SubmitField('Shorten URL')