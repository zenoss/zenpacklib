#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2018, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""Keyword Tests
This test will use lint to load in example yaml with keywords used
"""
from ZenPacks.zenoss.ZenPackLib.tests import ZPLBaseTestCase

RESERVED_YAML = """name: ZenPacks.zenoss.TestLogging
classes:
    ExampleDevice:
        base: [zenpacklib.Device]
        label: Example
        properties:
            uuid:
                label: UUID
            yield:
                label: Yield
            name:
                label: Name
            memory:
                label: Memory
    lambda:
        base: [zenpacklib.Component]
        label: Lambda
        properties:
            prop1:
                label: yield
            uuid:
                label: UUID
zProperties:
    zCommandUsername:
        default: ''
device_classes:
    /Server/SSH:
        templates:
            lambda:
                description: Poorly named template

                datasources:
                    health:
                        type: COMMAND
                        parser: Nagios
                        commandTemplate: "echo OK|percent=100"

                        datapoints:
                          percent:
                            rrdtype: GAUGE
                            rrdmin: 0
                            rrdmax: 100
                            breadCrumbs: 0
"""

NO_RESERVED_YAML = """name: ZenPacks.zenoss.TestLogging

classes:
    ExampleDevice:
        base: [zenpacklib.Device]
        label: Example
        properties:
            prop1:
                label: Example Property
    ProperComponent:
        base: [zenpacklib.Component]
        label: Properly Named Component
        properties:
            prop1:
                label: Property One
zProperties:
    zCommandUsername:
        default: ''
device_classes:
    /Server/SSH:
        templates:
            ProperComponentHealth:
                description: Properly named template

                datasources:
                    health:
                        type: COMMAND
                        parser: Nagios
                        commandTemplate: "echo OK|percent=100"

                        datapoints:
                          percent:
                            rrdtype: GAUGE
                            rrdmin: 0
                            rrdmax: 100
"""

EXPECTED = """[WARNING] <string>:7:13: ["Found reserved Zenoss keyword 'uuid' from DeviceInfo, ComponentInfo"]
[ERROR] <string>:9:13: ["Found reserved keyword 'yield' while processing ClassPropertySpec"]
[WARNING] <string>:11:13: ["Found reserved Zenoss keyword 'name' from Device, DeviceComponent, DeviceInfo, ComponentInfo"]
[ERROR] <string>:15:5: ["Found reserved keyword 'lambda' while processing ClassSpec"]
[WARNING] <string>:21:13: ["Found reserved Zenoss keyword 'uuid' from DeviceInfo, ComponentInfo"]
[ERROR] <string>:29:13: ["Found reserved keyword 'lambda' while processing RRDTemplateSpec"]
"""


class TestLoggingKeywords(ZPLBaseTestCase):
    disableLogging = False

    def test_reserved_keywords(self):
        actual = self.capture.test_yaml(RESERVED_YAML)
        self.assertEquals(actual, EXPECTED, 'Reserved keywords testing failed:\n  {}'.format(actual))

    def test_no_reserved_keywords(self):
        actual = self.capture.test_yaml(NO_RESERVED_YAML)
        self.assertEquals(actual, '', 'Non-reserved keywords testing failed:\n  {}'.format(actual))


def test_suite():
    """Return test suite for this module."""
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLoggingKeywords))
    return suite


if __name__ == "__main__":
    from zope.testrunner.runner import Runner
    runner = Runner(found_suites=[test_suite()])
    runner.run()
