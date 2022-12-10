from proxmoxer import ProxmoxAPI

import logging
import requests
import json


def proxmoxSyncUser(cluster):
    proxmox = ProxmoxAPI(str(cluster['ip']) + ":8006/api2/json/access/ticket",user=str(cluster['username']),password=cluster['password'],verify_ssl=False)
    proxmoxSyncUser = proxmox.access.domains.openlandscape.sync.post()
    return proxmoxSyncUser

def verifyAuth(cluster):
    try:
      name = cluster['name']
      url = cluster['ip']
      user = cluster['username']
      password = cluster['password']
      logging.info("start verify++++++++++++")
      logging.info(url)
      data_req = {}
      r = requests.post("https://"+str(url)+":8006/api2/json/access/ticket",verify=False,data={ "username":user, "password":password },timeout=5)
      r.close()
      data_req["name"] = str(name)
      data_req["url"] = str(url)
      data_req["status_code"] = r.status_code
      data_req["reason"] = r.reason
      return (data_req)
    except Exception as error:
      data_req = {}
      data_req["name"] = str(name)
      data_req["url"] = str(url)
      data_req["status_code"] = "error"
      data_req["reason"] = str(error)
      return (data_req)

