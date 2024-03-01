config file location: /etc/sysconfig/network-scripts

You may have to create new config files for the interfaces you're provided. Here's a general template:

TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens18
UUID= # use uuidgen <interface> to generate this
DEVICE=ens18
ONBOOT=yes
IPADDR=172.16.4.T  # external/internal router ip
NETMASK=255.255.0.0 (external) OR 255.255.255.0 (internal)
ZONE=external/internal
GATEWAY=172.16.0.1 # external gateway to scoring box
DNS1= # alex does this

Then restart: sudo systemctl restart network
(changes may not show up with ip a command; try ifconfig)

Then create port forwarding rule:
sudo firewall-cmd --zone=external --add-forward-port=port=80:proto=tcp:toport=80:toaddr=${web server addr} --permanent

Then create a gateway on the web server box by editing the 00-installer-config.yaml (or equivalent)
Here's a template:

network:
  ethernets:
    ens18:  # external interface
      gateway4: 192.168.T.1   # internal IP of router
      dhcp4: no
      addresses:
        - 192.168.T.3/24  # address of web server
      nameservers:
        addresses: [1.1.1.1]
  version: 2

then set up a gateway in the kali box to the scoring box, wait for firewall to finish setup, then try and ping scoring box. if you can, you can get points. if you can't, fix it.
