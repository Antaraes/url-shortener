from flask import Blueprint, request, jsonify, current_app, url_for
from app.services.shortener import URLShortenerService
from marshmallow import ValidationError
from app.api.schemas import CreateURLSchema, URLResponseSchema

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/shorten', methods=['POST'])
def shorten_url():
    """API endpoint to create a shortened URL."""
    schema = CreateURLSchema()
    
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    
    try:
        base_url = request.host_url.rstrip('/')
        service = URLShortenerService(base_url)
        
        result = service.create_short_url(
            original_url=data['url'],
            custom_id=data.get('custom_id'),
            expiration_days=data.get('expiration_days'),
            user_id=data.get('user_id')
        )
        
        return jsonify(URLResponseSchema().dump(result)), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating shortened URL: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@api_bp.route('/urls/<short_id>', methods=['GET'])
def get_url_stats(short_id):
    """API endpoint to get statistics for a shortened URL."""
    try:
        service = URLShortenerService(request.host_url.rstrip('/'))
        stats = service.get_url_stats(short_id)
        return jsonify(stats), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Error retrieving URL stats: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@api_bp.route('/urls', methods=['GET'])
def list_urls():
    """API endpoint to list URLs (for authenticated users)."""
    # This would typically include pagination, filtering, etc.
    # For now, we'll return a simple response
    return jsonify({"error": "This endpoint requires authentication"}), 401