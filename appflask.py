from flask import Flask, jsonify, render_template, request, redirect, url_for, jsonify, send_from_directory, Response
import json
from zeep import Client
from flask_cors import CORS  # Ajoutez cette importation pour gérer les CORS
from flask_wtf import FlaskForm
from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from forms import VotreFormulaire
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clef_secrete_tres_difficile'
CORS(app)  # Activez CORS pour votre application Flask

service_url = "http://localhost:8000/?wsdl"
# Créez un client Zeep
client = Client(service_url)



class RouteForm(FlaskForm):
    start = StringField('Point de départ', validators=[DataRequired()])
    end = StringField('Destination', validators=[DataRequired()])
    battery_autonomy = StringField('Autonomie de la batterie (km)', validators=[DataRequired()])
    submit = SubmitField('Calculer l’itinéraire')

@app.route('/votre_route')
def votre_vue():
    form = VotreFormulaire()  # Créez une instance de votre formulaire
    return render_template('map.html', form=form)

@app.route('/get-charging-stations')
def get_charging_stations():
    with open('static/bornes.json') as json_file:
        data = json.load(json_file)
        return jsonify(data)

@app.route('/static/bornes')
def static_files(filename):
    return send_from_directory('static', filename)






############################################################""
@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    try:
        vehicles = api_chargetrip_vehicles()  # Cette fonction doit renvoyer la liste des véhicules.
        return jsonify(vehicles)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")  # Pour le débogage
        return jsonify({"error": "Une erreur s'est produite lors de la récupération des véhicules"}), 500







def api_chargetrip_vehicles():
    url_liste = "https://api.chargetrip.io/graphql"
    
    headers = {
        "x-client-id": "655523ce62941664053da0bf",
        "x-app-id": "655523ce62941664053da0c1",
        "Content-Type": "application/json"
    }

    vehicules = []
    page = 0
    size = 100

    while True:
        query = {
            "query": """
            query vehicleList($page: Int, $size: Int) {
                vehicleList(page: $page, size: $size) {
                    id
                    naming {
                        make
                        model
                        chargetrip_version
                    }
                    media {
                        image {
                            thumbnail_url
                        }
                    }
                    range {
                        chargetrip_range {
                            best
                            worst
                        }
                    }
                }
            }
            """,
            "variables": {
                "page": page,
                "size": size
            }
        }

        reponse = requests.post(url_liste, json=query, headers=headers)
        if reponse.status_code == 200:
            data = reponse.json()
            batch_vehicules = data["data"]["vehicleList"]
            vehicules.extend(batch_vehicules)
            
            # Si moins de 100 véhicules sont retournés, c'est qu'on a récupéré tous les véhicules.
            if len(batch_vehicules) < 100:
                break

            # Sinon, passez à la page suivante.
            page += 1
        else:
            # En cas d'erreur, arrêtez la boucle.
            break

    return vehicules


# vehicle_data = api_chargetrip_vehicles()
# print(vehicle_data)

class HelloWorldService(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def get_electric_vehicles(ctx):
        return api_chargetrip_vehicles()

#code mis le 02/11 a 22H33
class ServiceElectrique(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def recuperer_voitures_electriques(ctx):
        return api_chargetrip_vehicles()
    
@app.route('/soap-api', methods=['POST'])
def soap_api():
    response = wsgi_application(request.environ, start_response)
    return Response(response=response[0], status=200, headers=dict(response[1]))



@app.route('/', methods=['GET', 'POST'])
def index():
    form = RouteForm()
    if form.validate_on_submit():
        start = form.start.data
        end = form.end.data
        battery_autonomy = form.battery_autonomy.data
        print(f'Itinéraire de {start} à {end}')
        return redirect(url_for('index'))
    return render_template('map.html', form=form)
    

# @app.route('/api/vehicles', methods=['GET'])
# def get_vehicles():
#     vehicles = api_list_vehicules()
#     return jsonify(vehicles)


#######################  stop bornes ########################################################
# import requests

# @app.route('/get-electric-vehicles')
# def am_electric_vehicles():
#     url = 'https://api.chargetrip.io/graphql'

#     headers = {
#         'x-client-id': '655283700932825baf12f935',
#         'x-app-id': '655283700932825baf12f937',
#         'Content-Type': 'application/json',
#     }

#     query = {
#         "query": """
#             query vehicleList {
#                 vehicleList {
#                     id
#                     naming {
#                         make
#                         model
#                     }
#                     range {
#                         chargetrip_range {
#                             best
#                         }
#                     }
#                 }
#             }
#         """
#     }

#     response = requests.post(url, json=query, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         vehicles = data.get('data', {}).get('vehicleList', [])
#     else:
#         vehicles = []

#     return render_template('map.html', vehicles=vehicles)











def start_response(status, headers, exc_info=None):
    return status, headers

application = Application([HelloWorldService], 'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)
CORS(app, resources={r"/soap-api/*": {"origins": "http://127.0.0.1:5000"}})



if __name__ == '__main__':
    app.run(debug=True)
