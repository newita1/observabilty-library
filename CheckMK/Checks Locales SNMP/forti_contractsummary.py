#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#move the plugin to the folder /opt/omd/sites/nameofsite/local/lib/check_mk/base/plugins/agent_bhistoryased
#chown in the script for the user site (name of site)
#execute in OMD "cmk --debug -I --detect-plguins=nameofplugin -v"
from .agent_based_api.v1 import *
from datetime import datetime

def discover_forti_contractdescription(section): 
    yield Service(item="Certificates Summary")

def check_forti_contractdescription(item, section):
    if item == "Certificates Summary":
        conteo_success = 0
        conteo_failed = 0
        name_licencias = []
        for name, date in section:
            fecha_formateada = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
            fecha_actual = datetime.now()
            diferencia = fecha_formateada - fecha_actual
            if int(diferencia.days) <= 14:
                conteo_failed += 1
                name_licencias.append(name)
            elif int(diferencia.days) < 30:
                conteo_failed += 1
                name_licencias.append(name)
            else:
                conteo_success += 1  
        if conteo_failed > 1:
            yield Result(
                state=State.CRIT,
                notice=f"Licencias vigentes: {conteo_success}, Licencias a punto de caducar: {conteo_failed}",
                details=f"Licencias caducadas: {', '.join(name_licencias)}" 
            )
        else:
            yield Result(state = State.OK, summary = f"Licencias vigentes: {conteo_success}, Licencias a punto de caducar: {conteo_failed}")

register.check_plugin(
    name="forti_summary",
    # En el service name se pone %s para que agrege al nombre del servicio en CheckMK el contenido del primer OID.
    service_name="%s", 
    discovery_function = discover_forti_contractdescription,
    check_function=check_forti_contractdescription,
)

register.snmp_section(
    #  output de la OID:
    #  .1.3.6.1.4.1.12356.101.4.6.3.1.2.1.1 ==> STRING NOMBRE "Attack Definitions"
    #  .1.3.6.1.4.1.12356.101.4.6.3.1.2.1.2 ==> STRING FECHA "Mon Feb  3 02:00:00 2025"
    name = "forti_summary",

    # Se comprueba si existe el OID y con el fetch recogemos las oids 1 y 2 de la OID base...
    detect = exists(".1.3.6.1.4.1.12356.101.4.6.3.1.2.1"), 
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12356.101.4.6.3.1.2.1",
        oids=[
            "1",
            "2",
],
    ),
)