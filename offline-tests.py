import sys
import random
import unittest

# first make sure eximunit is on the module search path
# You may want to modify $PYTHONPATH instead
sys.path.append('/path/to/eximunit/src')

# now import and extend from this class
from eximunit import EximTestCase

class InternalTestCase(EximTestCase):
    def setUp(self):
        super(InternalTestCase, self).setUp()
        self.setDefaultFromIP('10.0.0.1')
        self.from_address = 'valhallasw@arctus.nl'

class ExternalTestCase(EximTestCase):
    def setUp(self):
        super(ExternalTestCase, self).setUp()
        self.setDefaultFromIP('8.8.8.8')
        self.from_address = 'valhallasw@arctus.nl'

class ToToolsMailTests(object):
    """ This is a set of tests that should succeed both from internal
        and external connections
    """
    def testMailToValhallasw(self):
        session = self.newSession()
        session.mailFrom(self.from_address)
        session.rcptTo('valhallasw@tools.wmflabs.org')

    def testMailToRoot(self):
        session = self.newSession()
        session.mailFrom(self.from_address)
        session.rcptTo('root@tools.wmflabs.org')

    def testMailToAdmin(self):
        session = self.newSession()
        session.mailFrom(self.from_address)
        session.rcptTo('tools.admin@tools.wmflabs.org')

class ToToolsMailTestsInternal(InternalTestCase, ToToolsMailTests):
    pass

class ToToolsMailTestsExternal(ExternalTestCase, ToToolsMailTests):
    pass

class ToExternalMailTestInternal(InternalTestCase):
    def testMailToValhallaswAtArctus(self):
        session = self.newSession()
        session.mailFrom(self.from_address)
        session.rcptTo('valhallasw@arctus.nl')

class ToExternalMailTestExternal(ExternalTestCase):
    def testMailToValhallaswAtArctus(self):
        session = self.newSession()
        session.mailFrom(self.from_address)
        session.assertRcptToRejected('valhallasw@arctus.nl', 'relay not permitted')

class RoutingTestCase(EximTestCase):
    def testMailToValhallasw(self):
        self.assertRoutesTo('valhallasw', 'valhallasw@arctus.nl')
        self.assertRoutesTo('valhallasw@tools.wmflabs.org', 'valhallasw@arctus.nl')

    def testMailToRoot(self):
        self.assertRoutesTo('root', 'valhallasw@arctus.nl')
        self.assertRoutesTo('root', 'yuvipanda@gmail.com')
        self.assertRoutesTo('root@tools.wmflabs.org', 'valhallasw@arctus.nl')
        self.assertRouteUndeliverable('root@tools-bastion-01.wmflabs.org')

    def testMailToAdmin(self):
        self.assertRoutesTo('tools.admin', 'valhallasw@arctus.nl')
        self.assertRoutesTo('tools.admin', 'yuvipanda@gmail.com')
        self.assertRoutesTo('tools.admin@tools.wmflabs.org', 'valhallasw@arctus.nl')
        self.assertRouteUndeliverable('tools.admin@tools-bastion-01.tools.wmflabs.org')

    def testMailToNonexistentUser(self):
        self.assertRouteUndeliverable('doesnotexistreally')
        self.assertRouteUndeliverable('doesnotexistreally@tools.wmflabs.org')

    @unittest.expectedFailure
    def testMailToNonToolsUser(self):
        self.assertRouteUndeliverable('ben')

 
if __name__ == '__main__':
    unittest.main()
