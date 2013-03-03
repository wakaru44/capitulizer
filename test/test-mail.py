# -*- coding: utf-8 *-*
# define tests for the email service
# trying to use the taskqueue stub. By now the state is unknow

import unittest
from google.appengine.api import mail
from google.appengine.api import taskqueue
from google.appengine.ext import testbed

from email.message import Message 

import tasks.newEmail as numail

class MailTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_mail_stub()
        self.testbed.init_taskqueue_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        self.task_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
        self.task_stub._ParseQueueYaml  ## Is it working?

    def tearDown(self):
        self.testbed.deactivate()

    def sendEmail(self):
        """ """
        mail.send_mail(to='trigger@ifttt.com',
                       subject=u'ver True Blood Capitulo 7',
                       sender='capitulizer@capitulizer.appspotmail.com',
                       body='automagicoespialidoso, True Blood, ',
                       html='<html></html>')
        #TODO this is bullshit



    def testMailSent(self):
        """Example of how to test a sent mail"""
        self.sendEmail()
        messages = self.mail_stub.get_sent_messages(to='trigger@ifttt.com')
        self.assertEqual(1, len(messages))
        self.assertEqual('trigger@ifttt.com', messages[0].to)

    def test_taskqueue(self):
        print dir(self.testbed)
        #print "enabled stubs"
        #print self.testbed._enabled_stubs
        #print "service "
        #print dir(self.task_stub)
        print "colas"
        print self.task_stub.GetQueues()
        #print "numail"
        #print dir(numail.NewEmailHandler)
        tarea = numail.NewEmailHandler()
        print "jandler"
        print dir (repr(tarea.request))
        #tarea.request["keyEpisode"] = "asdfb"
        tarea.post()
        print "colas de tareas"
        print self.task_stub.GetQueues()
        
        
        
        # always fail to see the debug while i write this
        self.assertEqual("1", "2")

    def test_compose_email_good(self):
        """prueba el compositor de emails con una lista buena de varios prov.""" 
        pass

    def test_compose_email_somebad(self):
        """test compose_email with a list with a few of empty elements"""
        pass

    def test_compose_email2_good(self):
        """test compose_email2 with a list of good links to variuos prov."""
        pass

    def testMailSent2(self):
        mail.send_mail(to='wakaru44@gmail.com',
                          subject='This is a test',
                          sender='bob@example.com',
                          body='This is a test e-mail')
        messages = self.mail_stub.get_sent_messages(to='wakaru44@gmail.com')
        self.assertEqual(1, len(messages))
        self.assertEqual('wakaru44@gmail.com', messages[0].to)
        print messages[0].body


##def test_email(self):
#def test_email(self):
#    body = Message()
#    body.add_header('to', 'test-unknown@other-app.com')
#    body.add_header('from', 'test@app.com')
#    #body.add_header('Content-Type', 'multipart/alternative',
#    #                boundary=self.boundary)
#    text = Message()
#    text['content-type'] = 'text/plain'
#    text.set_payload('I am I! Don Quixote!  The man of La Mancha!')
#    body.attach(text)
#    print body
#
#    #post(payload=body.as_string())
# 
# 
# def createPayloadForEmail(bodyTxt):
#     body = Message()
#     body.add_header('to', 'agregar@capitulizer.appspotmail.com')
#     body.add_header('from', 'manolo@nomail.com')
#     body.add_header('Content-Type', 'multipart/alternative',
#                     boundary=self.boundary)
#     text = Message()
#     text['content-type'] = 'text/plain'
#     text.set_payload(bodyTxt)
#     body.attach(text)
#     return body.as_string()
#unittest.main()
