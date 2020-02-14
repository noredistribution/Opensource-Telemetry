#!/usr/bin/python
import requests
from requests.auth import HTTPBasicAuth
import json

USER = 'cvpadmin'
PASS = 'arastra'

requests.packages.urllib3.disable_warnings()

#api_call = "https://10.83.13.139:6020/restconf/data/interfaces/interface=Ethernet1"

api_call = "https://10.83.13.139:6020/restconf/data/interfaces/interface=Ethernet1/state/description"

headers = {'Content-Type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'}

result = requests.get(api_call, auth=HTTPBasicAuth(USER, PASS), headers=headers, verify=False)

if result.status_code == 200:
    	print ('Restconf call successful! Status Code is: {}\n').format(result.status_code)
    	result = json.loads(result.content.decode('utf-8'))
else:
    	print ('The Restconf call was not successful. Status Code is: {}').format(result.status_code)