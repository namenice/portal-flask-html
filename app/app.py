import logging
import requests
import ipaddress
import json
import xlwt
import io


from flask import Flask, render_template, request, url_for, flash, redirect, Response
from db import * 
from proxmoxer import ProxmoxAPI
from proxmoxs.sync_user_ad import verifyAuth, proxmoxSyncUser


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b9tt_#py=$fd++0l3cuuj@yaj#)$k0gd#km5!s!n^*5@(c*451'

logging.basicConfig(level=logging.DEBUG)


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clusterlist', methods=['GET'])
def clusterlist():
    clusters = get_db('clusters')
    return render_template('clusterlist.html', clusters=clusters) 


@app.route('/clusteradd', methods=['GET','POST'])
def clusteradd():
    if request.method == 'POST':
        name = request.form['name']
        ip = request.form['ip']
        site = request.form['site']
        domain = request.form['domain']
        username = request.form['username']
        password = request.form['password']

        if not name or not ip or not site or not domain or not username or not password:
            flash('Please enter all the fields.')
        else:
            cluster = {}
            cluster["name"] = name
            cluster["ip"] = ip
            cluster["site"] = site
            cluster["domain"] = domain
            cluster["username"] = username
            cluster["password"] = password
            cluster_add(cluster)
            flash('Complete add new cluster.')
            return redirect(url_for('clusterlist'))

@app.route('/clusteredit/<int:id>', methods=['GET','POST'])
def clusteredit(id):
    if request.method == 'POST':
        name = request.form['name']
        ip = request.form['ip']
        site = request.form['site']
        domain = request.form['domain']
        username = request.form['username']
        password = request.form['password']
        if not name or not ip or not site or not domain or not username or not password:
            flash('Please enter all the fields.')
        else:
            cluster = {}
            cluster["name"] = name
            cluster["ip"] = ip
            cluster["site"] = site
            cluster["domain"] = domain
            cluster["username"] = username
            cluster["password"] = password
            cluster_edit(id,cluster)
            flash('Complete Edit cluster.')
            return redirect(url_for('clusterlist'))

@app.route('/clusterdelete/<int:id>', methods=['GET','POST'])
def clusterdelete(id):
    cluster_delete(id)
    flash('Complete Delete cluster.')
    return redirect(url_for('clusterlist'))


########## networks
@app.route('/networklist', methods=['GET'])
def networklist():
    networks = get_db('networks')
    return render_template('networklist.html', networks=networks)

@app.route('/networkadd', methods=['GET','POST'])
def networkadd():
    if request.method == 'POST':
        name = request.form['name']
        vlan = request.form['vlan']
        subnet = request.form['subnet']
        domain = request.form['domain']
        vlanid = vlan+subnet+domain

        if not name or not vlan or not subnet or not domain:
            flash('Please enter all the fields.')
        else:
            network = {}
            network["name"] = name
            network["vlan"] = vlan
            network["subnet"] = subnet
            network["domain"] = domain
            network["vlanid"] = vlanid
            network_add(network)

            ipaddr = {}
            for ip in ipaddress.IPv4Network(str(subnet)).hosts():
                ipaddr["ip"] = str(ip)
                ipaddr["vlanid"] = vlanid
                ipaddress_add(ipaddr)

            flash('Complete add new network.')
            return redirect(url_for('networklist'))

@app.route('/networkedit/<int:id>', methods=['GET','POST'])
def networkedit(id):
    if request.method == 'POST':
        name = request.form['name']
        vlan = request.form['vlan']
        subnet = request.form['subnet']
        domain = request.form['domain']
        #vlanid = vlan+subnet+domain

        if not name or not vlan or not subnet or not domain:
            flash('Please enter all the fields.')
        else:
            network = {}
            network["name"] = name
            network["vlan"] = vlan
            network["subnet"] = subnet
            network["domain"] = domain
            #network["vlanid"] = vlanid
            network_edit(id,network)
            flash('Complete edit network.')
            return redirect(url_for('networklist'))

@app.route('/networkdelete/<int:id>', methods=['GET','POST'])
def networkdelete(id):
    ipaddress_delete(id)
    network_delete(id)
    flash('Complete Delete network.')
    return redirect(url_for('networklist'))

### ip address
@app.route('/ipaddresslist/<int:id>', methods=['GET'])
def ipaddresslist(id):
    ipaddr = get_ipaddr(id)
    return render_template('ipaddrlist.html', ipaddr=ipaddr)

@app.route('/ipaddressedit/<int:id>', methods=['GET','POST'])
def ipaddressedit(id):
    if request.method == 'POST':
        vm = request.form['vm']
        cluster = request.form['cluster']
        pool = request.form['pool']
        detail = request.form['detail']

        if not vm or not cluster or not pool or not detail:
            flash('Please enter all the fields.')
        else:
            ipaddr = {}
            ipaddr["vm"] = vm
            ipaddr["cluster"] = cluster
            ipaddr["pool"] = pool
            ipaddr["detail"] = detail
            ipaddress_edit(id,ipaddr)
            flash('Complete edit IP Address.')
            return redirect(url_for('networklist'))

#### sync ad
@app.route('/syncuserad', methods=['GET','POST'])
def syncuserad():
    clusters = get_db('clusters')
    logging.info (clusters)
    for cluster in clusters:
        logging.info(cluster)
        response = verifyAuth(cluster)
        if str(response["status_code"]) == "200":
            proxmoxSyncUser(cluster)
        else:
            flash('error sync user ad!!!!! Plese Try again !!!! : "{}"'.format(response["reason"]))
            return redirect(url_for('clusterlist'))
    flash('Complate Sync user with AD.')
    return redirect(url_for('clusterlist'))

#### scan ip
@app.route('/scanip/<int:id>', methods=['GET'])
def scanip(id):
    network = network_get(id)
    domain = [1,2,3,4]
    if network['domain'] in domain:
        if network['domain'] == 1:
            flash('scan ip domain {}.'.format(network['domain']))
        if network['domain'] == 2:
            flash('scan ip domain {}.'.format(network['domain']))
        if network['domain'] == 3:
            payload = {'subnet': network['subnet']}
            datares = requests.post("http://172.16.11.12:5000/scanip", data=payload)
            if str(datares.status_code) == "200":
                datares = json.loads(datares.text)
                for data in datares:
                    ip = str(data['ip'])
                    mac = str(data['macaddress'])
                    if str(mac) == "None":
                        status = "Available"
                    else:
                        status = "Active"
                    mac_update = ipaddress_update_mac(id,ip,mac,status)
                flash('Complete scan ip.')
                return redirect(url_for('networklist'))
            else:
                flash('error sync user ad!!!!! Plese Try again !!!! : "{}"'.format(response["reason"]))
                return redirect(url_for('networklist'))
        if network['domain'] == 4:
            flash('scan ip domain {}.'.format(network['domain']))
    else:
        flash('not have domain {}.'.format(network['domain']))
        return redirect(url_for('networklist'))
    return redirect(url_for('networklist'))

@app.route('/reportsubnet/<int:id>', methods=['GET'])
def reportsubnet(id):
    data = get_ipaddr(id)
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('IP Report')

    #add headers
    sh.write(0, 0, 'IP')
    sh.write(0, 1, 'Status')
    sh.write(0, 2, 'Macaddress')
    sh.write(0, 3, 'VM')
    sh.write(0, 4, 'Cluster')
    sh.write(0, 5, 'Pool')
    sh.write(0, 6, 'Detail')

    idx = 0
    for row in data:
        sh.write(idx+1, 0, str(row['ip']))
        sh.write(idx+1, 1, row['status'])
        sh.write(idx+1, 2, row['macaddress'])
        sh.write(idx+1, 3, row['vm'])
        sh.write(idx+1, 4, row['cluster'])
        sh.write(idx+1, 5, row['pool'])
        sh.write(idx+1, 6, row['detail'])
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=ip_report.xls"})


@app.route('/exporthw', methods=['GET'])
def exporthw():
    data = get_db('hardwares') 
    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sh = workbook.add_sheet('list-hardware')

    #add headers
    sh.write(0, 0, 'name')
    sh.write(0, 1, 'project')
    sh.write(0, 2, 'nameols')
    sh.write(0, 3, 'status')
    sh.write(0, 4, 'hwip')
    sh.write(0, 5, 'boxip')
    sh.write(0, 6, 'type')
    sh.write(0, 7, 'model')
    sh.write(0, 8, 'site')
    sh.write(0, 9, 'domain')
    sh.write(0, 10, 'rack')
    sh.write(0, 11, 'unit')
    sh.write(0, 12, 'hwserialnumber')
    sh.write(0, 13, 'boxserialnumber')
    sh.write(0, 14, 'switch')
    sh.write(0, 15, 'port')
    sh.write(0, 16, 'vender')
    sh.write(0, 17, 'owner')
    sh.write(0, 18, 'note')
    
    idx = 0
    
    for row in data:
        sh.write(idx+1, 0, row['name'])
        sh.write(idx+1, 1, row['project'])
        sh.write(idx+1, 2, row['nameols'])
        sh.write(idx+1, 3, row['status'])
        sh.write(idx+1, 4, row['hwip'])
        sh.write(idx+1, 5, row['boxip'])
        sh.write(idx+1, 6, row['type'])
        sh.write(idx+1, 7, row['model'])
        sh.write(idx+1, 8, row['site'])
        sh.write(idx+1, 9, row['domain'])
        sh.write(idx+1, 10, row['rack'])
        sh.write(idx+1, 11, row['unit'])
        sh.write(idx+1, 12, row['hwserialnumber'])
        sh.write(idx+1, 13, row['boxserialnumber'])
        sh.write(idx+1, 14, row['switch'])
        sh.write(idx+1, 15, row['port'])
        sh.write(idx+1, 16, row['vender'])
        sh.write(idx+1, 17, row['owner'])
        sh.write(idx+1, 18, row['note'])
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=list_hardware.xls"})


## racks
@app.route('/racklist', methods=['GET'])
def racklist():
    racks = get_db('racks')
    return render_template('racklist.html', racks=racks)


@app.route('/rackadd', methods=['GET','POST'])
def rackadd():
    if request.method == 'POST':
        name = request.form['name']
        site = request.form['site']
        room = request.form['room']
        floor = request.form['floor']
        domain = request.form['domain']
        rackid = name + site 

        if not name or not site or not room or not floor or not domain:
            flash('Please enter all the fields.')
        else:
            rack = {}
            rack["name"] = name
            rack["site"] = site
            rack["room"] = room
            rack["floor"] = floor
            rack["domain"] = domain
            rack["rackid"] = rackid
            rack_add(rack)
            flash('Complete add new rack.')
            return redirect(url_for('racklist'))

@app.route('/rackdelete/<int:id>', methods=['GET','POST'])
def rackdelete(id):
    rack_delete(id)
    flash('Complete Delete Rack.')
    return redirect(url_for('racklist'))


## switchs
@app.route('/switchlist', methods=['GET'])
def switchlist():
    switchs = get_db('switchs')
    racks = get_db('racks')
    return render_template('switchlist.html', switchs=switchs, racks=racks)

@app.route('/switchdelete/<int:id>', methods=['GET','POST'])
def switchdelete(id):
    switch_delete(id)
    return redirect(url_for('switchlist'))

@app.route('/switchadd', methods=['GET','POST'])
def switchadd():
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        ip = request.form['ip']
        site = request.form['site']
        domain = request.form['domain']
        rack = request.form['rack']
        unit = request.form['unit']
        serialnumber = request.form['serialnumber']
        model = request.form['model']
        vender = request.form['vender']
        note = request.form['note']
        rackid = rack + site

        if not name or not status or not ip or not site or not domain or not rack or not unit or not serialnumber or not model or not vender:
            flash('Please enter all the fields.')
        else:
            switch = {}
            switch["name"] = name
            switch["status"] = status
            switch["ip"] = ip
            switch["site"] = site
            switch["domain"] = domain
            switch["rack"] = rack
            switch["unit"] = unit
            switch["serialnumber"] = serialnumber
            switch["model"] = model
            switch["vender"] = vender
            switch["note"] = note
            switch["rackid"] = rackid
            switch_add(switch)
            flash('Complete add new switch.')

    return redirect(url_for('switchlist'))


@app.route('/switchedit/<int:id>', methods=['GET','POST'])
def switchedit(id):
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        ip = request.form['ip']
        site = request.form['site']
        domain = request.form['domain']
        rack = request.form['rack']
        unit = request.form['unit']
        serialnumber = request.form['serialnumber']
        model = request.form['model']
        vender = request.form['vender']
        note = request.form['note']
        rackid = rack + site

        if not name or not status or not ip or not site or not domain or not rack or not unit or not serialnumber or not model or not vender:
            flash('Please enter all the fields.')
        else:
            switch = {}
            switch["name"] = name
            switch["status"] = status
            switch["ip"] = ip
            switch["site"] = site
            switch["domain"] = domain
            switch["rack"] = rack
            switch["unit"] = unit
            switch["serialnumber"] = serialnumber
            switch["model"] = model
            switch["vender"] = vender
            switch["note"] = note
            switch["rackid"] = rackid
            switch_edit(id,switch)
            flash('Complete Edit switch.')

    return redirect(url_for('switchlist'))


## hardwares
@app.route('/hwlist', methods=['GET'])
def hwlist():
    hardwares = get_db('hardwares')
    racks = get_db('racks')
    switchs = get_db('switchs')
    return render_template('hwlist.html', hardwares=hardwares, racks=racks, switchs=switchs)

@app.route('/hwdelete/<int:id>', methods=['GET','POST'])
def hwdelete(id):
    hw_delete(id)
    return redirect(url_for('hwlist'))

@app.route('/hwadd', methods=['GET','POST'])
def hwadd():
    if request.method == 'POST':
        name = request.form['name']
        project = request.form['project']
        nameols = request.form['nameols']
        status = request.form['status']
        hwip = request.form['hwip']
        boxip = request.form['boxip']
        type = request.form['type']
        model = request.form['model']
        site = request.form['site']
        domain = request.form['domain']
        rack = request.form['rack']
        unit = request.form['unit'] 
        hwserialnumber = request.form['hwserialnumber']
        boxserialnumber = request.form['boxserialnumber']
        switch01 = request.form['switch01']
        port01 = request.form['port01']
        switch02 = request.form['switch02']
        port02 = request.form['port02']
        vender = request.form['vender']
        owner = request.form['owner']
        note = request.form['note']
        rackid = rack + site

        if not name or not project or not nameols or not status or not hwip or not  boxip or not type or not model or not site or not domain or not rack or not unit or not switch01 or not port01 or not vender or not owner or not note or not hwserialnumber or not boxserialnumber:
            flash('Please enter all the fields.')
        else:
            hw = {}
            hw["name"] = name
            hw["project"] = project
            hw["nameols"] = nameols
            hw["status"] = status
            hw["hwip"] = hwip
            hw["boxip"] = boxip
            hw["type"] = type
            hw["model"] = model
            hw["site"] = site
            hw["domain"] = domain
            hw["rack"] = rack
            hw["unit"] = unit
            hw["hwserialnumber"] = hwserialnumber
            hw["boxserialnumber"] = boxserialnumber
            hw["switch01"] = switch01
            hw["port01"] = port01
            hw["switch02"] = switch02
            hw["port02"] = port02
            hw["vender"] = vender
            hw["owner"] = owner
            hw["note"] = note
            hw["rackid"] = rackid
            hw_add(hw)
            flash('Complete add new hardware.')
    return redirect(url_for('hwlist'))

@app.route('/hwedit/<int:id>', methods=['GET','POST'])
def hwedit(id):
    if request.method == 'POST':
        name = request.form['name']
        project = request.form['project']
        nameols = request.form['nameols']
        status = request.form['status']
        hwip = request.form['hwip']
        boxip = request.form['boxip']
        type = request.form['type']
        model = request.form['model']
        site = request.form['site']
        domain = request.form['domain']
        rack = request.form['rack']
        unit = request.form['unit']
        hwserialnumber = request.form['hwserialnumber']
        boxserialnumber = request.form['boxserialnumber']
        switch01 = request.form['switch01']
        port01 = request.form['port01']
        switch02 = request.form['switch02']
        port02 = request.form['port02']
        vender = request.form['vender']
        owner = request.form['owner']
        note = request.form['note']
        rackid = rack + site

        if not name or not project or not nameols or not status or not hwip or not  boxip or not type or not model or not site or not domain or not rack or not unit or not switch01 or not port01 or not vender or not owner or not note or not hwserialnumber or not boxserialnumber:
            flash('Please enter all the fields.')
        else:
            hw = {}
            hw["name"] = name
            hw["project"] = project
            hw["nameols"] = nameols
            hw["status"] = status
            hw["hwip"] = hwip
            hw["boxip"] = boxip
            hw["type"] = type
            hw["model"] = model
            hw["site"] = site
            hw["domain"] = domain
            hw["rack"] = rack
            hw["unit"] = unit
            hw["hwserialnumber"] = hwserialnumber
            hw["boxserialnumber"] = boxserialnumber
            hw["switch01"] = switch01
            hw["port01"] = port01
            hw["switch02"] = switch02
            hw["port02"] = port02
            hw["vender"] = vender
            hw["owner"] = owner
            hw["note"] = note
            hw["rackid"] = rackid
            hw_edit(id,hw)
            flash('Complete Edit Hardware.')
    return redirect(url_for('hwlist'))





if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

