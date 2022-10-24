import smtplib                             
from email.mime.text import MIMEText
import os,environ
from pathlib import Path

def sendMail(recvEmail,title,content) :

    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
    environ.Env.read_env(
    env_file=os.path.join(ROOT_DIR, '.env')
    )

    env = environ.Env(DEBUG=(bool, True))

    smtpName = "smtp.naver.com"                  
    smtpPort = "587"                             

    sendEmail = env('MAIL_ID')
    password = env('MAIL_PW') 

    msg = MIMEText(content)                      
    msg['From'] = sendEmail
    msg['To'] = recvEmail
    msg['Subject'] = title                   

    s = smtplib.SMTP(smtpName , smtpPort)         
    s.starttls()                                
    s.login(sendEmail , password)
    s.sendmail(sendEmail, recvEmail, msg.as_string()) 
    s.close()