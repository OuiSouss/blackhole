from flask import Flask
from werkzeug.serving import run_simple

def create_app():
    app = Flask(__name__)
    app.debug = True
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


if __name__ == "__main__":
    app = create_app()
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)