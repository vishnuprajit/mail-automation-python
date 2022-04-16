import smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 

print("### Automated mailing with Gmail using Python ###")
flag = input("Have you filled up the subject, body, and recipients text files in this folder (Y/n)? ")

if flag == "Y" or flag == "y" or flag == "yes" or flag == "YES" or flag == "Yes":
    pass
else:
    print("Go on and fill up the content...!")
    sys.exit(1)

print()
# Getting credentials, and attachment name from STDIN
sender_mail = input("Enter your Gmail ID: ")
print("NOTE: Turn on 'Less Secure App Access' in your Gmail in order to send the mail using this script !!!\n")           
sender_pass = input("Enter your password: ")                                       
print()
print("NOTE: Copy your attachment to this script's folder before proceeding...!")
print()
filename = input('Enter File Name With Extension To Attach: ')

# Getting recipients list, and reading the subject and body contents.
with open("recipients.txt", "r") as recipients:
    receiver_mails = recipients.read().splitlines()
with open("subject.txt", "r") as sub:
    subject = sub.read()
with open("body.txt", "r") as message_body:
    body = message_body.read()

# Iterating for each recipient mail
for i in range(len(receiver_mails)): 
    receiver_mail = receiver_mails[i]
    print("Sending mail to " + receiver_mail + "...!")
    message = MIMEMultipart()
    message['From'] = sender_mail
    message['To'] =  receiver_mail
    message['Subject'] =  subject

    message.attach(MIMEText(body, 'plain'))

    with open(filename, "rb") as attachment:
        # MIME attachment is a binary file for that content type "application/octet-stream" is used
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Base64 encoding 
    encoders.encode_base64(part) 

    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)  
    message.attach(part) 

    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(sender_mail, sender_pass) 
    text = message.as_string()
    s.sendmail(sender_mail, receiver_mail, text) 
    s.quit() 

    print('Mail sent to {} successfully...!'.format(receiver_mail))