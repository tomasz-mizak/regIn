import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# TODO: Exception handling

class MailService():

    def __init__(self, **kwargs):
        self.server = smtplib.SMTP('smtp.office365.com',587)
        self.server.ehlo()
        self.server.starttls()
        # save data from kwargs
        login = kwargs['login'] or kwargs['Login']
        self.from_addr = login # always in this case!
        password = kwargs['password'] or kwargs['Password']
        if (login != None and password != None):
            self.server.login(login, password)
    
    def close(self):
        self.server.quit()

    def send(self, **kwargs):

        # create MimeMultipart
        msg = MIMEMultipart()

        # setup primary data
        msg['From'] = self.from_addr
        msg['To'] = kwargs['to']
        msg['Subject'] = kwargs['subject'] 

        # define MimeText as HTML
        html_text = MIMEText(kwargs['msg'], 'html', 'UTF-8')

        # attach to msg
        msg.attach(html_text)     

        # try to send mail
        try:
            self.server.sendmail(self.from_addr, kwargs['to'], msg.as_string())
        except Exception as ex:
            print(ex)