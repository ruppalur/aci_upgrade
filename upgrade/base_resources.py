"""
Version : 1
Usage: Gather the facts of Fabric during Upgrade
!
- Fabric Physical Information - done
- Capture the endpoint Information - done
- Capture the Southbound information connected to leafs -
    - identify the each interface in fabric
    - cdp and lldp information of each interface - #todo
    - opflex tunnels on each interface -
! All interfaces for operational state
for int in range(54):
    dn = output['imdata'][int]['l1PhysIf']['attributes']['dn']
    id = output['imdata'][int]['l1PhysIf']['attributes']['id']
    status = output['imdata'][int]['l1PhysIf']['children'][0]['ethpmPhysIf']['attributes']['operSt']
    type = output['imdata'][int]['l1PhysIf']['attributes']['usage']
! All northbound interfaces towards the Spines
for int in range(54):
    dn = output['imdata'][int]['l1PhysIf']['attributes']['dn']
    id = output['imdata'][int]['l1PhysIf']['attributes']['id']
    status = output['imdata'][int]['l1PhysIf']['children'][0]['ethpmPhysIf']['attributes']['operSt']
    type = output['imdata'][int]['l1PhysIf']['attributes']['usage']
    if 'fabric' in type:
        print(id,type,status)
! All southbound interfaces towards the compute,hosting
for int in range(54):
    dn = output['imdata'][int]['l1PhysIf']['attributes']['dn']
    id = output['imdata'][int]['l1PhysIf']['attributes']['id']
    status = output['imdata'][int]['l1PhysIf']['children'][0]['ethpmPhysIf']['attributes']['operSt']
    type = output['imdata'][int]['l1PhysIf']['attributes']['usage']
    if 'fabric' not in type:
        print(id,type,status)

#multithreading for hte node information - import concurrent.futures - completed

source: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/2-x/rest_cfg/2_1_x/b_Cisco_APIC_REST_API_Configuration_Guide/b_Cisco_APIC_REST_API_Configuration_Guide_chapter_01.html
source: https://github.com/unofficialaciguide/aci-python
!
    '''
    for node_id,model in crazy_output['leaf_nodes_info']:
        print(f"Gathering information for {node_id} {model} - ",end = "")
        #physcial interface information of node
        node_capture_start = time.perf_counter()
        node_physical_output = _instance.get_physical_interfaces(node_id)
        #print(node_physical_output)
        phy_node_output = format_leaf_interface_output(node_physical_output)
        #print("...done - ",end = "")
        #Get the fabric firmware information
        #print(f"Opflex information",end = "")
        opflex_node_output = _instance.get_opflex_information(node_id)
        crazy_output['phys_info'].append([node_id,phy_node_output,opflex_node_output])
        node_capture_stop = time.perf_counter()
        print(f' in {round(node_capture_stop - node_capture_start, 2)} sec(s)')
   '''
__author__ = ruppalur
"""

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from apic_data import APIC_INFORMATION
from extract_fvCep import extractfvcep
from fabric_info import fabric_node_fw
import time
import concurrent.futures


def get_interface_cdp_lldp_dn(int_dn):
    """
    This function will help to return the cdp dn and lldp dn
    :param int_dn: 'topology/pod-1/node-1011/sys/phys-[eth1/32]'
    :return: cdp_dn - 'topology/pod-1/node-1011/sys/cdp/inst/if-[eth1/32]'

    """
    cdp_int_dn = int_dn.replace('sys/phys','sys/cdp/inst/if')
    lldp_int_dn = int_dn.replace('sys/phys','sys/lldp/inst/if')

    return int_dn, cdp_int_dn, lldp_int_dn

def format_leaf_interface_output(l1PhysIf):
    """
    This function will help to format the L1Physical interface, list of information related to interface
    :param l1PhysIf: output of the leaf_int_url
    :return: dict segregated
    """
    output = {'spine_interfaces': [], 'southbound_interfaces': [], 'controller_interfaces': [], "spine_up_int_count": 0 ,
              "southbound_up_int_count": 0, "controller_up_int_count":0}
    ints_count = int(l1PhysIf['totalCount'])
    output['totalCount'] = ints_count
    for interface in range(ints_count):
        int_dn = l1PhysIf['imdata'][interface]['l1PhysIf']['attributes']['dn']
        int_id = l1PhysIf['imdata'][interface]['l1PhysIf']['attributes']['id']
        status = l1PhysIf['imdata'][interface]['l1PhysIf']['children'][0]['ethpmPhysIf']['attributes']['operSt']
        int_type = l1PhysIf['imdata'][interface]['l1PhysIf']['attributes']['usage']
        cdp_int_dn = int_dn.replace('sys/phys', 'sys/cdp/inst/if')
        lldp_int_dn = int_dn.replace('sys/phys', 'sys/lldp/inst/if')
        if 'fabric' in int_type:
            element_class = 'primary'
            output['spine_interfaces'].append([int_id , int_type, status, int_dn, cdp_int_dn, lldp_int_dn,element_class])
        elif 'controller' in int_type:
            element_class = 'danger'
            output['controller_interfaces'].append([int_id, int_type, status, int_dn, cdp_int_dn, lldp_int_dn,element_class])
        else:
            element_class = 'info'
            output['southbound_interfaces'].append([int_id, int_type, status, int_dn, cdp_int_dn, lldp_int_dn,element_class])
        #print([int_id, int_type, status, int_dn, cdp_int_dn, lldp_int_dn,element_class])
    #gather the up interfaces towards the spine
    output["spine_up_int_count"] = [spine[2] for spine in output['spine_interfaces'] ].count('up')
    # gather the up controller interfaces towards the spine
    output["controller_up_int_count"] = [spine[2] for spine in output['controller_interfaces']].count('up')
    # gather the up south_bound interfaces
    output["southbound_up_int_count"] = [spine[2] for spine in output['southbound_interfaces']].count('up')
    return output

def give_credentials(location, fabric):
    """
    This function will helps to retrieve the controller,username and pwd information with provided location,fabric info.
    :param location:
    :param fabric:
    :return: tuple(controller,username,password)
    """
    for fab in APIC_INFORMATION[location]:
        if fabric in fab.keys():
            controller = fab[fabric]["controller"]
            username = fab[fabric]["username"]
            password = fab[fabric]["password"]
            return controller, username, password

def extract_leaf_nodes(node_info):
    leaf_nodes = []
    for data in node_info['imdata']:
        if 'leaf' == data['fabricNode']['attributes']['role']:
            leaf_nodes.append([data['fabricNode']['attributes']['id'],data['fabricNode']['attributes']['model']])
    return leaf_nodes

class GatherFabricInfo:
    """
    This class will cover the functions required to capture Information
    of Fabric as suggested in MOP for upgrade.
    - Fabric Physical Information
        - APICs
        - SPINESs
        - Leafs
        - Node, Name, role, Model, Serial, DN, Firmware.
        - [IMPROVEMENT] - Please figure out if Any known Faults - ie, wear out of SSD.
    - Capture the endpoint Information
        - Endpoints, IP, MAC, Tenant, EPG/VRF/L3-out,Hostname,Encap vlan, Routable IP
    - Capture the Southbound information connected to leafs
        - CDP neighbors
        - MO tunnels
        - AVS/AVE information
        - Any Stale tunnel information
    """

    def __init__(self, apic, username, password):
        """
        :param apic: (str) - apic information - apic.example.com
        :param username: (str) - apic username
        :param password: (str) - apic password
        """
        self.username = username
        self.password = password
        self.apic = apic
        self.logged_in = False
        self.cookiejar = requests.cookies.RequestsCookieJar()
        self.base_url = "https://" + str(apic) + "/api/"
        self.login_url = self.base_url + "aaaLogin.json"
        self.logout_url = self.base_url + "aaaLogout.json"
        self.ep_url = self.base_url + "node/class/fvCEp.json"
        self.fabricNode_url = self.base_url + "node/class/fabricNode.json"
        self.firmware_url = self.base_url + 'node/class/firmwareRunning.json'
        self.node_dn_url = self.base_url + 'node/class/topology/pod-1/node-'
        self.topology_dn = ''

    def apic_login(self):
        """
        This function serves the login to APIC with the credential
        if logged in then response code is 200 - return the logged_in to True
        :return: update the self.logged_in to True if successful
        """

        login_post_data = {
            "aaaUser": {
                "attributes": {
                    "name": self.username,
                    "pwd": self.password
                }
            }
        }

        login_response = requests.post(self.login_url, json=login_post_data, verify=False)
        if login_response.status_code == 200:
            self.logged_in = True
            login_response_json = login_response.json()
            self.topology_dn = login_response_json["imdata"][0]["aaaLogin"]["attributes"]["node"][:-1]
        self.cookiejar = login_response.cookies

    def apic_logout(self):
        """
        Function servers to logout from the expect and returns nothing
        :return:
        """
        logout_post_data = {
            "aaaUser": {
                "attributes": {
                    "name": self.username
                }
            }
        }
        logout_response = requests.post(self.logout_url, json=logout_post_data, verify=False)
        if logout_response.status_code == 200:
            self.logged_in = False

    def get_endpoint_info(self):
        """
        This function servers to return the Endpoint information of all the Endpoints on the fabric
        corresponds to the MO class = fvCEp
        :return: ep_output
        """
        ep_response = requests.get(self.ep_url, cookies=self.cookiejar, verify=False)
        ep_output = ep_response.json()
        return ep_output

    def get_fabric_node_info(self):
        """
        This function servers to return the Fabric Node information on the fabric
        corresponds to the MO class = fabricNode
        :return:
        """
        node_response = requests.get(self.fabricNode_url, cookies=self.cookiejar, verify=False)
        node_output = node_response.json()
        return node_output

    def get_fabric_firmware_info(self):
        """
        This function servers to return the Fabric firmware information of existing nodes on the fabric
        corresponds to the MO class = fabricNode
        :return:
        """
        firmware_response = requests.get(self.firmware_url, cookies=self.cookiejar, verify=False)
        firmware_output = firmware_response.json()
        return firmware_output

    def get_physical_interfaces(self,node_id):
        """
        This function helps to retrieve all the Physical southbound interface(front panel interfaces)
        of a leaf
        :param node_id:
        :return:list of dn of interface
        """
        print(f"Physical interfaces info {node_id}", end="")
        int_url = "/l1PhysIf.json?rsp-subtree=children&rsp-subtree-class=ethpmPhysIf"
        leaf_int_url = self.node_dn_url + node_id + int_url
        leaf_int_output = requests.get(leaf_int_url, cookies=self.cookiejar, verify=False)
        print(f"...done - ", end="")
        return leaf_int_output.json()

    def get_opflex_information(self,node_id):
        """
        This function helps to retrieve all the Physical southbound interface(front panel interfaces)
        of a leaf
        :param node_id:
        :return:list of moquery information.
        """
        print(f"Opflex infor {node_id}",end = "")
        opflexodev_url = 'node/class/opflexODev.json?query-target-filter=and(wcard(opflexODev.fabricPathDn,"{0}"))'.\
            format(node_id)
        opflex_baseurl = self.base_url + opflexodev_url
        node_opflex_output = requests.get(opflex_baseurl, cookies=self.cookiejar, verify=False)
        print(f"...done",end = " ")
        return node_opflex_output.json()

    def get_phy_opflex_info(self,node_id):
        """
        This function helps to retrieve all the Physical southbound interface(front panel interfaces)
        of a leaf
        :param node_id:
        :return:list of oplex and physical information.
        """
        node_output = [node_id]
        node_info_start = time.perf_counter()
        int_url = "/l1PhysIf.json?rsp-subtree=children&rsp-subtree-class=ethpmPhysIf"
        leaf_int_url = self.node_dn_url + node_id + int_url
        leaf_int_output = requests.get(leaf_int_url, cookies=self.cookiejar, verify=False)
        node_output.append(leaf_int_output.json())
        opflexodev_url = 'node/class/opflexODev.json?query-target-filter=and(wcard(opflexODev.fabricPathDn,"{0}"))'. \
            format(node_id)
        opflex_baseurl = self.base_url + opflexodev_url
        node_opflex_output = requests.get(opflex_baseurl, cookies=self.cookiejar, verify=False)
        node_info_finish = time.perf_counter()
        print(f"Gathering Physical and Opflex information {node_id}...done in {round(node_info_finish-node_info_start, 2)} sec(s)")
        node_output.append(node_opflex_output.json())
        return node_output

def final_construct(location, fabric):
    start_function = time.perf_counter()
    cred_info = give_credentials(location, fabric)
    crazy_output = {'phys_info': [],
                    'opflex_info': [],
                    'location': location,
                    'fabric': fabric,
                    'controller': cred_info[0]}
    _instance = GatherFabricInfo(cred_info[0],cred_info[1],cred_info[2])
    #Trigger the login function
    login_start = time.perf_counter()
    print('Trying to logging in ',end = " ")
    _instance.apic_login()
    login_stop = time.perf_counter()
    print(f"...done in {round(login_stop-login_start, 2)} sec(s)")

    #Get the fabric information
    fabric_start = time.perf_counter()
    print('Gathering the information of fabric',end = " ")
    crazy_output['fabric_node_info'] = _instance.get_fabric_node_info()
    fabric_stop = time.perf_counter()
    print(f"...done in {round(fabric_stop-fabric_start, 2)} sec(s)")

    #Get the fabric firmware information
    print('Gathering the firmware information of fabric',end = " ")
    firmware_start = time.perf_counter()
    crazy_output['fabric_firmware_info'] = _instance.get_fabric_firmware_info()
    firmware_stop = time.perf_counter()
    print(f"...done in {round(firmware_stop-firmware_start, 2)} sec(s)")

    #extract leaf node information from the fabric_node_info.
    print('Extracting the node information of fabric',end = " ")
    nodeinfo_start = time.perf_counter()
    crazy_output['leaf_nodes_info'] = extract_leaf_nodes(crazy_output['fabric_node_info'])
    nodeinfo_stop = time.perf_counter()
    print(f"...done in {round(nodeinfo_stop - nodeinfo_start, 2)} sec(s)")


    #Get the Physical interfaces of node
    with concurrent.futures.ThreadPoolExecutor() as executor:
        nodes = [node[0] for node in crazy_output['leaf_nodes_info']]
        results = executor.map(_instance.get_phy_opflex_info,nodes)

        for phy_result in results:
            phy_node_output = format_leaf_interface_output(phy_result[1])
            crazy_output['phys_info'].append([phy_result[0], phy_node_output, phy_result[2]])
            #print(phy_result)
    '''
    #get Endpoint information
    print('-'*60)
    print('Gathering the endpoint information of fabric',end = " ")
    get_endpoint_start = time.perf_counter()
    endpoint_output = _instance.get_endpoint_info()
    crazy_output['endpoint_info'] = extractfvcep(endpoint_output)
    crazy_output['endpoint_total'] = endpoint_output['totalCount']
    get_endpoint_stop = time.perf_counter()
    print(f'...done in {round(get_endpoint_stop - get_endpoint_start, 2)} sec(s)')

    #test trigger to capture the node info
    nodeouput = _instance.get_phy_opflex_info(node_id)
    print(nodeouput)
    '''
    #Trigger the logout function
    print('Gathered all the information of fabric..logging off',end = " ")
    _instance.apic_logout()
    print("...logged off")

    # Merging both node and firmware output
    crazy_output['node_information'] = fabric_node_fw(crazy_output['fabric_node_info'], crazy_output['fabric_firmware_info'])
    finish_function = time.perf_counter()
    crazy_output['totalTime'] = round(finish_function - start_function, 2)
    return crazy_output

if __name__ == '__main__':
    my_location = 'SVL'
    my_fabric = 'SVL-FAB7'
    #node_id = '1011'
    final_construct_output = final_construct(my_location, my_fabric)
    for out in final_construct_output['phys_info']:
        print(out[2])

