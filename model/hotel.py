from slq_alchemy import banco



class HotelModel(banco.Model) :
    __tablename__ = 'hoteis'# nome da tabela

    #Mapeando a classe par o sqlAlchemy
    hotel_id = banco.Column(banco.String, primary_key = True)
    nome = banco.Column(banco.String(80))   
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision = 2))
    cidade = banco.Column(banco.String(80))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'))
    #Poderia ser feiro uma referencia de volta ao hotel, ficaria => site = banco.relationship('SiteModel')
    
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id
    def json(self):
        """Retorna o objeto como um json"""
        return {
            'hotel_id' : self.hotel_id,
            'nome' : self.nome,
            'estrelas': self.estrelas,
            'diaria' : self.diaria,
            'cidade' : self.cidade,
            'site_id' : self.site_id
        }
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.cidade = cidade
        self.estrelas = estrelas
        self.diaria = diaria

        self.save_hotel()

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
        
    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id = hotel_id).first() #SELECT * FROM hoteis where hotel_id =  hotel_id
        if hotel:
            return hotel
        return None