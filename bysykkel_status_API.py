from flask import Flask
from flask_restful import Resource, Api
from bysykkel_status_requests import get_table


app = Flask(__name__)
api = Api(app)

class Station_status(Resource):
    def get(self):
        table, success = get_table()
        if success:
            data = []
            for row in table:
                data.append({"Stasjon":row[0],
                             "Ledige sykler":row[1],
                             "Ledige låser":row[2]
                             })
            return data, 200
        else:
            return "Kunne ikke hente data", 500

api.add_resource(Station_status, '/')

if __name__ == '__main__':

    app.run()
