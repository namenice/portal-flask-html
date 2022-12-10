

DROP TABLE IF EXISTS clusters;
CREATE TABLE clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ip TEXT NOT NULL,
    site TEXT NOT NULL,
    domain INTEGER NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    );

DROP TABLE IF EXISTS networks;
CREATE TABLE networks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    vlan INTEGER NOT NULL,
    subnet TEXT NOT NULL,
    domain INTEGER NOT NULL,
    vlanid TEXT NOT NULL
    );

DROP TABLE IF EXISTS ipaddress;
CREATE TABLE ipaddress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    status TEXT NOT NULL,
    macaddress TEXT NOT NULL,
    vm TEXT NOT NULL,
    cluster TEXT NOT NULL,
    pool TEXT NOT NULL,
    detail TEXT NOT NULL,
    vlanid TEXT NOT NULL,
    FOREIGN KEY(vlanid) REFERENCES networks(vlanid)
    );


DROP TABLE IF EXISTS racks;
CREATE TABLE racks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    site TEXT NOT NULL,
    room TEXT NOT NULL,
    floor INTEGER NOT NULL,
    domain INTEGER NOT NULL,
    rackid TEXT NOT NULL
    );


DROP TABLE IF EXISTS switchs;
CREATE TABLE switchs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    ip TEXT NOT NULL,
    site TEXT NOT NULL,
    domain INTEGER NOT NULL,
    rack TEXT NOT NULL,
    unit TEXT NOT NULL,
    serialnumber TEXT NOT NULL,
    model TEXT NOT NULL,
    vender TEXT NOT NULL,
    note TEXT,
    rackid TEXT NOT NULL,
    FOREIGN KEY(rackid) REFERENCES racks(rackid)
    );

DROP TABLE IF EXISTS hardwares;
CREATE TABLE hardwares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    project TEXT NOT NULL,
    nameols TEXT NOT NULL,
    status TEXT NOT NULL,
    hwip TEXT NOT NULL,
    boxip TEXT NOT NULL,
    type TEXT NOT NULL,
    model TEXT NOT NULL,
    site TEXT NOT NULL,
    domain INTEGER NOT NULL,
    rack TEXT NOT NULL,
    unit TEXT NOT NULL,
    hwserialnumber TEXT NOT NULL,
    boxserialnumber TEXT NOT NULL,
    switch01 TEXT NOT NULL,
    port01 TEXT NOT NULL,
    switch02 TEXT NOT NULL,
    port02 TEXT NOT NULL,
    vender TEXT NOT NULL,
    owner TEXT NOT NULL,
    note TEXT,
    rackid TEXT NOT NULL,
    FOREIGN KEY(rackid) REFERENCES racks(rackid)
    );





