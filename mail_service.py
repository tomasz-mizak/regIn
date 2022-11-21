import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Patterns to implement in main.py
from datetime import datetime

test_inserts = 12
success = 0
MSG_PATTERN = f'''
<b>regIn monit, date {datetime.today()}</b>
<b>detected inserts:</b> {test_inserts}
<b>successful inserts:</b> {success}
'''
# if exceptions exist, add to MSG_PATTERN AS:
ex_pattern = '''
<br><br>
<b>Handled exception!</b>
<p>EXCEPTION ARGUMENTS</p>
'''

print(MSG_PATTERN)