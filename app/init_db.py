
import sqlite3

## create db cluster
connection = sqlite3.connect('./databases/data.db')

with open('schemaracks.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO clusters (name, ip, site, domain, username, password) VALUES (?, ?, ?, ?, ?, ?)",
#            ('pool test', '192.168.10.11', 'srb' , '3', 'root', 'password')
#            )

#cur.execute("INSERT INTO networks (name, vlan, subnet, domain, vlanid) VALUES (?, ?, ?, ?, ?)",
#            ('mgmt-test', '123', '192.168.10.0/24' , '3', '123')
#            )

#cur.execute("INSERT INTO ipaddress (ip, status, macaddress,  vm, cluster, pool, detail, vlanid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#            ('192.168.10.1', 'active', 'mac', 'vmtestna', 'draco' , 'pooltest', 'vm id 20000', '123')
#            )

#cur.execute("INSERT INTO racks (name, site, room, floor, domain, rackid) VALUES (?, ?, ?, ?, ?, ?)",
#            ('rack02-02-02', 'tst', 'room-d', '10', '3' , 'rack02-02-02tstroom-d')
#            )

cur.execute("INSERT INTO switchs (name, status, ip, site, domain, rack, unit, serialnumber, model, vender, note, rackid) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            ('1','2','3','4','5','6','7','8','9','10','11','12')
            )
cur.execute("INSERT INTO hardwares (name, project, nameols, status, hwip, boxip, type, model, site, domain, rack, unit, hwserialnumber, boxserialnumber, switch01, port01, switch02, port02, vender, owner, note, rackid) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22')
            )


connection.commit()
connection.close()

