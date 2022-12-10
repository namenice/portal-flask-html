import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    pathdb = "./databases/data.db"
    conn = sqlite3.connect(pathdb)
    conn.row_factory = sqlite3.Row
    return conn


def get_db(dbname):
    conn = get_db_connection()
    task = 'SELECT * FROM {}'.format(dbname)
    data = conn.execute(task).fetchall()
    conn.close()
    if data is None:
        abort(404)
    return data


def cluster_add(cluster):
    conn = get_db_connection()
    conn.execute('INSERT INTO clusters (name, ip, site, domain, username, password) VALUES (?, ?, ?, ?, ?, ?)',
                (cluster['name'], cluster['ip'], cluster['site'], cluster['domain'], cluster['username'], cluster['password']))
    conn.commit()
    conn.close()
    return "ok"

def cluster_edit(id,cluster):
    conn = get_db_connection()
    conn.execute('UPDATE clusters SET name = ?, ip = ?, site = ?, domain = ?, username = ?, password = ?' 
                 ' WHERE id = ?',
                 (cluster['name'], cluster['ip'], cluster['site'], cluster['domain'], cluster['username'], cluster['password'], id))
    conn.commit()
    conn.close()
    return "ok"

def cluster_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clusters WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return "ok"

######## network
def network_get(id):
    conn = get_db_connection()
    network = conn.execute('SELECT * FROM networks WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if network is None:
        abort(404)
    return network

def network_add(network):
    conn = get_db_connection()
    conn.execute('INSERT INTO networks (name, vlan, subnet, domain, vlanid) VALUES (?, ?, ?, ?, ?)',
                (network['name'], network['vlan'], network['subnet'], network['domain'], network['vlanid']))
    conn.commit()
    conn.close()
    return "ok"

def network_edit(id,network):
    conn = get_db_connection()
    conn.execute('UPDATE networks SET name = ?, vlan = ?, subnet = ?, domain = ?'
                 ' WHERE id = ?',
                 (network['name'], network['vlan'], network['subnet'], network['domain'], id))
    conn.commit()
    conn.close()
    return "ok"

def network_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM networks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return "ok"

####### ip
def ipaddress_add(ipaddress):
    conn = get_db_connection()
    conn.execute('INSERT INTO ipaddress (ip, status, macaddress,  vm, cluster, pool, detail, vlanid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (ipaddress['ip'], 'Available', '', '-', '-', '-', '-', ipaddress['vlanid']))
    conn.commit()
    conn.close()
    return "ok"

def ipaddress_delete(id):
    conn = get_db_connection()
    network = conn.execute('SELECT * FROM networks WHERE id = ?',
                        (id,)).fetchone()
    vlanid = network['vlanid']
    conn.execute('DELETE FROM ipaddress WHERE vlanid = ?', (vlanid,))
    conn.commit()
    conn.close()
    return "ok" 

def ipaddress_edit(id,ipaddr):
    conn = get_db_connection()
    conn.execute('UPDATE ipaddress SET vm = ?, cluster = ?, pool = ?, detail = ?'
                 ' WHERE id = ?',
                 (ipaddr['vm'], ipaddr['cluster'], ipaddr['pool'], ipaddr['detail'], id))
    conn.commit()
    conn.close()
    return "ok"

def ipaddress_update_mac(id,ipaddr,macaddress,status):
    conn = get_db_connection()
    network = conn.execute('SELECT * FROM networks WHERE id = ?',
                        (id,)).fetchone()
    vlanid = network['vlanid']
    conn.execute('UPDATE ipaddress SET macaddress = ?, status = ?'
                 'WHERE vlanid = ? and ip = ?',
                 (macaddress, status, vlanid, ipaddr))
    conn.commit()
    conn.close()
    return "ok"


def get_ipaddr(id):
    conn = get_db_connection()
    network = conn.execute('SELECT * FROM networks WHERE id = ?',
                        (id,)).fetchone()
    vlanid = network['vlanid']
    ipaddr = conn.execute('SELECT * FROM ipaddress WHERE vlanid = ?',
                        (vlanid,)).fetchall()
    conn.close()
    if ipaddr is None:
        abort(404)
    return ipaddr
    
 
##### rack
def rack_add(rack):
    conn = get_db_connection()
    conn.execute('INSERT INTO racks (name, site, room, floor, domain, rackid) VALUES (?, ?, ?, ?, ?, ?)',
                (rack['name'], rack['site'], rack['room'], rack['floor'], rack['domain'], rack['rackid']))
    conn.commit()
    conn.close()
    return "ok"

def rack_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM racks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return "ok"

##### switch
def switch_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM switchs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return "ok"

def switch_add(switch):
    conn = get_db_connection()
    conn.execute("INSERT INTO switchs (name, status, ip, site, domain, rack, unit, serialnumber, model, vender, note, rackid) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (switch['name'], switch['status'], switch['ip'], switch['site'], switch['domain'], switch['rack'], switch['unit'], switch['serialnumber'], switch['model'], switch['vender'], switch['note'], switch['rackid']))
    conn.commit()
    conn.close()
    return "ok"


def switch_edit(id,switch):
    conn = get_db_connection()
    conn.execute('UPDATE switchs SET name = ?, status = ?, ip = ?, site = ?, domain = ?, rack = ?, unit = ?, serialnumber = ?, model = ?, vender = ?, note = ?, rackid = ?'
                 ' WHERE id = ?',
                 (switch['name'], switch['status'], switch['ip'], switch['site'], switch['domain'], switch['rack'], switch['unit'], switch['serialnumber'], switch['model'], switch['vender'], switch['note'], switch['rackid'], id))
    conn.commit()
    conn.close()
    return "ok"

##### hw
def hw_add(hw):
    conn = get_db_connection()
    conn.execute("INSERT INTO hardwares (name, project, nameols, status, hwip, boxip, type, model, site, domain, rack, unit, hwserialnumber, boxserialnumber, switch01, port01, switch02, port02, vender, owner, note, rackid) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (hw['name'], hw['project'], hw['nameols'], hw['status'], hw['hwip'], hw['boxip'], hw['type'], hw['model'], hw['site'], hw['domain'], hw['rack'], hw['unit'], hw['hwserialnumber'], hw['boxserialnumber'], hw['switch01'], hw['port01'],hw['switch02'], hw['port02'], hw['vender'], hw['owner'], hw['note'], hw['rackid']))
    conn.commit()
    conn.close()
    return "ok"

def hw_delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM hardwares WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return "ok"

def hw_edit(id,hw):
    conn = get_db_connection()
    conn.execute('UPDATE hardwares SET name = ?, project = ?, nameols = ?, status = ?, hwip = ?, boxip = ?, type = ?, model = ?, site = ?, domain = ?, rack = ?, unit = ?, hwserialnumber = ?, boxserialnumber = ?, switch01 = ?, port01 = ?,switch02 = ?, port02 = ?, vender = ?, owner = ?, note = ?, rackid = ?'
                 ' WHERE id = ?',
                 (hw['name'], hw['project'], hw['nameols'], hw['status'], hw['hwip'], hw['boxip'], hw['type'], hw['model'], hw['site'], hw['domain'], hw['rack'], hw['unit'], hw['hwserialnumber'], hw['boxserialnumber'], hw['switch01'], hw['port01'],hw['switch02'], hw['port02'], hw['vender'], hw['owner'], hw['note'], hw['rackid'], id))
    conn.commit()
    conn.close()
    return "ok"




