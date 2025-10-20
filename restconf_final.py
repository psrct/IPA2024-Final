import os, json, requests
requests.packages.urllib3.disable_warnings()

ROUTER_IP = os.environ.get("ROUTER_IP")
STUDENT_ID = os.environ.get("STUDENT_ID")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

api_url = f"https://{ROUTER_IP}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{STUDENT_ID}"
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = (USERNAME, PASSWORD)

def get_loopback_ip(student_id):
    # 3 หลักท้าย => abc; x=a, y=bc  -> 172.x.y.1/24
    abc = student_id[-3:]
    x = abc[0]
    y = abc[1:]  # เก็บสองหลักท้าย
    return f"172.{x}.{y}.1"

def create():
    Loopback_ip = get_loopback_ip(STUDENT_ID)
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}",
            "description": f"Loopback interface for student {STUDENT_ID} created by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": Loopback_ip, "netmask": "255.255.255.0"}]}
        }
    }

    resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if(resp.status_code == 201):
        return f"Interface loopback {STUDENT_ID} is created successfully"
    elif(resp.status_code == 204):
        return f"Cannot create: Interface loopback {STUDENT_ID}"
    return f"Error: Interface Loopback {STUDENT_ID} already exists"

def delete():
    resp = requests.delete(api_url, auth=basicauth, headers=headers, verify=False)
    if resp.status_code in (200, 204):
        return f"Interface loopback {STUDENT_ID} is deleted successfully"
    elif resp.status_code == 404:
        return f"Cannot delete: Interface loopback {STUDENT_ID}"
    else:
        return f"Error deleting interface {STUDENT_ID}"
