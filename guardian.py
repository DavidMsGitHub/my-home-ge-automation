import requests

def check_for_ip():
    #GET IP
    ip_address = requests.get('https://api.ipify.org').text

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


check_for_ip()