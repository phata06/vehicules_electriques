
from flask import Flask, render_template, request, Response, jsonify
from zeep import Client
from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import requests
from flask_cors import CORS
import json
#import requests

app = Flask(__name__)
service_url = "http://localhost:8000/?wsdl"
# Créez un client Zeep
client = Client(service_url)



# URL du service SOAP HelloWorldService
#service_url = "http://localhost:8000/?wsdl"  # Assurez-vous de mettre l'URL correcte

# Créez un client Zeep
#client = Client(service_url)
#########################" debit de modif ################


@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = api_list_vehicules()
    return jsonify(vehicles)


class HelloWorldService(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def get_electric_vehicles(ctx):
        return api_list_vehicules()

#code mis le 02/11 a 22H33
class ServiceElectrique(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def recuperer_voitures_electriques(ctx):
        return api_list_vehicules()
    
# fin




# def api_chargetrip_vehicles():
#     url = 'https://api.chargetrip.io/graphql'
#     headers = {
#         "x-client-id": '6533834a9399c506085963ba',
#         "x-app-id": '6533834a9399c506085963bc'
#     }
#     query = """
#     query {
#         carList {
#             id
#             naming {
#                 make
#                 model
#                 version
#             }
#         }
#     }
#     """
#     response = requests.post(url, json={'query': query}, headers=headers)
#     data = response.json()
#     return (f"{car['naming']['make']} {car['naming']['model']} {car['naming']['version']}" for car in data['data']['carList'])

# debt de code 
import requests

def api_list_vehicules():
    url_liste = "https://api.chargetrip.io/graphql"
    
    headers = {
        "x-client-id": "6547bed991842fd24093e3e1",
        "x-app-id": "6547bed991842fd24093e3e3",
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


@app.route('/')
def liste_vehicules():
    vehicules = api_list_vehicules()
    return render_template('map.html', vehicules=vehicules)



# fin de code 

@app.route('/soap-api', methods=['POST'])
def soap_api():
    response = wsgi_application(request.environ, start_response)
    return Response(response=response[0], status=200, headers=dict(response[1]))


def start_response(status, headers, exc_info=None):
    return status, headers

application = Application([HelloWorldService], 'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)

CORS(app, resources={r"/soap-api/*": {"origins": "http://127.0.0.1:5000"}})









############### fin de modif ################
@app.route('/')
def index():
    return render_template('map.html')
    


@app.route('/calculate', methods=['GET'])
def calculate():
    a_str = request.args.get('a')
    b_str = request.args.get('b')
    #a = int(request.args.get('a'))
    #b = int(request.args.get('b'))
    heures = 0
    minutes = 0
    secondes = 0
    if a_str is not None and b_str is not None:
        a = int(a_str)
        b = int(b_str)
    # Appelez la méthode addition du service HelloWorldService
    result = client.service.addition(a, b)
    if (result == 60):
        heures = 1
    elif(result <= 59):
        minutes = int (result)
    else:
        
        heures = int(result / 60)
        minutes = int(result - (heures*60))
        
    #return minutes, heures , secondes
        
    
    
    return render_template('calculatrice.html', result=secondes, minute=minutes, seconde=secondes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


