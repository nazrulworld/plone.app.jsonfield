# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from zope.configuration import xmlconfig


TEST_ZCML = """\
<configure
    xmlns="http://namespaces.zope.org/zope">
</configure>
"""


class PloneAppJSONFieldLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configuration_context):  # noqa: N802
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)

        import z3c.form
        self.loadZCML(package=z3c.form)

        import plone.app.z3cform
        self.loadZCML(package=plone.app.z3cform)

        import plone.app.jsonfield
        self.loadZCML(package=plone.app.jsonfield)
        # Load Custom
        xmlconfig.string(TEST_ZCML, context=configuration_context)

    def setUpPloneSite(self, portal):  # noqa: N802

        setRoles(portal, TEST_USER_ID, ['Manager'])

        applyProfile(portal, 'plone.restapi:default')

        applyProfile(portal, 'plone.app.jsonfield:default')

        # Apply Test profile
        applyProfile(portal, 'plone.app.jsonfield:testing')


PLONE_APP_JSON_FIELD_FIXTURE = PloneAppJSONFieldLayer()


PLONE_APP_JSON_FIELD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_JSON_FIELD_FIXTURE,),
    name='PloneAppJSONFieldLayer:IntegrationTesting'
)


PLONE_APP_JSON_FIELD_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_JSON_FIELD_FIXTURE, z2.ZSERVER_FIXTURE),
    name='PloneAppJSONFieldLayer:FunctionalTesting'
)


PLONE_APP_JSON_FIELD_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_APP_JSON_FIELD_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PloneAppJSONFieldLayer:AcceptanceTesting'
)
