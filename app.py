from flask import Flask, jsonify
from flask_restful import Resource, Api
from resources.hotel import Hoteis, Hotel
from flask_jwt_extended import JWTManager
from BLACKLIST import BLACKLIST
from resources.site import Site, Sites


from resources.usuario import User, UserRegister, UserLogin, UserLogout, UserConfirm, ForgotSenha, ResetSenha

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'KEY-SECRET'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

#Mail trap configutartion
app.config['MAIL_SERVER']=''
app.config['MAIL_PORT'] = ''
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = ''
app.config['MAIL_USE_SSL'] = ''


api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blacklist_loader
def verefica_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidade():
    return jsonify({'message' : 'Esse token ja foi expirado'})


@jwt.unauthorized_loader
def unauthorized(token):
    return jsonify({
        'message' : 'Usuario Não Autorizado'
    })

@jwt.invalid_token_loader
def invalid_token(token):
    return jsonify({
        'message' : 'Token informado é invalido'
    })
 


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/register') 
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')
api.add_resource(ForgotSenha, '/forgotsenha/<int:user_id>')
api.add_resource(ResetSenha, '/resetsenha/<int:user_id>')

if __name__ == '__main__':
    from slq_alchemy import banco
    from my_flask_mail import mail
    banco.init_app(app)
    mail.init_app(app)
    app.run(debug=True)
