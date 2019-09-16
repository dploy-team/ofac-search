from flask import Flask, request
from flask_restful import Resource, Api
import ofacdb
import ofacsearch
from flask import request
from flask import jsonify


app = Flask(__name__)
api = Api(app)


class ImportFiles(Resource):
    def put(self):
        try:
            ofacdb.import_files()
            return jsonify("{message: 'Success'}")
        except :
            return jsonify("{message: 'Não foi possível importar os arquivos'}")

class SearchOfac(Resource):
    def get(self):
        try:
            name = request.args.get('name')
            min_score = request.args.get('min_score')
            result = ofacsearch.search(name, min_score)
            return jsonify(result)
        except:
            return jsonify("{message: 'Ocorreu um erro ao pesquisar na base!'}")

api.add_resource(ImportFiles, '/import')
api.add_resource(SearchOfac, '/search')

if __name__ == '__main__':
     app.run(port='5002')
