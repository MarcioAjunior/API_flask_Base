from flask_restful import Resource
from model.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site :
            return{'site' : site.json()}
        return {'message' : 'Site não encontrado'}, 404

    def post(self, url):
        if SiteModel.find_site(url):
            return {"message" : "Site '{}' já cadastrado".format(url)}, 400
        novo_site = SiteModel(url)
        try:
            novo_site.save_site()
        except:
            return {'message' : 'Erro na merda do server'}, 500
        return novo_site.json(), 201
    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deletado porra'}, 200
        return {"message" : "Erro ao localizar site: '{}'".format(site)}, 404
