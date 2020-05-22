#Linux Privesc Cheatsheet

*User accounts*

Configured - ```/etc/passwd```
Hashes - ```/etc/shadow```

root user (uid-0)	

*Group accounts*

Configured - ```/etc/group```

*Permissions*

- Read Write and Execute

Only file owners can change the permission of a file.

*Special Permissions*

- SUID bit --> when this is set file gets executed by the privileges of the fileowner
- SGID bit --> when this is set file gets executed by the privileges of the file group

## Privilege Escalation Script

- LSE.sh

``` zsh
./lse.sh -i -l 1
./lse.sh -i -l 2
```

1 and 2 just give different amounts of info.

- LinEnum

```zsh
./LinEnum.sh -k password -e export -t
```

In this command it will look for the word password and puts the result in export directory (made by us). the ```t``` in the end is for thorough tests.

## Kernel Exploits

uname -a , searchsploit, compile and find.

```zsh
searchsploit linux kernel 2.6.32 priv esc
```
## Service Exploits

```zsh
ps aux | grep "^root"
```

Running this will let us know all the services running as root.

```zsh
dpkg -l | grep apache
```
Will give us the versions of the program

or
program -v or -vv

Port Forwarding:

```ssh -R 4444:127.0.0.1:3306 root@192.168.158.146```



## Weak file permissions

/etc/shadow file - modifiable or readable ?

head