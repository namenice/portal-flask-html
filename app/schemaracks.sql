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

