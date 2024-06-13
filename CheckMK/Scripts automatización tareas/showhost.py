
#                                         o8o      .               
#                                         `"'    .o8             
# ooo. .oo.    .ooooo.  oooo oooo    ooo oooo  .o888oo  .oooo.    
# `888P"Y88b  d88' `88b  `88. `88.  .8'  `888    888   `P  )88b    
#  888   888  888ooo888   `88..]88..8'    888    888    .oP"888    
#  888   888  888    .o    `888'`888'     888    888 . d8(  888   
# o888o o888o `Y8bod8P'     `8'  `8'     o888o   "888" `Y888""8o 

import requests
import pandas as pd
import pprint
from tqdm import tqdm
import os

# Definimos variables generales
API_URL = "http://url/master/check_mk/api"
HEADERS = {"Authorization": "Bearer usuario contrasena ", "Accept": "application/json", "Content-Type": "application/json"}

# Inicializamos la sesión
session = requests.session()
session.headers = HEADERS

def find_host_by_ip():
    try:
        resp = session.get(
            f"{API_URL}/domain-types/host_config/collections/all",
            params={  # goes into query string
            "effective_attributes": True,  # Show all effective attributes on hosts, not just the attributes which were set on this host specifically.
        },
    )
        host_info = resp.json()

        # Cargar el DataFrame desde el archivo Excel
        data_frame = pd.read_excel('prueba.xlsx')

        non_exist_rows = []

        for index, row in data_frame.iterrows():
            # Comprobar si la IP en la fila no está presente en la información del host
            if not pd.isna(row[7]) and str(row[7]) not in str(host_info):
                print(row[7] + ', a trabajar becario!!! Que para algo te pagan!! Poco, pero algo...')
                non_exist_rows.append(row)
            else:
                print('CAFE TIME')
        # Crear un nuevo DataFrame con las filas que no coincidieron
        df_non_exist = pd.DataFrame(non_exist_rows)

        # Guardar el nuevo DataFrame en 'non_exist.xlsx'
        df_non_exist.to_excel('non_exist.xlsx', index=False)

        print("Proceso completado.")
        
    except requests.RequestException as e:
        print(f"Error en la solicitud a la API: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
if __name__ == '__main__':
    os.system('cls')  # Limpia la pantalla, puede variar según el sistema operativo
    find_host_by_ip()
