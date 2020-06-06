# CyberSecLabs : Office 


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

