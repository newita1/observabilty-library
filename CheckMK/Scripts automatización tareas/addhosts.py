
#                                         o8o      .               
#                                         `"'    .o8             
# ooo. .oo.    .ooooo.  oooo oooo    ooo oooo  .o888oo  .oooo.    
# `888P"Y88b  d88' `88b  `88. `88.  .8'  `888    888   `P  )88b    
#  888   888  888ooo888   `88..]88..8'    888    888    .oP"888    
#  888   888  888    .o    `888'`888'     888    888 . d8(  888   
# o888o o888o `Y8bod8P'     `8'  `8'     o888o   "888" `Y888""8o 

import requests
import pandas as pd
from tqdm import tqdm
import os

import requests
import pandas as pd
from tqdm import tqdm
import os
import pprint

# Definimos variables generales
HOST_NAME = "localhost"
SITE_NAME = "site"
API_URL = f"http://{HOST_NAME}/{SITE_NAME}/check_mk/api/1.0"

USERNAME = "usuario"
PASSWORD = "contrasena"

session = requests.session()
session.headers['Authorization'] = f"Bearer {USERNAME} {PASSWORD}"
session.headers['Accept'] = 'application/json'
DEFAULT_FILL_VALUE = "NA"



# Modificamos los hosts que tienen etag a través de una request a la API
def add_host_checkmk(main, pais, establecimiento, centro, codigosalon, hostname, alias, ip_address, checkagent, snmp, dispositivo, fabricante, modelo, sistemaop, servicio):
    folder_path = f"/{main}/{pais}/{establecimiento}/{centro}"
    resp = session.post(
        f"{API_URL}/domain-types/host_config/collections/all",
        params={  # goes into query string
            "bake_agent": False,  # Tries to bake the agents for the just created hosts.
        },
        headers={
            "Content-Type": 'application/json',  # (required) A header specifying which type of content is in the request/response body.
        },
            json={
            'folder': folder_path,
            'host_name': hostname,
            'attributes': {
                'alias': alias,
                'ipaddress': ip_address,
                'tag_agent': checkagent,
                'tag_snmp_ds': snmp,
                'tag_TipoDispositivo': dispositivo,
                'tag_Fabricante': fabricante,
                'tag_Modelo': modelo,
                'tag_SistemaOperativo': sistemaop,
                'tag_Servicio': servicio
            },
        },
    )
    if resp.status_code == 200:
        pprint.pprint(f"Se ha creado {hostname} en el folder {folder_path}")
    elif resp.status_code == 204:
        print("Done")
    else:
        raise RuntimeError(pprint.pformat(resp.json()))


if __name__ == '__main__':
    # Solicitamos en un input los hosts a los que se les va a realizar la modificación
    data_frame = pd.read_excel('plantilla_add_hosts.xlsx').fillna(DEFAULT_FILL_VALUE)

    os.system('cls')  # Limpia la pantalla, puede variar según el sistema operativo

    if not data_frame.empty:
        for index, row in tqdm(data_frame.iterrows(), desc="Creando hosts"):
            add_host_checkmk(*row.values)
    else:
        print("El DataFrame está vacío.")
