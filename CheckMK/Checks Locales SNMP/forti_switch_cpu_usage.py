#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#move the plugin to the folder /opt/omd/sites/master/local/lib/check_mk/base/plugins/agent_based
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

def discover_syscpu_usage(section):
    name = "CPU Usage"
    yield Service(item=name)

def check_syscpu_usage(item, section):
    for i in section:
        if item == "CPU Usage":
            yield Metric("cpu_used", int(i[0]))
            if int(i[0]) >= 90:
                yield Result(state = State.CRIT, summary = f"CPU Usage: {float(i[0]):.2f}%")
            elif int(i[0]) >= 80:
                yield Result(state = State.WARN, summary = f"CPU Usage: {float(i[0]):.2f}%")
            else:
                yield Result(state = State.OK, summary = f"CPU Usage: {float(i[0]):.2f}%")
        return

register.check_plugin(
    name="fortiswitch_syscpu_usage",
    service_name="%s",
    discovery_function = discover_syscpu_usage,
    check_function=check_syscpu_usage,
)

register.snmp_section(
    name = "fortiswitch_syscpu_usage",
    detect = exists(".1.3.6.1.4.1.12356.106.4.1.2"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12356.106.4.1.2",
        oids=[
            "0", 
],
    ),
)                                                                    

                                                                     
                                                                     
                                                                     
