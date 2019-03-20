"""
run.py
===================
Run the application
"""
from flask import Flask
from backend.mongo_json_encoder import MongoJSONEncoder, ObjectIdConverter
def create_app():
    """
    create_app Configure applicationt on /api

    Set Flask on debug mode
    Add a JSON Encode
    Set a blueprint /api

    :return: An application
    :rtype: Application object
    """
    app = Flask(__name__)
    app.debug = True
    app.config['BUNDLE_ERRORS'] = True

    app.json_encoder = MongoJSONEncoder
    app.url_map.converters['object_id'] = ObjectIdConverter

    from backend.app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    application = create_app()
    application.run()
