import requests
import json
import os
import time
import urllib3
urllib3.disable_warnings()

def attach_template(deviceName,templateName):

    # LOGIN
    url = "https://172.18.100.91:443/j_security_check"
    payload = 'j_username=admin&j_password=sentinel'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    session = requests.Session()
    response = session.post(url, headers=headers, data = payload, verify=False)
    # print("Login Status Code:", response.status_code)

    # TOKEN
    url = "https://172.18.100.91:443/dataservice/client/token"
    payload = {}
    response = session.get(url, headers=headers, data = payload, verify=False)
    token = response.text
    # print("Token:",token)

    # DEVICE LIST
    deviceId= ""
    deviceObj = None
    url = "https://172.18.100.91:443/dataservice/device"
    payload = {}
    response = session.get(url, headers=headers, data = payload, verify=False)
    devicelist = json.loads(response.text)
    for i in devicelist['data']: 
        if i['host-name'] == deviceName: 
            deviceId = i['uuid']
            deviceObj = i
    print("Number of devices", len(devicelist['data']) )
    if deviceId == "":
        print("Device not found:", deviceName)
        exit()
    else:
        # print("Device:",deviceName, deviceId )

    # TEMPLATE LIST
    templateId= ""
    templateObj = None
    url = "https://172.18.100.91:443/dataservice/template/device"
    payload = {}
    response = session.get(url, headers=headers, data = payload, verify=False)
    templatelist = json.loads(response.text)
    for i in templatelist['data']: 
        if i['templateName'] == templateName: 
            templateId = i['templateId']
            templateObj = i
    # print("Number of templates:", len(templatelist['data']) )
    if templateId == "":
        print("templateId not found:", templateName)
        exit()
    else:
        # print("Template:",templateName, "Id", templateId )
        pass

    # CHECK ATTACHED DEVICES
    url = "https://172.18.100.91:443/dataservice/template/device/config/attached/{0}".format(templateId)
    response = session.get(url, headers=headers, data = payload, verify=False)
    attachedlist = json.loads(response.text)
    for i in attachedlist['data']: 
        if i['host-name'] == deviceName: 
            print("Template:",templateName, "already attached to", deviceName )
            return True

    # ATTACH TEMPLATE
    url = "https://172.18.100.91:443/dataservice/template/device/config/attachfeature"
    payloadjson = {
        "deviceTemplateList": [
            {
            "templateId":templateId,
            "device": [
                {
                "csv-status": "complete",
                "csv-deviceId": deviceId,
                "csv-deviceIP": "10.255.255.1",
                "csv-host-name": "cEdge1",
                "/10/GigabitEthernet3/interface/ip/address": "10.10.1.1/28",
                "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/vpn0_next_hop_ip_internet/address": "10.0.1.1",
                "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/vpn0_next_hop_ip_mpls/address": "10.0.254.254",
                "/0/vpn0_mpls_if_name/interface/if-name": "GigabitEthernet2",
                "/0/vpn0_mpls_if_name/interface/ip/address": "10.0.254.1/24",
                "/0/vpn0_isp_if_name/interface/if-name": "GigabitEthernet1",
                "/0/vpn0_isp_if_name/interface/ip/address": "10.0.1.2/30",
                "//system/host-name": "cEdge1",
                "//system/system-ip": "10.255.255.1",
                "//system/site-id": "1",
                "csv-templateId": "76ba39e8-eb0e-47ac-ad8c-305ee31c8818",
                "selected": "true "
                }
            ],
            "isEdited": "false",
            "isMasterEdited": "false "
            }
        ]
    }
    payload = json.dumps(payloadjson)
    session.headers.update({'X-XSRF-TOKEN': token})
    session.headers.update({'Content-Type': 'application/json'})
    response = session.post(url, data = payload, verify=False)
    print("Template Push Response:",response.text)
    print("Waiting 60 Seconds for template to apply....",response.text)
    time.sleep( 60)


print("Starting script.....")
routerName  = "cEdge1" if not os.environ.get('routerName') else os.environ.get('routerName')
TemplateUp  = "Branches_cEdge1" if not os.environ.get('TemplateUp') else os.environ.get('TemplateUp')
TemplateDn  = "Branches_cEdge1_NODIA" if not os.environ.get('TemplateDn') else os.environ.get('TemplateDn')
monitorHost = "10.0.1.1" if not os.environ.get('monitorHost') else os.environ.get('monitorHost')
loopTimer   = 10  if not os.environ.get('loopTimer') else int(os.environ.get('loopTimer'))

while True:
    if( os.system("ping -c 1 " + monitorHost) ):
        attach_template( routerName, TemplateDn)
    else:
        attach_template( routerName, TemplateUp)

    time.sleep( loopTimer )
