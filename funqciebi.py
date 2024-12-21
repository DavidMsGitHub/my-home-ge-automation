import requests
import json
import base64
import random



def check_for_ip():
    try:
        #GET IP
        try:
            ip_address = requests.get('https://api.ipify.org').text
        except:
            ip_address = "0.0.0.0"

        url = "https://api.jsonbin.io/v3/b/6761e27ee41b4d34e46722b0"
        headers = {
            "X-Master-Key": "$2a$10$GrNqHYXjs5IwHIFTEl.g4uMymGv8UhCoHHovCFaMmu.BRcGAUjeEi",
            "X-Access-Key": "$2a$10$/RK1RphOTyfESbNk9s4Bq.g65mEtFaCweiNaBOQwu1LnCmn6sUecy"
        }
        gigi = requests.get(url, headers=headers).json()



        for i in gigi["record"]["ips"]:
            if ip_address == i:
                return True

        print("Access Blocked")
        quit()
    except:
        pass

def submit_error(id, time, type="Poster"):
    url = "https://api.jsonbin.io/v3/b/676726b1acd3cb34a8bd73d0"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": "$2a$10$GrNqHYXjs5IwHIFTEl.g4uMymGv8UhCoHHovCFaMmu.BRcGAUjeEi",
        "X-Access-Key": "$2a$10$/RK1RphOTyfESbNk9s4Bq.g65mEtFaCweiNaBOQwu1LnCmn6sUecy"
    }


    ip = requests.get('https://api.ipify.org').text if requests.get('https://api.ipify.org').status_code == 200 else "0.0.0.0"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        existing_data = response.json().get("record", {})
    else:
        existing_data = {}


    existing_data[id] = {
        "time": time,
        "ip": ip,
        "type": type
    }


    update_response = requests.put(url, json=existing_data, headers=headers)


def login():
    user = input("Enter User Email: ")
    password = input("Enter User Password: ")

    contact_num = input("Enter Contact Number: ")
    contact_name = input("Enter Contact Name: ")

    new_credentials = {
        "email": user,
        "password": password
    }
    new_contact = {
        "name": contact_name,
        "number": contact_num
    }

    with open("config.json", "r", encoding='utf-8') as file:
        encoded_config = file.read()

    decoded_config = base64.b64decode(encoded_config).decode('utf-8')

    config = json.loads(decoded_config)

    if "credentials" in config:
        config["credentials"].update(new_credentials)
    else:
        config["credentials"] = new_credentials

    if "contact" in config:
        config["contact"].update(new_contact)
    else:
        config["contact"] = new_contact

    updated_config = json.dumps(config, ensure_ascii=False, indent=4)
    encoded_config = base64.b64encode(updated_config.encode('utf-8')).decode('utf-8')

    with open("config.json", 'w', encoding='utf-8') as file:
        file.write(encoded_config)
