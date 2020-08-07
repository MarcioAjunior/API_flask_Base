from flask_restful import Resource, reqparse
from model.hotel import HotelModel
from model.site import SiteModel
from flask_jwt_extended import jwt_required
import sqlite3 

from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade

#path, criando buscas com filtros atraves dos parametros da uri
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)#Quantidade de itens para exibir
path_params.add_argument('offset', type=float)#Quantidade de elementos que se deseja pular

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        #dict compreenshion
        dados_validos = {chave : dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else :
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []

        for linha in resultado :
            hoteis.append({
            'hotel_id' : linha[0],
            'nome' : linha[1],            
            'estrelas': linha[2],
            'diaria' : linha[3],
            'cidade' : linha[4],
            'site_id' : linha[5]    
            })


        return {'Hoteis' : hoteis}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help='Este campo é obrigatório')    
    argumentos.add_argument('estrelas', type=float,
                            required=True, help='Este campo é obrigatório')
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('cidade', type=str, required=True,
                            help='Este campo é obrigatório')
    argumentos.add_argument('site_id', type=int, required=True,
                            help='Este campo referese ao site, e é obrigatório')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não econtrado'}
    
    #Passando por decorator pro jwt que é necessario um token para acessar essa função
    @jwt_required
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel ID '{}' ja existe".format(hotel_id)}, 400
        else:
            dados = Hotel.argumentos.parse_args()
            # Desempacotando dados como kwards
            hotel = HotelModel(hotel_id, **dados)

            if not SiteModel.find_by_id(dados.get('site_id')):
                return {'message' : 'O Hotel precisa estar assciado a um id valido'}, 400
            try:
                hotel.save_hotel()
            except:
                return {'message': 'Erro interno ao salvar Hotel'}, 500
            return hotel.json(), 201
    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            try:
                hotel_encontrado.update_hotel(**dados)
            except:
                return {'message': 'Erro interno ao alterar'}, 500
            return hotel_encontrado.json(), 200
        return {'message': 'hotel não encontrado'}, 404

    @jwt_required
    def delete(self, hotel_id):
       hotel = HotelModel.find_hotel(hotel_id)
       if hotel:
            try:
                hotel.delete_hotel()
                return {'message': 'Hotel deletado com sucesso'}, 200
            except:
                return {'message' : 'Erro interno ao deletar'}, 500
            return {'message' : 'Not Found'}, 400
