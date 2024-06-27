#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#move the plugin to the folder /opt/omd/sites/nameofsite/local/lib/check_mk/base/plugins/agent_bhistoryased
#chown in the script for the user site (name of site)
#execute in OMD "cmk --debug -I --detect-plguins=nameofplugin -v"
from .agent_based_api.v1 import *
from datetime import datetime

def discover_forti_contractdescription(section):
    # Recorro con un for las oids y agregamos como nombre de item el contenido del oid 1
    for name, date in section: 
        yield Service(item=name)

def check_forti_contractdescription(item, section):
        # Recorro con un for la seccion que contiene los valores de la oid 1 (name) y la oid 2 (date)
        for name, date in section:
            # Si la oid 1 es IGUAL al item entra en el if
            if name == item:
                # Formateamos la fecha y calculamos los dias totales que quedan para que caduque el certificado
                fecha_formateada = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
                fecha_actual = datetime.now()
                diferencia = fecha_formateada - fecha_actual
                # Si la caducidad(en dias) es menor a 1 mes, salta un warning, si es a 2 semanas, salta un critical, si no es ninguna de las dos, esta en ok.
                if int(diferencia.days) <= 14:
                    yield Result(state = State.CRIT, summary = f"Quedan {diferencia.days} dias para que caduque el certificado.")
                elif int(diferencia.days) < 30:
                    yield Result(state = State.WARN, summary = f"Quedan {diferencia.days} dias para que caduque el certificado.")
                else:
                     yield Result(state = State.OK, summary = f"Quedan {diferencia.days} dias para que caduque el certificado.")

register.check_plugin(
    name="forti_contractdescription",
    # En el service name se pone %s para que agrege al nombre del servicio en CheckMK el contenido del primer OID.
    service_name="Forti Certificate - %s", 
    discovery_function = discover_forti_contractdescription,
    check_function=check_forti_contractdescription,
)

register.snmp_section(
    #  output de la OID:
    #  .1.3.6.1.4.1.12356.101.4.6.3.1.2.1.1 ==> STRING NOMBRE "Attack Definitions"
    #  .1.3.6.1.4.1.12356.101.4.6.3.1.2.1.2 ==> STRING FECHA "Mon Feb  3 02:00:00 2025"
    name = "forti_contractdescription",

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