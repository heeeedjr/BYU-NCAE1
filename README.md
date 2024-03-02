# BYU-NCAE1

## Start Here
- Get service up
- Change password for blueteam
- Create backup user and write down the password on the whiteboard
- Shutdown unnecessary ports and services
- Take backups
- Set static IP, gateway, and DNS server in `/etc/netplan/*.yaml`

### Static IP
If you don't have `Network Manager` installed, delete the renderer line from the .yaml file!

`/etc/netplan/00-installer-all.yaml`
``` yaml
network:
  version: 2
  renderer: NetworkManager <<< this line can get deleted if it causes problems
  ethernets:
    #interface name (Ex: ens18)
      addresses:
        - #ip address with CIDR (Ex: 192.168.<team>.<server>/24)
      dhcp4: false
      gateway4: #internal router IP (Ex: 192.168.1.1)
```

Apply Command:
`sudo netplan apply`

Use `ip r | grep default`, if you see the IP address you set for your gateway in your YAML file you are good to go!!
