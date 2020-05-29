10.10.10.7


Can be exploited in many ways

- Using LFI, taking out password and login as SSH

```https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../../etc/amportal.conf%00&module=Accounts&action```

Get the password login via ssh as root

- Using Shellshock

Webmin hosted at port 10000

```zsh
searchsploit webmin 1.5 
```
You will find this ```Webmin 1.580 - '/file/show.cgi' Remote Command Execution```

Now we will not use metasploit for it.

Simply fire up burp and simply add the shellshock code for a reverse like in my ```Shocker Video```.

- Using an RCE 

```FreePBX 2.10.0 / Elastix 2.2.0 - Remote Code Execution```

This will be the current exploit. Throws SSL error.
By passed this using burp. Changed https to http in the code. RHOST as localhost. Changed extentsion to 233. Add a listener on BURP at port 80, Redirection to 10.10.10.7 port 443, Force use of TLS.