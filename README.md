## Install Grafana
Updatte and Upgrade package
```sh
sudo apt update -y
sudo apt upgrade -y
```
First, install all required dependencies using the following command
```sh
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```
Add this repository for stable releases  
```sh
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```
After you add the repository
```sh
sudo apt-get update
sudo apt-get install grafana -y
```
Verify Grafana server
```sh
grafana-server -v
```
Now, start the Grafana service and enable it to start at system
```sh
systemctl start grafana-server
systemctl enable grafana-server
systemctl restart grafana-server
```
Check the status of the Grafana
```sh
systemctl status grafana-server
``` 

## Install Prometheus
Download Package Prometheus
```sh
wget https://github.com/prometheus/prometheus/releases/download/v2.40.2/prometheus-2.40.2.linux-amd64.tar.gz
```
Unpackag Prometheus
```sh
tar xvfz prometheus-2.40.2.linux-amd64.tar.gz
cd prometheus-2.40.2.linux-amd64
```
Create a Prometheus user, required directories, and make Prometheus the user as the owner of those directories
```sh
sudo useradd --no-create-home --shell /bin/false prometheus
sudo mkdir /etc/prometheus  
sudo mkdir /var/lib/prometheus
sudo chown prometheus:prometheus /etc/prometheus
sudo chown prometheus:prometheus /var/lib/prometheus
```
Copy prometheus and promtool binary to /usr/local/bin and change the ownership to prometheus user
```sh
sudo cp prometheus /usr/local/bin/
sudo cp promtool /usr/local/bin/
sudo chown prometheus:prometheus /usr/local/bin/prometheus
sudo chown prometheus:prometheus /usr/local/bin/promtool
```
Move the consoles and console_libraries directories to /etc/prometheus folder and change the ownership to prometheus user
```sh
sudo cp -r consoles /etc/prometheus/
sudo cp -r console_libraries /etc/prometheus/
sudo chown -R prometheus:prometheus /etc/prometheus/consoles
sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries
```
Create Prometheus config
```sh
sudo vi /etc/prometheus/prometheus.yml
```
Copy the following content to the file
```sh
global:
  scrape_interval: 30s

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 10s
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'node_exporter'
    scrape_interval: 10s
    static_configs:
      - targets: ['localhost:9100']
```
Change the ownership of the file to prometheus user
```sh
sudo chown prometheus:prometheus /etc/prometheus/prometheus.yml
```
Create a prometheus service file
```sh
sudo vi /etc/systemd/system/prometheus.service 
```
Copy the following content to the file
```sh
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```
Reload the systemd service
```sh
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl restart prometheus
```
Check the prometheus service status
```sh
sudo systemctl status prometheus
```
Access Prometheus Web UI
```sh
http://<prometheus-ip>:9090/
```

## Install Node Exporter 
Download Package Node Exporter
```sh
wget https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-amd64.tar.gz
```
Unpackage Node Exporter
```sh
tar xvfz node_exporter-1.4.0.linux-amd64.tar.gz
cd node_exporter-1.4.0.linux-amd64
```
Create Node Exporter User
```sh
sudo useradd --no-create-home --shell /bin/false node_exporter
```
Copy node_exporter binary to /usr/local/bin and change the ownership to node_exporter user
```sh
sudo cp node_exporter /usr/local/bin
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```
Create a node exporter service file
```sh
sudo vi /etc/systemd/system/node_exporter.service
```
Copy the following content to the file
```sh
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```
Reload the systemd service
```sh
sudo systemctl daemon-reload
sudo systemctl start node_exporter.service 
sudo systemctl restart node_exporter.service
```
Check the prometheus service status
```sh
sudo systemctl status node_exporter.service
```
Verify Node Exporter service
```sh
curl 127.0.0.1:9100/metrics
```

