from slq_alchemy import banco
from flask import request, url_for
from requests import post
from mailgun import FROM_EMAIL, MY_API_KEY, MY_DOMAIN_NAME, TITULO
from flask_mail import Message

from my_flask_mail import mail

class UserModel(banco.Model) :
    __tablename__ = 'usuarios'# nome da tabela

    #Mapeando a classe par o sqlAlchemy
    user_id = banco.Column(banco.Integer, primary_key = True, nullable=False)#Se não for definido no construtor e deiza com valor Integer o SLQAlchemi crias Ids altomativos incrmendados
    login = banco.Column(banco.String(20))
    senha = banco.Column(banco.String(20), nullable=False)
    email = banco.Column(banco.String(100), unique = True, nullable=False)
    ativado = banco.Column(banco.Boolean, default=False)


    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado
    
    def send_email_confirm(self): #Configurado para o mailtrap
        #Pegando link de maneira dinamica
        link = request.url_root[:-1] + url_for('userconfirm', user_id= self.user_id)
        msg = Message("Confimarção de conta",
                  sender="noreply@noreply.com",
                  body= "Fala meu consagrado, use esse link para ativar a sua conta '{}'".format(link),
                  html = "<p>Click no link a seguir para completar a verificação da sua conta<a href={}> CLICK AQUI <a/></p>".format(link),
                  recipients = [self.email])# Dexa assim, pq ta funcionando.                  
        return mail.send(msg)

    def json(self):
        """Retorna o objeto como um json, sem a senha"""
        return {
            'user_id' : self.user_id,
            'login' : self.login,
            'ativado' : self.ativado,
            'email' : self.email
        }   
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def send_email_reset(self):
        link = request.url_root[:-1] + url_for('resetsenha', user_id = self.user_id)
        msg = Message("Alteração de senha",
                  sender="noreply@noreply.com",
                  body= "Fala meu consagrado, use esse link para resetar a sua senha '{}'".format(link),
                  html = "<p>Click no link a seguir para alterar sua senha '{}' </p>".format(link), # colocar uma tag a para criar link no email
                  recipients = [self.email])# Dexa assim, pq ta funcionando.                  
        return mail.send(msg)


    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()


    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login = login).first() #SELECT * FROM usuarios where hotel_id =  hotel_id
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email = email).first() #SELECT * FROM usuarios where hotel_id =  hotel_id
        if user:
            return user
        return None
        
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first() #SELECT * FROM hoteis where hotel_id =  hotel_id
        if user:
            return user
        return None

