import json
import requests
from apic_data import APIC_INFORMATION


def give_credentials(location, fabric):
    for fab in APIC_INFORMATION[location]:
        if fabric in fab.keys():
            controller = fab[fabric]["controller"]
            username = fab[fabric]["username"]
            password = fab[fabric]["password"]
            base_url = "https://" + str(controller) + "/api/"
            login_bit = "aaaLogin.json"
            logout_bit = ''
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
            login_cookie_jar = {'APIC-cookie': login_response.cookies['APIC-cookie']}
            # Setting Root node
            root_node = login_response_json["imdata"][0]["aaaLogin"]["attributes"]["node"]

            # logout
            logout_response = requests.post(login_url, json=login_post_data, verify=False)
            # logout Response status_code
            logout_status_code = logout_response.status_code

            return (location, fabric, controller, username, login_status_code, login_token,
                    login_headers, login_cookie_jar, root_node, logout_status_code)
