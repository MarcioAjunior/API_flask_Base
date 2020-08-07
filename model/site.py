from slq_alchemy import banco



class SiteModel(banco.Model) :
    __tablename__ = 'sites'# nome da tabela

    #Mapeando a classe par o sqlAlchemy
    site_id = banco.Column(banco.Integer, primary_key = True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')  #Lista de objetos de hoteis

    def __init__(self, url):
        self.url = url

    def json(self):
        """Retorna o objeto como um json"""
        return {
            'site_id' : self.site_id,
            'url' : self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    def save_site(self) :
        banco.session.add(self)
        banco.session.commit()


    def delete_site(self):
        #Deletando todos os hoteis associados ao site
        [hotel.delete_hotel() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()


    @classmethod
    def find_by_id(cls, site_id):
        site = cls.query.filter_by(site_id = site_id).first() #SELECT * FROM hoteis where hotel_id =  hotel_id
        if site:
            return site
        return None
        
    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url = url).first() #SELECT * FROM hoteis where hotel_id =  hotel_id
        if site:
            return site
        return None