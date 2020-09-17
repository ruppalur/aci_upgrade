import json
import requests
import re
from apic_data import APIC_INFORMATION
from extract_fvCep import extractfvCEP
from fabric_info import fabric_node_fw

controller = APIC_INFORMATION['SVL'][0]['SVL-FAB7']['controller']
username = APIC_INFORMATION['SVL'][0]['SVL-FAB7']['username']
password = APIC_INFORMATION['SVL'][0]['SVL-FAB7']['password']
LOCATION = 'SVL'
FABRIC = 'SVL-FAB7'
LEAFS = ['1011','1012']

def give_credentials(location, fabric):
    for fab in APIC_INFORMATION[location]:
        if fabric in fab.keys():
            controller = fab[fabric]["controller"]
            username = fab[fabric]["username"]
            password = fab[fabric]["password"]
            base_url = "https://" + str(controller) + "/api/"
            login_bit = "aaaLogin.json"
            logout_bit = 'aaaLogout.json'
            login_url = base_url + login_bit

            login_post_data = {
                "aaaUser": {
                    "attributes": {
                        "name": username,
                        "pwd": password
                    }
                }
            }
            logout_post_data = {
                "aaaUser": {
                    "attributes": {
                        "name": username
                    }
                }
            }
            # Login Post data for troubleshooting
            # str(login_post_data)
            # Login
            login_response = requests.post(login_url, json=login_post_data, verify=False)
            # login Status status_code
            login_status_code = login_response.status_code
            # Converting the session data to Json object
            login_response_json = login_response.json()
            # accessing the token
            login_token = login_response_json["imdata"][0]["aaaLogin"]["attributes"]["token"]
            # accessing the header
            login_headers = str(login_response.headers)
            # accessing the Cookie in header
            cookie_jar = {'APIC-cookie': login_response.cookies['APIC-cookie']}
            # Setting Root node
            root_node = login_response_json["imdata"][0]["aaaLogin"]["attributes"]["node"]

            # getting all endpoint information of Fabric
            ep_url = base_url + "node/class/fvCEp.json"
            ep_response = requests.get(ep_url, cookies=cookie_jar, verify=False)
            ep_output = ep_response.json()
            ep_total = ep_output['totalCount']
            ep_information = extractfvCEP(ep_output)
            #
            #
            #with open('/home/ruppalur/Dev/aup/sample_data/fvCep.json') as f:
            #    ep_output = json.load(f)
            #ep_total = ep_output['totalCount']
            # placeholder to capture are vaible ip address.
            #ep_information = extractfvCEP(ep_output)

            #getting the node(both leaf and spine) information of the fabric:
            # id, name, dn,fabricst, model,role,serial number
            node_url = base_url + "node/class/fabricNode.json"
            node_response = requests.get(node_url, cookies=cookie_jar, verify=False)
            node_output = node_response.json()

            #getting the node(both leaf and spine) information of the fabric:
            # firmware of all nodes except APIC
            firmware_url = base_url + 'node/class/firmwareRunning.json'
            firmware_response = requests.get(firmware_url, cookies=cookie_jar, verify=False)
            firmware_output = firmware_response.json()

            #concontenate both node and firmware output
            node_information = fabric_node_fw(node_output,firmware_output)

            # logout
            logout_response = requests.post(login_url, json=login_post_data, verify=False)
            # logout Response status_code
            logout_status_code = logout_response.status_code

            context_output = {
                'location': location,
                "fabric": fabric,
                "controller": controller,
                "username": username,
                "ep_total": ep_total,
                "login_status_code": login_status_code,
                "root_node": root_node,
                "logout_status_code": logout_status_code,
                "ep_info": ep_information,
                "node_output": node_information["imdata"]
            }
            return context_output

if __name__ == '__main__':
    give_credentials(LOCATION, FABRIC, LEAFS)