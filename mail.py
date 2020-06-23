"""
This script sends the email with gpus.
I removed me and my friends email and the bots password
"""

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

class Email:
    def __init__(self):
        #Define emails and passwords
        self.smtp_server = "smtp.gmail.com"
        self.port = 587 
        self.sender_email = "sender_password"
        self.password = "sender_password"
        self.receiver_email_1 = "my_email"
        self.receiver_email_2 = "friends_email"

        #Create and send message
        self.create_msg()
        self.send_msg()

    #Connect to server and send the message
    def send_msg(self):
        context = ssl.create_default_context()

        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.ehlo() 
            server.starttls(context=context) 
            server.ehlo() 
            server.login(self.sender_email, self.password)
            # server.sendmail(self.sender_email, self.receiver_email_1, str(self.message))
            # server.sendmail(self.sender_email, self.receiver_email_2, str(self.message))

        except Exception as e:
            print(e)

        finally:
            server.quit() 

    def create_msg(self):
        #Create body and subject
        body = "See the attachment for the gpus. The first index contains todays prices, the second index contains yesterdays prices."
        subject = "gpus" + str(date.today())

        #Break up the message in parts
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = subject

        self.message.attach(MIMEText(body, "plain"))

        #Attach a file to the mail
        filename ="gpus.csv" 
        
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            self.message.attach(part)
            text = self.message.as_string()
            
        except FileNotFoundError:
            print("File doens't exist")
