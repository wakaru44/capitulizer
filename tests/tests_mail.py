# -*- coding: utf-8 *-*
# define tests for the email service

import unittest
from google.appengine.api import mail
from google.appengine.ext import testbed


class MailTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def testMailSent(self):
        mail.send_mail(to='alice@example.com',
                       subject='This is a test',
                       sender='bob@example.com',
                       body='This is a test e-mail')
        messages = self.mail_stub.get_sent_messages(to='alice@example.com')
        self.assertEqual(1, len(messages))
        self.assertEqual('alice@example.com', messages[0].to)

    def test_compose_email_good(self):
        """prueba el compositor de emails con una
            lista buena de varios prov."""
        pass

    def test_compose_email_somebad(self):
        """test compose_email with a list with a few of empty elements"""
        pass

    def test_compose_email2_good(self):
        """test compose_email2 with a list of good links to variuos prov."""
        pass

from email.message import Message 

def test_email(self):
    body = Message()
    body.add_header('to', 'test-unknown@other-app.com')
    body.add_header('from', 'test@app.com')
    body.add_header('Content-Type', 'multipart/alternative',
                    boundary=self.boundary)
    text = Message()
    text['content-type'] = 'text/plain'
    text.set_payload('I am I! Don Quixote!  The man of La
                       Mancha!')
    body.attach(text)

    post(payload=body.as_string())


def createPayloadForEmail(bodyTxt):
    body = Message()
    body.add_header('to', 'agregar@capitulizer.appspotmail.com')
    body.add_header('from', 'manolo@nomail.com')
    body.add_header('Content-Type', 'multipart/alternative',
                    boundary=self.boundary)
    text = Message()
    text = ['content-type'] = 'text/plain'
    text.set_payload(bodyTxt)
    body.attach(text)
    return body.as_string()




#unittest.main()
