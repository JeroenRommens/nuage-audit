#!/usr/bin/python
"""
Usage:
  nuage-audit [options]
  nuage-audit (-h | --help)
  
Options:
  -h --help              Show this screen
  -v --version           Show version
  --vsd=<string>         IP of VSD
  --enterprise=<string>  Enterprise name

"""

from docopt import docopt
from vspk import v5_0 as vsdk
import json


def getargs():
    return docopt(__doc__, version="nuage-audit 0.0.1")

def execute():
    main(getargs())

def main(args):
    api_url = "https://"+str(args['--vsd'])+":8443"
    try:
        session = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url=api_url)
        session.start()
        csproot = session.user
    except:
        print("ERROR: Could not establish connection to VSD API")
        sys.exit(1)

    enterprise_filter_str = 'name == "'+str(args['--enterprise'])+'"'
    enterprise = csproot.enterprises.get_first(filter=enterprise_filter_str)
    domains = enterprise.domains.get()

    print("--------------------------")
    print("Printing VSD Audit Summary")
    print("--------------------------")
    print("Enterprise Name: "+"\033[1m"+enterprise.name+"\033[0m")
    print("Number of L3 domains: "+"\033[1m"+str(len(domains))+"\033[0m")
    print("L3 Domain details: ")
    for domain in domains:
        print("\t" + domain.name +" :")
        subnets = domain.subnets.get()
        zones = domain.zones.get()
        vports = domain.vports.get()
        number_bridge_vports = 0
        number_host_vports = 0
        for vport in vports:
            if vport.type == 'BRIDGE':
                number_bridge_vports += 1
            elif vport.type == 'HOST':
                number_host_vports += 1

        print("\t\t Zones: "+"\033[1m"+str(len(zones))+"\033[0m")
        print("\t\t Subnets: "+"\033[1m"+str(len(subnets))+"\033[0m")
        print("\t\t Number of vPorts: "+"\033[1m"+str(len(vports)) +"\033[0m"+ " (Type Bridge: "+"\033[1m"+str(number_bridge_vports)+"\033[0m"+" Type Host: "+"\033[1m"+str(number_host_vports)+"\033[0m"+")")
        print("\t\t Underlay Breakout settings: Underlay Enabled: " +"\033[1m" + domain.underlay_enabled+"\033[0m"+ " PAT Enabled: "+"\033[1m" + domain.pat_enabled+"\033[0m")
        print("\t\t DPI Setting: " +"\033[1m" + domain.dpi+"\033[0m")

        ingress_acl_templates = domain.ingress_acl_templates.get()
        print("\t\t Ingress ACL Rules:")
        if len(ingress_acl_templates) == 0:
            print("\t\t\t \033[1m None Defined \033[0m")
        for ingress_acl_template in ingress_acl_templates:
            print("\t\t\t Name: "+"\033[1m"+ingress_acl_template.name+"\033[0m"+" Active: "+"\033[1m"+str(ingress_acl_template.active)+"\033[0m"+" Default Allow IP: "+"\033[1m"+str(ingress_acl_template.default_allow_ip)+"\033[0m"+" Default Allow Non IP: "+"\033[1m"+str(ingress_acl_template.default_allow_non_ip)+"\033[0m"+" Allow Address Spoofing: "+"\033[1m"+str(ingress_acl_template.allow_address_spoof)+"\033[0m")
            ingress_acl_entry_templates = ingress_acl_template.ingress_acl_entry_templates.get()
            for ingress_acl_entry_template in ingress_acl_entry_templates:
                if ingress_acl_entry_template.associated_l7_application_signature_id == None:
                    print("\t\t\t\t Priority: "+"\033[1m"+str(ingress_acl_entry_template.priority)+"\033[0m"+" Description: "+"\033[1m"+str(ingress_acl_entry_template.description)+"\033[0m"+" Source: "+"\033[1m"+str(ingress_acl_entry_template.network_type)+"\033[0m"+" Destination: "+"\033[1m"+str(ingress_acl_entry_template.location_type)+"\033[0m"+" Protocol: "+"\033[1m"+str(ingress_acl_entry_template.protocol)+"\033[0m")
                    print("\t\t\t\t Source Port: "+"\033[1m"+str(ingress_acl_entry_template.source_port)+"\033[0m"+" Destination Port: "+"\033[1m"+ingress_acl_entry_template.destination_port+"\033[0m"+" Action: "+"\033[1m"+str(ingress_acl_entry_template.action)+"\033[0m")
                    print("\t\t\t\t Stateful: "+"\033[1m"+str(ingress_acl_entry_template.stateful)+"\033[0m"+" Stats Logging Enabled: "+"\033[1m"+str(ingress_acl_entry_template.stats_logging_enabled)+"\033[0m"+" Flow Logging Enabled: "+"\033[1m"+str(ingress_acl_entry_template.flow_logging_enabled)+"\033[0m"+"\n")

        egress_acl_templates = domain.egress_acl_templates.get()
        print("\t\t Egress ACL Rules:")
        if len(egress_acl_templates) == 0:
            print("\t\t\t \033[1m None Defined \033[0m")
        for egress_acl_template in egress_acl_templates:
            print("\t\t\t Name: "+"\033[1m"+egress_acl_template.name+"\033[0m"+" Active: "+"\033[1m"+str(egress_acl_template.active)+"\033[0m"+" Default Allow IP: "+"\033[1m"+str(egress_acl_template.default_allow_ip)+"\033[0m"+" Default Allow Non IP: "+"\033[1m"+str(egress_acl_template.default_allow_non_ip)+"\033[0m"+" Install ACL Implicit Rules: "+"\033[1m"+str(egress_acl_template.default_install_acl_implicit_rules)+"\033[0m")


    print("Infrastructure Details: ")
    ns_gateways = enterprise.ns_gateways.get()
   
    number_nsg_active = 0
    number_nsg = 0
    number_nsgbr = 0
    number_nsgubr = 0
    number_nsg_single_uplink = 0 
    number_nsg_dual_uplink = 0
    number_pppoe = 0
    number_static = 0
    number_dynamic = 0
    number_lte = 0
    number_uplinks_nat_probes = 0
    number_uplinks_ubr_only = 0
    number_ike_tunnels = 0
    number_uplinks_bgp = 0
    number_uplinks_patpool = 0
    number_egressqos = 0

    for ns_gateway in ns_gateways:
        if ns_gateway.bootstrap_status == 'ACTIVE':
            number_nsg_active += 1
        if ns_gateway.personality == 'NSG':
            number_nsg += 1
            if isSingleUplink(ns_gateway):
                number_nsg_single_uplink += 1
            else:
                number_nsg_dual_uplink += 1
            number_pppoe += getPPPoE(ns_gateway)
            number_static += getStatic(ns_gateway)
            number_dynamic += getDynamic(ns_gateway)
            number_lte += getLTE(ns_gateway)
            number_uplinks_nat_probes += getNATflag(ns_gateway)
            number_uplinks_ubr_only += getUBRflag(ns_gateway)
            number_ike_tunnels += getIKE(ns_gateway)
            number_uplinks_bgp += getBGP(ns_gateway)
            number_uplinks_patpool += getPATNAT(ns_gateway) 
            number_egressqos += getEgressQoS(ns_gateway)

        elif ns_gateway.personality == 'NSGBR':
            number_nsgbr += 1
        elif ns_gateway.personality == 'NSGDUC':
            number_nsgubr += 1

    print("\tNumber of Network Services Gateways configured: "+"\033[1m"+str(len(ns_gateways))+"\033[0m" + " (Status Active: "+"\033[1m"+str(number_nsg_active)+"\033[0m"+" Other: "+"\033[1m"+str(len(ns_gateways)-number_nsg_active)+"\033[0m"+")")
    print("\tPersonality distribution: NSG: "+"\033[1m"+str(number_nsg)+"\033[0m"+" NSG-BR: "+"\033[1m"+str(number_nsgbr)+"\033[0m"+" NSG-UBR: "+"\033[1m"+str(number_nsgubr)+"\033[0m")
    print("\tSingle/Dual Uplink distribution (only including personality NSG): Single Uplink: "+"\033[1m"+str(number_nsg_single_uplink)+"\033[0m"+" Dual Uplink: "+"\033[1m"+str(number_nsg_dual_uplink)+"\033[0m")
    print("\tUplink connection distribution (only including personality NSG): Dynamic: "+"\033[1m"+str(number_dynamic)+"\033[0m"+" Static: "+"\033[1m"+str(number_static)+"\033[0m"+" PPPoE: "+"\033[1m"+str(number_pppoe)+"\033[0m"+" LTE: "+"\033[1m"+str(number_lte)+"\033[0m")
    print("\tNumber of uplinks with NAT probes enabled: "+"\033[1m"+str(number_uplinks_nat_probes)+"\033[0m")
    print("\tNumber of uplinks with Traffic Through UBR Only flag enabled: "+"\033[1m"+str(number_uplinks_ubr_only)+"\033[0m")
    print("\tNumber of uplinks with an IKE tunnel configured: "+"\033[1m"+str(number_ike_tunnels)+"\033[0m")
    print("\tNumber of uplinks with BGP configured: "+"\033[1m"+str(number_uplinks_bgp)+"\033[0m")
    print("\tNumber of uplinks with a PAT Pool configured: "+"\033[1m"+str(number_uplinks_patpool)+"\033[0m")
    print("\tNumber of uplinks with Egress QoS Profile: "+"\033[1m"+str(number_egressqos)+"\033[0m")
    
    print("--------------------------\n")

    #print("Printing VSD Audit Details")
    #print("--- Enterprise JSON Object ---")
    #print json.dumps(enterprise.to_dict(), indent=3)

def getEgressQoS(ns_gateway):
    ns_ports = ns_gateway.ns_ports.get()
    num_egressqos = 0
    for ns_port in ns_ports:
        if ns_port.port_type == 'NETWORK':
            vlans = ns_port.vlans.get()
            for vlan in vlans:
                if vlan.associated_egress_qos_policy_id != None:
                    num_egressqos += 1
    return num_egressqos


def getPATNAT(ns_gateway):
    patnat_pools = ns_gateway.patnat_pools.get()
    return len(patnat_pools)

def getIKE(ns_gateway):
    ns_ports = ns_gateway.ns_ports.get()
    num_ike = 0
    for ns_port in ns_ports:
        if ns_port.port_type == 'NETWORK':
            vlans = ns_port.vlans.get()
            for vlan in vlans:
                ike_gateway_connections = vlan.ike_gateway_connections.get()
                if len(ike_gateway_connections) > 0:
                    num_ike += 1
    return num_ike

def getBGP(ns_gateway):
    ns_ports = ns_gateway.ns_ports.get()
    num_bgp = 0
    for ns_port in ns_ports:
        if ns_port.port_type == 'NETWORK':
            vlans = ns_port.vlans.get()
            for vlan in vlans:
                bgp_neighbors = vlan.bgp_neighbors.get()
                if len(bgp_neighbors) > 0:
                    num_bgp += 1
    return num_bgp


def isSingleUplink(ns_gateway):
    ns_ports = ns_gateway.ns_ports.get()
    network_ports = 0
    for ns_port in ns_ports:
        if ns_port.port_type == 'NETWORK':
            network_ports += 1
    if network_ports == 1:
        return True
    else:
        return False

def getNATflag(ns_gateway):
    ns_ports = ns_gateway.ns_ports.get()
    nat_flags = 0
    for ns_port in ns_ports:
        if ns_port.enable_nat_probes == True:
            nat_flags += 1
    return nat_flags

def getUBRflag(ns_gateway):
    ns_ports = ns_gateway.ns_ports.get()
    ubr_flags = 0
    for ns_port in ns_ports:
        if ns_port.traffic_through_ubr_only == True:
            ubr_flags += 1
    return ubr_flags

def getPPPoE(ns_gateway):
    uplink_connections = ns_gateway.uplink_connections.get()
    pppoe_ports = 0
    for uplink_connection in uplink_connections:
        if uplink_connection.mode == 'PPPoE':
            pppoe_ports += 1
    return pppoe_ports

def getStatic(ns_gateway):
    uplink_connections = ns_gateway.uplink_connections.get()
    static_ports = 0
    for uplink_connection in uplink_connections:
        if uplink_connection.mode == 'Static':
            static_ports += 1
    return static_ports

def getLTE(ns_gateway):
    uplink_connections = ns_gateway.uplink_connections.get()
    lte_ports = 0
    for uplink_connection in uplink_connections:
        if uplink_connection.mode == 'LTE':
            lte_ports += 1
    return lte_ports

def getDynamic(ns_gateway):
    uplink_connections = ns_gateway.uplink_connections.get()
    dynamic_ports = 0
    for uplink_connection in uplink_connections:
        if uplink_connection.mode == 'Dynamic':
            dynamic_ports += 1
    return dynamic_ports


if __name__ == "__main__":
    main(getargs())


 

 