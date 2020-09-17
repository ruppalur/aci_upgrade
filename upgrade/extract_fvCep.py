import re
import socket

pattern_192 = '^192\.168\.'
pattern_19 = '^19\.168\.'
pattern_10 = '^10\.0\.'
pattern_2 = '^2\.2'
pattern_3 = '^3\.3'
pattern_null = '^0\.0\.0\.0'

def resolve_name(ipaddress):
    try:
        dnsname = socket.gethostbyaddr(ipaddress)
        return dnsname[0]
    except socket.herror:
        return "No DNS entry"

def filter_local_ip(ip_add):
    """
    This Function matches the know non routed subnets in fabric and if matches return false.
    :param ip_add:
    :return: boolean True if it is routable and false if it is non-routable
    """
    match_1 = re.search(pattern_192, ip_add)
    match_2 = re.search(pattern_10, ip_add)
    match_3 = re.search(pattern_null, ip_add)
    match_4 = re.search(pattern_19, ip_add)
    match_5 = re.search(pattern_2, ip_add)
    match_6 = re.search(pattern_3, ip_add)
    if (not match_1) and (not match_2) and (not match_3) and (not match_4) and (not match_5) and (not match_6):
        return True
    else:
        return False

def extractfvcep(ep_output):
    """
    this functions helps to extract the Tenant, epg, ip,mac, encap and dns from the ep_output of Fabric fvCEP.
    :param ep_output:
    :return: list of (tenant,epc, ep,ip,mac, encap, routable, dns)
    """
    tenant_list = []
    epg_list = []
    ep_list = []
    ip_list = []
    mac_list = []
    encap_list = []
    routable_list = []
    dns_list = []
    element_class = []

    for n_object in ep_output['imdata']:
        # print(object)
        routable_info = filter_local_ip(n_object['fvCEp']['attributes']['ip'])
        resolve_ip = resolve_name(n_object['fvCEp']['attributes']['ip'])
        dn = n_object['fvCEp']['attributes']['dn']
        split_dn = dn.split("/")
        tenant_list.append(split_dn[1])
        epg_list.append(split_dn[-2])
        ep_list.append(split_dn[-1])
        ip_list.append(n_object['fvCEp']['attributes']['ip'])
        mac_list.append(n_object['fvCEp']['attributes']['mac'])
        encap_list.append(n_object['fvCEp']['attributes']['encap'])
        routable_list.append(routable_info)
        dns_list.append(resolve_ip)
        if (routable_info == 'No DNS entry') or (routable_info == False):
            element_class.append('danger')
        else:
            element_class.append('success')

    list_of_ep = zip(tenant_list, epg_list, ep_list, ip_list, mac_list, encap_list,
                     routable_list, dns_list,element_class)
    df_input = list(list_of_ep)
    return df_input
