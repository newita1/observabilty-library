
#                                         o8o      .               
#                                         `"'    .o8             
# ooo. .oo.    .ooooo.  oooo oooo    ooo oooo  .o888oo  .oooo.    
# `888P"Y88b  d88' `88b  `88. `88.  .8'  `888    888   `P  )88b    
#  888   888  888ooo888   `88..]88..8'    888    888    .oP"888    
#  888   888  888    .o    `888'`888'     888    888 . d8(  888   
# o888o o888o `Y8bod8P'     `8'  `8'     o888o   "888" `Y888""8o 

import requests
import json
import re
import pprint
import time
import pandas as pd
from tqdm import tqdm #Requiere instalacion
import os
#Definimos variables generales
headers = {"Authorization": "Bearer usuario contrasena","Accept": "application/json","Content-Type": "application/json"}
etag = ""
API_URL = "http://url/master/check_mk/api/1.0/"

session = requests.session()
session.headers = headers

def delete_hosts(host):
    resp = session.delete(
        f"{API_URL}/objects/host_config/{host}",
    )
    if resp.status_code == 200:
        pprint.pprint(resp.json())
    elif resp.status_code == 204:
        print("Done")
    else:
        raise RuntimeError(pprint.pformat(resp.json()))

if __name__ == '__main__':
    #Solicitamos en un input los hosts a los que se les va a realizar la modificacion
    hosts = input("Listado de hosts que van a ser modificados: \n")
    #Spliteamos el resultado para obtener una lista con todos los hosts como valores
    hosts = hosts.split(",")
    os.system('cls')
    for i in tqdm(hosts, desc="Getting information from host"):
        i = re.sub(" ","", i)
        delete_hosts(i)
         