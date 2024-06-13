#Alertado ElasticSearch uptime sondas
#Nos apoyamos en una PSQL para guardar las sondas, sus transacciones, el estado anterior y los tiempos de delay.
#Una vez tenemos a traves de las querys las transacciones a revisar y las sondas, las vamos recorriendo haciendo querys a ElasticSearch para obtener el estado de la sonda.
#Los diferentes estados son: 0. OK, 1.Delayed (Warning), 2.Degraded(Major), 3. Not accesible(Critical), esto se revisa que ocurra algun error 2 de cada 5 ejecuciones.
#Paquetes que requieren de instalacion
import psycopg2
import re
from elasticsearch import Elasticsearch
import urllib3
import requests

total_failed = 3
total_executions = 5
API_ELASTIC = "apielastic"

#funcion para enviar evento a OMI.
def send_omi_alert(status, sonda, ubicacion):
    header = {'Content-Type': 'application/xml' }
    if status == 3:
        description = f"Fallo en la sonda {sonda} en la instancia {ubicacion}."
        severity = "critical"
    elif status == 2:
        description = f"Degradacion grave en la sonda {sonda} en la instancia {ubicacion}."
        severity = "Major"
    elif status == 1:
        description = f"Degradacion leve en la sonda {sonda} en la instancia {ubicacion}."
        severity = "Minor"
    elif status == 0:
        description = f"Se ha recuperado la sonda {sonda} en la instancia {ubicacion}."
        severity = "Normal"
    xml=f"<event><description>{description}</description><severity>{severity}</severity><nodo>{ubicacion}</nodo><category>Sondas</category><subcategory>{sonda}</subcategory><fuente>Sondas</fuente><type>Availability</type><subcomponent></subcomponent><name>{sonda}</name></event>"
    request = requests.post('https://ip/bsmc/rest/events/Sondas',headers = header, data = xml, verify=False) 


#Funcion para obtener los datos de ElasticSearch haciendo una query.
def query_elastic(sonda=None, transaccion=None, ubicacion=None, data="sondas"):
    global API_ELASTIC
    global total_executions
    client = Elasticsearch("https://ipelastic:9200", api_key=API_ELASTIC, verify_certs=False)
    if data == "sondas":
    #Realizamos una busqueda con los datos de la query (nombre de sonda, transaccion y ubicacion) y con ello revisamos el estado de la sonda y el tiempo que ha tardado.
        result = client.search(
            index="synthetics-browser-default",
            query={"bool": {"must": [
                        {"match": {"monitor.name": {"query": f"{sonda}"}}},
                        {"match": {"monitor.type": {"query": "browser"}}},
                        {"match": {"synthetics.step.name": {"query": f"{transaccion}"}}},
                        {"match": {"observer.geo.name": {"query": f"{ubicacion}"}}},
                        {"exists": {"field": "synthetics.step.customstatus.code"}}  
                    ]
                }
            },
            sort={"@timestamp": {"order": "desc"}},
            size = total_executions
        )
    #Realizamos una busqueda para obtener todas las locations que usamos en los ultimos 7 dias para verificar de forma dinamica si se usa alguna ubicacion o se elimina alguna de forma dinamica.
    elif data == "ubicacion":
        result = []
        get_data = client.search(
            index="synthetics-browser-default",
            query={"bool": {"must": [
                    {"match": {"browser.relative_trace.name": {"query": "loadEvent"}}},
                    {"exists": {"field": "observer.geo.name"}},
                    {"range": {
                        "@timestamp": {
                        "gte": "now-1d",
                        "lte": "now"}}}
                    ]
                }
            },
            size = 700,
            sort={"@timestamp": {"order": "desc"}}
            )
        for i in get_data['hits']['hits']:
            result.append(i['_source']['observer']['geo']['name'])
        result = list(set(result))
    return(result)

#Funcion para atacar a la PostgreSQL, si la funcion es get, obtenemos todos los datos de la tabla, si la funcion es update, actualizamos los valores de la sonda.
def get_all_data_psql(funcion, data="sondas", status=None, sonda=None, location=None):
    conn = psycopg2.connect("host=ippostgres dbname=dbpostgres user=usuariopostgres password=contrasenapostgres")
    cur = conn.cursor()
    if funcion == "get":
        if data == "sondas":
            cur.execute("select * from sondas;")
            result = cur.fetchall()
    elif funcion == "update":
        cur.execute(f"UPDATE sondas SET status={status}, location_failed='{location}' WHERE sonda like '{sonda}';")
        result = "updated"
    conn.commit()
    cur.close()
    conn.close()
    return(result)

#Funcion principal, llamamos a las diferentes querys segun la necesidad que tengamos y determinamos si se debe de enviar una alerta y que alerta enviar.
def get_alerts():
    global total_failed
    #Creamos las variables necesarias para controlar la sonda que se esta verificando y la cantidad de hits que hay tanto de ejecuciones fallidas
    #como de ejecuciones degradadas o extremadamente degradadas.
    failed = {}
    degraded = {}
    high_degraded = {}
    ubicaciones = query_elastic(data="ubicacion")
    sonda_anterior = "no_sonda"
    status_anterior = 0
    location_notified_anterior = ""
    for i in ubicaciones:
        failed[i] = 0
        degraded[i] = 0
        high_degraded[i] = 0
    all_syntethics_executions = get_all_data_psql("get")
    all_syntethics_executions.append(["","",0,"","",""])
    #Recorremos todos los resultados de la PostgreSQL para ver que sondas tenemos y sus transacciones, en caso de ser una sonda diferente, restableceremos
    #las variables que verifican la cantidad de ejecuciones erroneas o con un tiempo de respuesta mayor al que queremos
    for sonda, transaccion, status, degraded_time, high_degraded_time, location_notified in all_syntethics_executions:
        #Si detectamos que la sonda actual es diferente a la anterior y la sonda anterior no es "no_sonda" (texto por defecto para detectar que es la primera linea
        #y se ha verificado ningun dato anteriormente),miramos que su status no sea 0 (OK) y que no haya ningun fallo ni degradacion. 
        if sonda != sonda_anterior:
            if int(status_anterior) != 0 and not sonda_anterior == "no_sonda":
                locations = []
                failed_locations = ""
                for i in ubicaciones:
                    location_notified_anterior = re.sub(', $','', str(location_notified_anterior))
                    if int(failed[i]) == 0 and int(degraded[i]) == 0 and int(high_degraded[i]) == 0 and str(i) in str(location_notified_anterior):
                        locations.append(i)
                    elif failed[i] != 0 or degraded[i] != 0 or high_degraded[i] != 0:
                        failed_locations = f"{i}, {failed_locations}"
                print(locations)
                print(failed_locations)
                for i in locations:
                    send_omi_alert(0, sonda_anterior, i)
                if len(failed_locations) >= 4:
                    get_all_data_psql(funcion="update", sonda=sonda_anterior, status=int(status_anterior), location=failed_locations)
                else:
                    get_all_data_psql(funcion="update", sonda=sonda_anterior, status=0, location=" ")
            sonda_anterior = sonda
            status_anterior = status
            location_notified_anterior = location_notified
            for i in ubicaciones:
                failed[i] = 0
                degraded[i] = 0
                high_degraded[i] = 0
        if sonda == "":
            break
        #Miramos por cada ubicacion si la transaccion esta success o failed, en caso de ser success miramos que no se pasen del umbral de
        #degradacion marcado en la base de datos ni ya haya sido notificado este estado anteriormente.
        for ubicacion in ubicaciones:
            query_elastic_result = query_elastic(sonda, transaccion, ubicacion)
            for i in query_elastic_result['hits']['hits']:
                if i['_source']['synthetics']['step']['status'] == "succeeded":
                #El tiempo de ElasticSearch esta en microsegundos, se debe de dividir entre 1000000 para obtener los segundos o multiplicar un segundo por 1000000
                    if int(i['_source']['synthetics']['step']['duration']['us']) >= (int(high_degraded_time)*1000000):
                        high_degraded[ubicacion] = high_degraded[ubicacion] + 1
                        if high_degraded[ubicacion] == total_failed and status != 2 and status !=3: 
                            send_omi_alert(2, sonda, ubicacion)
                            get_all_data_psql(funcion="update", sonda=sonda, status=2, location=ubicacion)
                    elif int(i['_source']['synthetics']['step']['duration']['us']) >= (int(degraded_time)*1000000):
                        degraded[ubicacion] = degraded[ubicacion] + 1
                        if degraded[ubicacion] == total_failed and status != 1 and status !=3:
                            send_omi_alert(1, sonda, ubicacion)
                            get_all_data_psql(funcion="update", sonda=sonda, status=1, location=ubicacion)
                elif i['_source']['synthetics']['step']['status'] == "failed":
                    failed[ubicacion] = failed[ubicacion] + 1
                    if failed[ubicacion] == total_failed and status != 3:
                        send_omi_alert(3, sonda, ubicacion)
                        get_all_data_psql(funcion="update", sonda=sonda, status=3, location=ubicacion)

if __name__=='__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_alerts()
