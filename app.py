from distutils.command.build_scripts import first_line_re
from flask import Flask
from flask_restful import Api
from user import Login, Car, car1,Register,search
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager



app = Flask(__name__)
api = Api(app)

app.config['DEBUG']=True
app.config['JWT_SECRET_KEY']="secret-key"
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Apple God Market',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

api.add_resource(Car, '/Car')
docs.register(Car)
api.add_resource(car1, '/Car/<string:name>')
docs.register(car1)
api.add_resource(Login,'/Car/login')
docs.register(Login)
api.add_resource(Register, '/Car/register')
docs.register(Register)
api.add_resource(search, '/Car/product/<string:name>')
docs.register(search)

if __name__ == '__main__':
    JWTManager().init_app(app)
    app.run(debug=True)