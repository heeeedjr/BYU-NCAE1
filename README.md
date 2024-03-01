# BYU-NCAE1

## Start Here
- Get service up
- Change password for blueteam
- Create backup user and write down the password on the whiteboard
- Shutdown unnecessary ports and services
- Take backups
- Set static IP, gateway, and DNS server in `/etc/netplan/*.yaml`

###s Static IP
If you don't have `Network Manager` installed, delete the renderer line from the .yaml file!

`/etc/netplan/00-installer-all.yaml`
``` yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    #interface name (Ex: ens18)
      addresses:
        - #ip address with CIDR (Ex: 192.168.<team>.<server>)
      nameservers:
        addresses:
          - #ip address (Ex: 192.168.<team>.<dns_server>)
      dhcp4: false
      gateway4: <internal router ip>
```

Apply Command:
`sudo netplan apply`


Check to make sure our DNS server shows up here:
`/etc/resolv.conf`
``` bash
nameserver # ip of nameserver
```
