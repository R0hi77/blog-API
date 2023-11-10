from flask import Flask
import os
from flask_jwt_extended import JWTManager



def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'api.sqlite'),
        JWT_SECRET_KEY = 'JWT_SECRET_KEY'
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    JWTManager(app)
    
    from . import database
    database.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.authbp)

    from . import blog
    app.register_blueprint(blog.blogbp)


    return app

    
