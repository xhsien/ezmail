import csv
import sys
import yaml
import smtplib
import itertools
from string import Template
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool


def start_server(conf):
    host = conf['host']
    port = conf['port']
    username = conf['username']
    password = conf['password']

    server = smtplib.SMTP(host=host, port=port)
    server.starttls()
    server.login(username, password)
    return server


def read_template(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    return Template(content)


def read_contacts(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        contacts = list(csv.DictReader(f))
    return contacts


def send_email(contact, template, conf):
    msg = MIMEMultipart()

    # Meta
    msg['To'] = contact['email']
    msg['Cc'] = conf['email-data']['cc']
    msg['From'] = conf['email-data']['from']
    msg['Subject'] = conf['email-data']['subject']

    # Body
    body = template.substitute(contact)
    msg.attach(MIMEText(body, 'html'))

    # Attachments
    for f in config['email-data']['attachments']:
        with open(f, 'rb') as file:
            part = MIMEApplication(file.read(), Name=basename(f))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    try:
        server = start_server(conf['server'])
        server.send_message(msg)
        print("Email sent to: " + contact['email'])
    except:
        print("Unsuccesful for " + contact['email'])


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("Missing yaml file! Aborting...")
        exit(0)

    with open(sys.argv[1]) as stream:    
        config = yaml.load(stream)

    print("Logging into mailing server...")
    start_server(config['server'])
    print("Login successful!")

    template = read_template(config['data']['template'])
    contacts = read_contacts(config['data']['contacts'])

    pool = Pool(cpu_count())
    results = pool.starmap(send_email, zip(contacts, itertools.repeat(template), itertools.repeat(config)))
