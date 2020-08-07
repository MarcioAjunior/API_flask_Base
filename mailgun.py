#Configure o seu mailgun dominio aqui

MY_API_KEY = '' 
MY_DOMAIN_NAME = ''
TITULO = 'NOreply@DOMAIN'
FROM_EMAIL = 'noreplay@noreply'


#ESTA FUNÇÃO SERIA PARA enviar email de confirmação por meio do mailgun(minha lisença expirou)
"""
 def send_email_confirm(self):
        #Pegado a url de maneira dinamica
        link = request.url_root[:-1] + url_for('userconfirm', user_id= self.user_id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MY_DOMAIN_NAME),
        auth=('api', MY_API_KEY), 
        data= {'from' : '{} <{}>'.format(TITULO, FROM_EMAIL),
                'to' : self.email,
                'subject' : 'Confirmação de cadastro',
                'text' : 'Confirme seu cadastro clicando no link a seguir {} :'.format(link),
                'html' : '<html> <p> Confirme o seu cadastro clicando no link <a href="{}">CONFIRMAR eMAIL</a> </p></html>'.format(link)
              })
"""