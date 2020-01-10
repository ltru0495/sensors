import datetime
import requests

module_name = 'MOD1'
orion_server = 'http://190.119.192.192:1026'
prefix = '/v2/entities/urn:ngsi-ld:DataObserved:'+module_name+'/attrs'  #DIRECCION SERVIDOR
url_server = orion_server+prefix

delay = 10

def datenow():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def post(data):
    r = requests.post(url_server, json=data)
    return r.status_code
