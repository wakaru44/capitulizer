# -*- coding: utf-8 *-*

# test provisional para probar como funciona el testing en appengine

import unittest
from google.appengine.ext import testbed
from google.appengine.api import mail


class MailTestCase(unittest.TestCase):

#    def __init__(self):
#        super(MailTestCase, self).__init__()

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def send_Email():
        mail.send_mail(to='wakaru44@gmail.com',
            subject='this is a mail test',
            sender='capitulos@waklab0.appspotmail.com',
            body=u'this is a test mail body.'
            ) 

    def testMailSent(self):
        self.send_Email()
        messages_sent = self.mail_stub.get_sent_messages(to='wakaru44@gmail.com')
        self.assertEqual(1, len(messages))
        self.assertEqual('wakaru44@gmail.com', messages[0].to)

#unittest.main()
