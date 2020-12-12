from flask import Flask
from config import Config
from flask_mysqldb import MySQL

db = MySQL()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)    

    from app.main import bp
    app.register_blueprint(bp)

    
    return app
