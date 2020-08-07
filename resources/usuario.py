from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from BLACKLIST import BLACKLIST
import traceback
from flask import make_response, render_template


from model.usuario import UserModel




#/usuario/user_id
class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuario não econtrado'}

    @jwt_required
    def delete(self, user_id):
       user = UserModel.find_user(user_id)
       if user:
            try:
                user.delete_user()
                return {'message': 'Usuario deletado com sucesso'}, 200
            except:
                return {'message' : 'Erro interno ao deletar'}, 500
            return {'message' : 'Not Found'}, 400


#/register
class UserRegister(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type= str, required=True, help='Informe o login')
    atributos.add_argument('senha', type= str, required=True, help='Informe a senha')
    atributos.add_argument('email', type= str, help='Informe um email')
    atributos.add_argument('ativado', type= bool, required=False, default=False)


    def post(self):
        #Os dados estão empacotado em dados
        dados = UserRegister.atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return {'message': 'O campo Email é obrigatório'}, 400
        
        if UserModel.find_by_email(dados.get('email')):
            return {'message' : 'Este email já foi cadastrado "{}"'.format(dados['email'])}, 400

        if UserModel.find_by_login(dados['login']):
            return {"message" : "O usuario '{}' já existe".format(dados['login'])}

        user = UserModel(**dados) #user = UserModel(dados['login'], dados['senha'])
        
        user.ativado = False #Garantindo que o ususario não esta ativado  ||False      
        try:
            user.save_user()
            user.send_email_confirm()
        except :
            user.delete_user()
            traceback.print_exc()
            return {'message' : 'Erro interno ao enviar requisição'}, 500           
        return {'message': 'Usuario cadastrado com sucesso'}, 201

class UserLogin(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('login', type= str, required=True, help='Informe o login')
    atributos.add_argument('senha', type= str, required=True, help='Informe a senha')
    atributos.add_argument('ativado', type= bool, required=False)

    @classmethod
    def post(cls):
        dados = cls.atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token = create_access_token(identity = user.user_id)
                return {'access token' : token  }, 200
            return {'message' : 'Usuario ainda não foi confirmado'}, 400
        return {'message' :'Senha e/ou usuario incorreto(s)'}, 401

class UserLogout(Resource):
    
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message' : 'Até breve'}

class UserConfirm(Resource):
    #raiz / confirmacao / user_id
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message" : "Usuario de id '{}' não cadastrado".format(user_id)}, 404
        user.ativado = True
        user.save_user()
        #return {"message" : "Usuario '{}' Verificado".format(user_id)}, 200
        #reescrevendo header
        headers = {'Content-Type' : 'text/html'}
        #context é um parametro da função render template, recebe uma kwars, ou Any,
        #e nele pode ser passado as variaveis que serão utilizadas no template,
        #  neste caso estou passando login e email
        return make_response(render_template('user_confirm.html',usuario=user.login, email= user.email), 200, headers)
class ForgotSenha(Resource):
    #enviar link
    @classmethod   
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {'message' : 'Usario não encontrado'}, 404
        
        user.send_email_reset()
        return {'message' : 'Acesse seu email para trocar a senha'}, 200

class ResetSenha(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('compara_senha', type=str, required=True, help='Compara senha obrigatorio')
    atributos.add_argument('senha', type=str, required=True, help='Senha nova obrigatoria')
    
    @classmethod
    def post(cls, user_id):
        dados = cls.atributos.parse_args()
        user = UserModel.find_user(user_id)

        if not user :
            return {'message' : 'Usario não encontrado'}, 404

        if not dados.get('senha') or dados.get('senha') is None :
            return {'message' : 'O campo senha é obrigatório'}
        
        if not dados.get('compara_senha') or dados.get('compara_senha') is None :
            return {'message' : 'O campo para comparar senhas é obrigatório'}
        
        if not safe_str_cmp(dados['senha'], dados['compara_senha']):
            return {'message' : 'Senhas não conferem'}
        
        try:
            user.senha = dados['senha']
            user.save_user()
        except:
            return {'message' : 'Erro ao salvar nova senha'}, 500
        return {'message' : 'Senha alterada com sucesso'}, 200
