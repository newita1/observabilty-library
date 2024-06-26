#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#move the plugin to the folder /opt/omd/sites/nameofsite/local/lib/check_mk/base/plugins/agent_bhistoryased
#chown in the script for the user site (name of site)
#execute in OMD "cmk --debug -I --detect-plguins=nameofplugin -v"

#                                         o8o      .               
#                                         `"'    .o8             
# ooo. .oo.    .ooooo.  oooo oooo    ooo oooo  .o888oo  .oooo.    
# `888P"Y88b  d88' `88b  `88. `88.  .8'  `888    888   `P  )88b    
#  888   888  888ooo888   `88..]88..8'    888    888    .oP"888    
#  888   888  888    .o    `888'`888'     888    888 . d8(  888   
# o888o o888o `Y8bod8P'     `8'  `8'     o888o   "888" `Y888""8o 

from .agent_based_api.v1 import *

def discover_tvoice_llamadassalientes(section):
    name = "Llamadas Salientes"
    yield Service(item=name)

def check_stvoice_llamadassalientes(item, section):
    if item == "Llamadas Salientes":
        if len(section) < 1 or int(section[0]) > 0:
            value = "0"
            yield Result(state=State.OK, summary=f"Llamadas Salientes: {value}")
        else:
            value = ""
            for i in section:
                value = f"{value} {i}".strip()
            yield Result(state=State.OK, summary=f"Llamadas Salientes: {value}")
        
        yield Metric("outcoming_calls", int(value))


register.check_plugin(
    name="tvoice_sbc_llamadassalientes",
    service_name="%s",
    discovery_function = discover_tvoice_llamadassalientes,
    check_function=check_stvoice_llamadassalientes,
)

register.snmp_section(
    name = "tvoice_sbc_llamadassalientes",
    detect = exists(".1.3.6.1.4.1.5003.10.8.2.54.41"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.5003.10.8.2.54.41",
        oids=[
            "0", 
],
    ),
)