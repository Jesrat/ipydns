#!/usr/bin/python

import os
import re
import json
import paramiko
from datetime import datetime

pSsh_host = ''
pSsh_port = 22
pSsh_user = ''

HOME_DIR = os.path.dirname(__file__)
JSON_FILE = os.path.join(HOME_DIR, "data.json")


def main():

    with open(JSON_FILE, "r") as rawjson:
        jsonData = json.load(rawjson)

    vIp = newIp(jsonData)
    print('vIp is: {0}'.format(vIp))
    if vIp:
        vTimes = getTimes(jsonData)
        vCommand = 'iprenew {0} {1:02d}'.format(vIp, vTimes)

        print('comand to send is: {0}'.format(vCommand))

        dnsServer = paramiko.SSHClient()
        dnsServer.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dnsServer.connect(hostname=pSsh_host, port=pSsh_port, username=pSsh_user)
        _ = dnsServer.exec_command(vCommand)
        dnsServer.close()

        jsonData['lastIp'] = vIp
        jsonData['times'] = vTimes
        jsonData['on'] = '{0:%d%m%Y%H%M%S}'.format(datetime.now())

        with open(JSON_FILE, "w") as f:
            f.write(json.dumps(jsonData))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getTimes(pJData):
    vUpd = datetime.strptime(pJData['on'], '%d%m%Y%H%M%S')

    if datetime.today().date() == vUpd.date():
        return 1 if pJData['times'] > 98 else pJData['times'] + 1
    else:
        return 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def newIp(pJData):
    raw = os.popen('curl ipinfo.io/ip').read()
    res = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', raw)
    if res.group(0) != pJData['lastIp']:
        return res.group(0)
    else:
        return False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    main()