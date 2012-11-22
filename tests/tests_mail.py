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


#unittest.main()
