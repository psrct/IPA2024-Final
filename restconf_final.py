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

def enable():
    yangConfig = {
        "ietf-interfaces:interface": {"enabled": True}
    }

    resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {STUDENT_ID} is enabled successfully"
    elif resp.status_code == 404:
        return f"Cannot enable: Interface loopback {STUDENT_ID}"
    else:
        return f"Error enabling interface {STUDENT_ID}"

def disable():
    yangConfig = {
        "ietf-interfaces:interface": {"enabled": False}
    }

    resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)


    if 200 <= resp.status_code <= 299:
        return f"Interface loopback {STUDENT_ID} is shutdowned successfully"
    elif resp.status_code == 404:
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"
    else:
        return f"Error disabling interface {STUDENT_ID}"

def status():
    api_url_status = f"https://{ROUTER_IP}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback{STUDENT_ID}"
    resp = requests.get(api_url_status, auth=basicauth, headers=headers, verify=False)

    if 200 <= resp.status_code <= 299:
        response_json = resp.json()
        interface = response_json["ietf-interfaces:interface"][0]
        admin_status = interface.get("admin-status")
        oper_status = interface.get("oper-status")
        if admin_status == "up" and oper_status == "up":
            return f"Interface loopback {STUDENT_ID} is enabled"
        elif admin_status == "down" and oper_status == "down":
            return f"Interface loopback {STUDENT_ID} is disabled"
        else:
            return f"Interface loopback {STUDENT_ID} admin={admin_status}, oper={oper_status}"
    elif resp.status_code == 404:
        return f"No Interface loopback {STUDENT_ID}"
    else:
        return f"Error checking status for {STUDENT_ID}"