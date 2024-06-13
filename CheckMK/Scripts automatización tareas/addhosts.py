
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

# Definimos variables generales
API_URL = "https://url/master/check_mk/api/v0"
HEADERS = {"Authorization": "Bearer usuario contrasena ", "Accept": "application/json", "Content-Type": "application/json"}
DEFAULT_FILL_VALUE = "NA"

# Inicializamos la sesión
session = requests.session()
session.headers = HEADERS

# Modificamos los hosts que tienen etag a través de una request a la API
def add_host_checkmk(main, pais, establecimiento, centro, codigosalon, hostname, alias, ip_address, checkagent, snmp, dispositivo, fabricante, modelo, sistemaop, servicio):
    try:
        folder_path = f"/{main}/{pais}/{establecimiento}/{centro}"
        resp = session.post(
            f"{API_URL}/domain-types/host_config/collections/all",
            params={"bake_agent": False,
                    "verify": False},
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
        print(f"Host {hostname} creado en {folder_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error al crear host {hostname}: {e}")
        print(f"Respuesta del servidor: {resp.text}")


if __name__ == '__main__':
    # Solicitamos en un input los hosts a los que se les va a realizar la modificación
    data_frame = pd.read_excel('plantilla_add_hosts.xlsx').fillna(DEFAULT_FILL_VALUE)

    os.system('cls')  # Limpia la pantalla, puede variar según el sistema operativo

    if not data_frame.empty:
        for index, row in tqdm(data_frame.iterrows(), desc="Creando hosts"):
            add_host_checkmk(*row.values)
    else:
        print("El DataFrame está vacío.")
