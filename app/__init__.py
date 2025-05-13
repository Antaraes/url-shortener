def register_commands(app):
    """Register custom Flask CLI commands."""
    
    @app.cli.command("clean-expired")
    def clean_expired():
        """Remove expired URLs from the database."""
        from app.models.url import URL
        from datetime import datetime
        
        with app.app_context():
            expired = URL.query.filter(
                URL.expires_at.isnot(None),
                URL.expires_at < datetime.utcnow()
            ).delete()
            
            db.session.commit()
            print(f"Removed {expired} expired URLs.")
    
    @app.cli.command("stats")
    def url_stats():
        """Show basic statistics about the application."""
        from app.models.url import URL
        from sqlalchemy import func
        
        with app.app_context():
            total_urls = URL.query.count()
            total_clicks = db.session.query(func.sum(URL.visit_count)).scalar() or 0
            
            print(f"Total URLs: {total_urls}")
            print(f"Total Clicks: {total_clicks}")
            
            if total_urls > 0:
                avg_clicks = total_clicks / total_urls
                print(f"Average Clicks per URL: {avg_clicks:.2f}")
                
                # Most popular URLs
                popular = URL.query.order_by(URL.visit_count.desc()).limit(5).all()
                
                if popular:
                    print("\nMost Popular URLs:")
                    for url in popular:
                        print(f"/{url.short_id} → {url.visit_count} clicks")
    
    # Call this function in create_app
    # register_commands(app)