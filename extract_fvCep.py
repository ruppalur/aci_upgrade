import re
import socket

ep_output = {'totalCount': '8',
             'imdata': [{'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/ctx-COAST_vrf/cep-00:DE:FB:79:8D:43',
                                                  'encap': 'vlan-222',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '192.168.50.12',
                                                  'lcC': 'learned',
                                                  'lcOwn': 'local',
                                                  'mac': '00:DE:FB:79:8D:43',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-15T11:58:25.443-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '00:DE:FB:79:8D:43',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}},
                        {'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/ctx-COAST_vrf/cep-00:DE:FB:79:8B:C3',
                                                  'encap': 'vlan-50',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '192.168.50.11',
                                                  'lcC': 'learned',
                                                  'lcOwn': 'local',
                                                  'mac': '00:DE:FB:79:8B:C3',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-15T11:34:31.824-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '00:DE:FB:79:8B:C3',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}},
                        {'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/ctx-COAST_vrf/cep-00:22:BD:F8:19:FF',
                                                  'encap': 'vlan-50',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '192.168.50.1',
                                                  'lcC': '',
                                                  'lcOwn': 'local',
                                                  'mac': '00:22:BD:F8:19:FF',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-15T11:58:25.443-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '00:22:BD:F8:19:FF',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}},
                        {'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/ctx-COAST_vrf/cep-50:0F:80:42:05:AF',
                                                  'encap': 'vlan-50',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '192.168.50.2',
                                                  'lcC': '',
                                                  'lcOwn': 'local',
                                                  'mac': '50:0F:80:42:05:AF',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-11T09:59:57.314-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '50:0F:80:42:05:AF',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}},
                        {'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/ap-app1/epg-epg1/cep-00:50:56:93:88:78',
                                                  'encap': 'vlan-101',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '101.1.1.101',
                                                  'lcC': 'learned',
                                                  'lcOwn': 'local',
                                                  'mac': '00:50:56:93:88:78',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-12T08:36:21.569-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '00:50:56:93:88:78',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}},
                        {'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/ctx-COAST_vrf/cep-00:00:00:00:00:00',
                                                  'encap': 'vlan-50',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '100.64.3.1',
                                                  'lcC': '',
                                                  'lcOwn': 'local',
                                                  'mac': '00:00:00:00:00:00',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-15T10:55:37.601-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '00:00:00:00:00:00',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}},
                        {'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/LDevInst-[uni/tn-COAST/lDevVip-PBR_DEV]-ctx-COAST_vrf/G-PBR_DEVctxCOAST_vrf-N-pbr-C-1arm/cep-00:DE:FB:79:8B:C3',
                                                  'encap': 'vlan-223',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '100.64.4.1',
                                                  'lcC': 'learned',
                                                  'lcOwn': 'local',
                                                  'mac': '00:DE:FB:79:8B:C3',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-21T09:35:28.830-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '00:DE:FB:79:8B:C3',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}},
                        {'fvCEp': {'attributes': {'annotation': '',
                                                  'childAction': '',
                                                  'contName': '',
                                                  'dn': 'uni/tn-COAST/LDevInst-[uni/tn-COAST/lDevVip-PBR_DEV]-ctx-COAST_vrf/G-PBR_DEVctxCOAST_vrf-N-pbr-C-1arm/cep-00:DE:FB:79:8D:43',
                                                  'encap': 'vlan-223',
                                                  'extMngdBy': '',
                                                  'id': '0',
                                                  'idepdn': '',
                                                  'ip': '100.64.4.3',
                                                  'lcC': 'learned',
                                                  'lcOwn': 'local',
                                                  'mac': '00:DE:FB:79:8D:43',
                                                  'mcastAddr': 'not-applicable',
                                                  'modTs': '2019-02-21T09:54:09.015-06:00',
                                                  'monPolDn': 'uni/tn-common/monepg-default',
                                                  'name': '00:DE:FB:79:8D:43',
                                                  'nameAlias': '',
                                                  'status': '',
                                                  'uid': '0',
                                                  'uuid': '',
                                                  'vmmSrc': ''}}}]}


pattern_192 = '^192\.168\.'
pattern_19 = '^19\.168\.'
pattern_10 = '^10\.0\.'
pattern_null = '^0\.0\.0\.0'


def resolve_name(ipaddress):
    try:
        dnsname = socket.gethostbyaddr(ipaddress)
        return dnsname[0]
    except:
        return "No DNS entry"


def filter_local_ip(ip_add):
    match_1 = re.search(pattern_192, ip_add)
    match_2 = re.search(pattern_10, ip_add)
    match_3 = re.search(pattern_null, ip_add)
    match_4 = re.search(pattern_19, ip_add)
    if (not match_1) and (not match_2) and (not match_3) and (not match_4):
        return True
    else:
        return False


def extractfvCEP(ep_output):
    tenant_list = []
    epg_list = []
    ep_list = []
    ip_list = []
    mac_list = []
    encap_list = []
    routable_list = []
    dns_list = []

    for object in ep_output['imdata']:
        # print(object)
        dn = object['fvCEp']['attributes']['dn']
        split_dn = dn.split("/")
        tenant_list.append(split_dn[1])
        epg_list.append(split_dn[-2])
        ep_list.append(split_dn[-1])
        ip_list.append(object['fvCEp']['attributes']['ip'])
        mac_list.append(object['fvCEp']['attributes']['mac'])
        encap_list.append(object['fvCEp']['attributes']['encap'])
        routable_list.append(filter_local_ip(object['fvCEp']['attributes']['ip']))
        dns_list.append(resolve_name(object['fvCEp']['attributes']['ip']))

    list_of_ep = zip(tenant_list, epg_list, ep_list, ip_list, mac_list, encap_list,
                     routable_list, dns_list)

    df_input = list(list_of_ep)

    return df_input
