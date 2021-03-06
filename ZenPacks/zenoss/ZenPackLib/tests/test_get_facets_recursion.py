#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2018, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""
    ToMany-ToMany (M:M) non-containing relationships cause infinite recursion in get_facets
    ZEN-23840
"""
from ZenPacks.zenoss.ZenPackLib.tests import ZPLBaseTestCase

YAML_DOC = """
name: ZenPacks.zenoss.GetFacets

class_relationships:
  - UnivaGrid 1:MC UGEFilesystem
  - UnivaGrid 1:MC ECCNetwork
  - UnivaGrid 1:MC UGEServer
  - UnivaGrid 1:MC UGEQueue
  - UnivaGrid 1:MC HPC
  - HPC(hpctapelibraries) 1:MC HPCTapeLibrary
  - HPC 1:MC HPCFilesystem
  - HPC 1:MC HPCCluster
  - HPCCluster 1:MC HPCNode
  - HPCCluster 1:MC HPCNetwork
  - HPCNetwork(hpcswitches) 1:MC HPCSwitch
  - UGEQueue M:M HPCNode

classes:
  UnivaGrid:
    base: [zenpacklib.Device]
    label: Univa Grid Engine
    properties:
      version:
        type: string
        label: Version
        order: 10

  UGEQueue:
    base: [zenpacklib.Component]
    label: UGE Queue
    order: 45
    properties:
      status:
        type: string
        label: Status
        order: 10

  UGEFilesystem:
    base: [zenpacklib.Component]
    label: UGE Filesystem
    order: 30

  UGEServer:
    base: [zenpacklib.Component]
    label: UGE Server
    order: 40

  ECCNetwork:
    base: [zenpacklib.Component]
    label: ECC Network
    order: 40

  HPC:
    base: [zenpacklib.Component]
    label: HPC Infrastructure
    order: 50

  HPCCluster:
    base: [zenpacklib.Component]
    label: HPC Cluster
    order: 55

  HPCSwitch:
    base: [zenpacklib.Component]
    label: HPC Switch
    plural_label: HPC Switches
    order: 65

  HPCNode:
    base: [zenpacklib.Component]
    label: HPC Node
    order: 70
    properties:
      status:
        type: string
        label: Version
        order: 10
    extra_paths:
    - ['ugequeues', 'hpcnodes']

  HPCFilesystem:
    base: [zenpacklib.Component]
    label: HPC Filesystem
    order: 52

  HPCNetwork:
    base: [zenpacklib.Component]
    label: HPC Network
    order: 60

  HPCTapeLibrary:
    base: [zenpacklib.Component]
    label: HPC TapeLibrary
    plural_label: HPC TapeLibraries
    order: 53

device_classes:
  /UGE:
    zProperties:
      zPythonClass: ZenPacks.zenoss.PS.SA.UGE.UnivaGrid
      zPingMonitorIgnore: true
      zSnmpMonitorIgnore: true
"""


class TestGetFacets(ZPLBaseTestCase):
    """Test fix for ZEN-23840

       ToMany-ToMany (M:M) non-containing relationships cause infinite recursion in get_facets
    """

    yaml_doc = YAML_DOC
    build = True

    def test_get_facets_recursion(self):
        config = self.configs.get('ZenPacks.zenoss.GetFacets')
        objects = config.get('objects').class_objects
        expected = 2
        for name, data in objects.items():
            ob = data.get('ob')
            if ob.meta_type == 'HPCNode':
                facets = []
                for f in ob.get_facets():
                    facets.append(f)
                actual = len(facets)
                self.assertEquals(expected, actual, 'get_facets expected {}, got {} objects'.format(expected, actual))


def test_suite():
    """Return test suite for this module."""
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGetFacets))
    return suite


if __name__ == "__main__":
    from zope.testrunner.runner import Runner
    runner = Runner(found_suites=[test_suite()])
    runner.run()
