### Static IP
`/etc/netplan/00-installer-all.yaml`
``` yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    #interface name:
      addresses:
        - #ip address with CIDR
      nameservers:
        addresses:
          - #ip address
      dhcp4: false
```

Apply Command:
`sudo netplan apply`


`/etc/resolv.conf`
``` bash
nameserver # ip of nameserver
```
### DNS
#### Helpful  Packages
- `bind9utils`
- `bind9-doc`


#### Forward Lookup:
- Domain Name -> IP Address
#### Reverse Lookup:
- IP Address -> Domain Name


#### Status
- `systemctl status bind9`
OR
- `systemctl status named`


#### FILES
Add zones into: `/etc/bind/named.conf.default-zones` or `/etc/bind/named.conf.local`
``` bash
# looks up ip address for subdomains on ncaecybergames.org
zone "ncaecybergames.org = forward" IN {
	type master;
	file "/etc/bind/zones/forward.ncaecybergames.org"
	allow-update { none; };
};

# looks up the domain name for things on the 192.168.1.0/24 network
zone "1.168.192.in-addr.arpa = reverse" IN {
	type master;
	file "/etc/bind/zones/reverse.ncaecybergames.org"
	allow-update { none; };
};

# looks up the domain name for things on the 172.10.0.0/16 network
zone "20.172.in-addr.arpa = reverse" IN {
	type master;
	file "/etc/bind/zones/reverse.ncaecybergames.org"
	allow-update { none; };
};
```


`/etc/bind/zones/forward.ncaecybergames.org`:
``` bash
$TTL    604800
@       IN      SOA     ncaecybergames.org. root.ncaecybergame.org. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@        IN    NS        ns1.ncaecybergames.org

ns1      IN    A         192.168.1.2
www      IN    A         192.168.1.3
score    IN    A         172.20.0.1 # if its score.ncaecybergames.org
```

`/etc/bind/zones/reverse.ncaecybergames.org`:
``` bash
$TTL    604800
@       IN      SOA     ncaecybergames.org. root.ncaecybergames.org. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@        IN    NS        ns1.ncaecybergames.org.

2        IN    PTR       ns1.cybergames.org.
3        IN    PTR       www.ncaecybergames.org.
1.0      IN    PTR       score.ncaecybergames.org.
```

#### Tools to Help
- `sudo named-checkconf`: checks for syntax errors in my bind conf files
- `sudo named-checkzone <domain-name> <file for domain-name>`: forward lookup
- `sudo named-checkzone <ip address> <file for ip address>`: reverse lookup


#### External DNS Requests
- Set external machines to send query to external IP of router: nameserver -> 172.20.1.1
###### Firewall on Router
- `sudo firewall-cmd --zone=external --permanent --add-forward-port=port=53:proto=udp:toport=53:toaddr=192.168.1.2`
- `sudo firewall-comd --reload`

`/etc/sysconfig/network-scripts/ifcfg-<interface>`
```bash
# Add this line in external interface
DNS1=172.16.0.1 # external DNS server

# Add this line in internal interface
DNS1=192.168.1.2 # internal DNS server
```

