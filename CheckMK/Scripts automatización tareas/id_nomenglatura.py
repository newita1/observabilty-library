import requests
import pandas as pd
import pprint
from tqdm import tqdm
import re 
import os
import json
# Definimos variables generales
API_URL = "http://checkmk.central.cirsa.com/master/check_mk/api"
HEADERS = {"Authorization": "Bearer automationfcarrenom TYYYBCJPCBJOU@VFRPDF ", "Accept": "application/json", "Content-Type": "application/json"}

# Inicializamos la sesión
session = requests.session()
session.headers = HEADERS

def find_host_by_ip():
        resp = session.get(
            f"{API_URL}/domain-types/host_config/collections/all",
            params={
                "effective_attributes": False,
            },
        )
        host_info = resp.json()
        data_frame = pd.read_excel('prueba.xlsx')

        for index, row in data_frame.iterrows():
            i = 1
            while True:
                host_info_str = json.dumps(host_info)

                # Comprobar si la etiqueta en la fila no está presente en la información del host
                if not re.search(re.escape(f"{row[5]}{i}"), host_info_str):
                    print("No está presente:", f"{row[5]}{i}")
                    data_frame.loc[index, "HOSTNAME"] = f"{row[5]}{i}"
                    break
                else:
                    print("Está presente:", f"{row[5]}{i}")
                    i += 1
                    data_frame.loc[index, "HOSTNAME"] = f"{row[5]}{i}"
            data_frame.to_excel('test.xlsx', index=False)

if __name__ == '__main__':
    os.system('cls')  # Limpia la pantalla, puede variar según el sistema operativo
    find_host_by_ip()
