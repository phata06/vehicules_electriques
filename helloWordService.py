# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 13:57:44 2023

@author: user
"""

from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
from spyne.protocol.soap import Soap11
from  spyne.server.wsgi import WsgiApplication
import requests

##########" deubt"
# def api_chargetrip_vehicles():
#     url = 'https://api.chargetrip.io/graphql'
#     headers = {
#         "x-client-id": '634d7dfcd0930830249a0bb3',
#         "x-app-id": '634d7dfcd0930830249a0bb5'
#     }
#     query = """
#     query carListAll {
#         carList {
#             id
#             naming {
#                 make
#                 model
#                 version
#                 edition
#                 chargetrip_version
#             }
#             adapters {
#                 standard
#                 power
#                 time
#                 speed
#             }
#             battery {
#                 usable_kwh
#                 full_kwh
#             }
#             range {
#                 chargetrip_range {
#                     best
#                     worst
#                 }
#             }
#             media {
#                 image {
#                     id
#                     type
#                     url
#                     height
#                     width
#                     thumbnail_url
#                     thumbnail_height
#                     thumbnail_width
#                 }
#                 brand {
#                     id
#                     type
#                     url
#                     height
#                     width
#                     thumbnail_url
#                     thumbnail_height
#                     thumbnail_width
#                 }
#                 video {
#                     id
#                     url
#                 }
#             }
#         }
#     }
# """
#     r = requests.post(url=url, json={'query': query}, headers=headers).json()
#     list_vehicles = []
#     for i in r['data']['carList']:
#         make = i['naming']['make']
#         model = i['naming']['model']
#         version =  i['naming']['version']
#         range = (i['range']['chargetrip_range']['best'] + i['range']['chargetrip_range']['worst']) / 2
#         data = make,model,version,range
#         list_vehicles.append(data)
#     return(list_vehicles)

#### fin



# def api_chargetrip_vehicles():
#     url = 'https://api.chargetrip.io/graphql'
#     headers = {
#         "x-client-id": '634d7dfcd0930830249a0bb3',
#         "x-app-id": '634d7dfcd0930830249a0bb5'
#     }
#     query = """
#     query carListAll {
#         carList {
#             id
#             naming {
#                 make
#                 model
#                 version
#                 edition
#                 chargetrip_version
#             }
#             adapters {
#                 standard
#                 power
#                 time
#                 speed
#             }
#             battery {
#                 usable_kwh
#                 full_kwh
#             }
#             range {
#                 chargetrip_range {
#                     best
#                     worst
#                 }
#             }
#             media {
#                 image {
#                     id
#                     type
#                     url
#                     height
#                     width
#                     thumbnail_url
#                     thumbnail_height
#                     thumbnail_width
#                 }
#                 brand {
#                     id
#                     type
#                     url
#                     height
#                     width
#                     thumbnail_url
#                     thumbnail_height
#                     thumbnail_width
#                 }
#                 video {
#                     id
#                     url
#                 }
#             }
#         }
#     }
# """
#     r = requests.post(url=url, json={'query': query}, headers=headers).json()
#     list_vehicles = []
#     for i in r['data']['carList']:
#         make = i['naming']['make']
#         model = i['naming']['model']
#         version =  i['naming']['version']
#         range = (i['range']['chargetrip_range']['best'] + i['range']['chargetrip_range']['worst']) / 2
#         data = make,model,version,range
#         list_vehicles.append(data)
#     return(list_vehicles)


class HelloWorldService(ServiceBase):
 @rpc(Unicode, Integer, _returns=Iterable(Unicode))
 def say_hello(ctx, name, times):
     for i in range(times):
             yield u'Hello, %s' % name
             
 @rpc(Integer, Integer, _returns=Integer)
 def addition(ctx, a, b):
        return a // b
             

application = Application([HelloWorldService], 'spyne.examples.hello.soap', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)



if  __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()





