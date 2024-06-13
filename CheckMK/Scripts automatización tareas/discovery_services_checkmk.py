
#                                         o8o      .               
#                                         `"'    .o8             
# ooo. .oo.    .ooooo.  oooo oooo    ooo oooo  .o888oo  .oooo.    
# `888P"Y88b  d88' `88b  `88. `88.  .8'  `888    888   `P  )88b    
#  888   888  888ooo888   `88..]88..8'    888    888    .oP"888    
#  888   888  888    .o    `888'`888'     888    888 . d8(  888   
# o888o o888o `Y8bod8P'     `8'  `8'     o888o   "888" `Y888""8o 

import requests
import warnings
import re
import pprint
import requests
import os
from tqdm import tqdm #Requiere instalacion
#variables globales
HEADERS = {"Authorization": "Bearer usuario contrasena","Accept": "application/json","Content-Type": "application/json"}
session = requests.session()
session.headers = HEADERS
#Funcion discovery servicios
def service_discovery(host):

    resp = session.post(
        f"http://url/master/check_mk/api/1.0/domain-types/service_discovery_run/actions/start/invoke",
        headers={
            "Content-Type": 'application/json',  # (required) A header specifying which type of content is in the request/response body.
        },
        json={'host_name': host, 'mode': 'refresh'},
        allow_redirects=True,
    )
    if resp.status_code == 200:
        pprint.pprint(resp.json())
    elif resp.status_code == 204:
        print("Done")
    else:
        raise RuntimeError(pprint.pformat(resp.json()))

#Funcion aplicar cambios
if __name__ == '__main__':
    #filtramos los errores de warning que nos devuelve por el ssl verify.
    warnings.filterwarnings('ignore')
    #Hacemos una llamada al usuario con input para que ponga el listado de hosts y lo spliteamos
    hosts = input("Indica el listado de hosts (recuerda que deben de estar separados por una coma): \n")
    hosts = hosts.split(",")
    #Limpiamos la shell de Windows, si se requiere para Linux modificar con "clear"
    os.system('cls')
    #Recorremos el listado de hosts y añadimos una barra de carga por la cantidad de elementos que existen.
    for i in tqdm(hosts, desc="Discovering services"):
        #Eliminamos espacios y llamamos a la funcion que hace el discovery de servicios.
        i= re.sub(" ","", i)
        service_discovery(i)
    # #Una vez recorridos todos los hosts, aplicamos los cambios.