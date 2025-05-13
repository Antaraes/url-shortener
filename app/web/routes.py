from flask import Blueprint, render_template, redirect, request, flash, abort, current_app
from app.services.shortener import URLShortenerService
from app.web.forms import URLForm

web_bp = Blueprint('web', __name__)

@web_bp.route('/', methods=['GET', 'POST'])
def index():
    """Home page with URL shortening form."""
    form = URLForm()
    
    if form.validate_on_submit():
        try:
            base_url = request.host_url.rstrip('/')
            service = URLShortenerService(base_url)
            
            result = service.create_short_url(
                original_url=form.url.data,
                custom_id=form.custom_id.data if form.custom_id.data else None,
                expiration_days=form.expiration_days.data if form.expiration_days.data else None
            )
            
            return render_template('result.html', url_data=result)
        
        except ValueError as e:
            flash(f"Error: {str(e)}", 'danger')
        except Exception as e:
            current_app.logger.error(f"Error creating shortened URL: {str(e)}")
            flash("An unexpected error occurred", 'danger')
    
    return render_template('index.html', form=form)

@web_bp.route('/<short_id>')
def redirect_to_url(short_id):
    """Redirect short URLs to their original URLs."""
    try:
        service = URLShortenerService(request.host_url.rstrip('/'))
        original_url = service.get_original_url(short_id)
        return redirect(original_url)
    
    except ValueError as e:
        abort(404, description=str(e))
    except Exception as e:
        current_app.logger.error(f"Error redirecting URL: {str(e)}")
        abort(500)

@web_bp.route('/stats/<short_id>')
def url_stats(short_id):
    """Display statistics for a shortened URL."""
    try:
        service = URLShortenerService(request.host_url.rstrip('/'))
        stats = service.get_url_stats(short_id)
        return render_template('stats.html', stats=stats)
    
    except ValueError:
        abort(404)
    except Exception as e:
        current_app.logger.error(f"Error displaying URL stats: {str(e)}")
        abort(500)

@web_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404, name='Page Not Found', 
                          description='The requested page could not be found.'), 404

@web_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code=500, name='Internal Server Error',
                          description='Something went wrong on our end.'), 500