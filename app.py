import os
from flask import Flask, render_template
from config import config_by_name
from routes.main_routes import main_bp
from routes.student_routes import student_bp

def create_app(config_name=None):
    """
    Application factory pattern. Configures and returns the Flask application instance.
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp)

    # Register Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('404.html', error_message="Internal Server Error occurred. Please try again."), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', True))
