"""
Run the application
"""
from flask import Flask
from backend.mongo_json_encoder import MongoJSONEncoder, ObjectIdConverter
def create_app():
    """
    @return app : Create the application in debug mode
    """
    app = Flask(__name__)
    app.debug = True
    
    app.json_encoder = MongoJSONEncoder
    app.url_map.converters['objectid'] = ObjectIdConverter

    from backend.app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    application = create_app()
    application.run()
