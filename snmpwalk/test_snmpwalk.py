# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import os
import copy
import time

# 3p
from nose.plugins.attrib import attr

# project
from checks import AgentCheck
from tests.checks.common import AgentCheckTest


RESULTS_TIMEOUT = 10

@attr(requires='snmpwalk')
class TestSnmpwalk(AgentCheckTest):
    """Basic Test for snmpwrap integration."""
    CHECK_NAME = 'snmpwalk'
    FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'ci')

    CHECK_TAGS = ['snmp_device:localhost:11111']
    INSTANCE_CONF = {
        'ip_address': "localhost",
        'port': 11111,
        'community_string': "public",
    }
    CONFIG = {
        'init_config': {},
        'instances' : [INSTANCE_CONF]
    }

    TABULAR_OBJECTS = [{
        'MIB': "IF-MIB",
        'table': "ifTable",
        'symbols': ["ifInOctets", "ifOutOctets"],
        'metric_tags': [
            {
                'tag': "interface",
                'column': "ifDescr"
            }, {
                'tag': "dumbindex",
                'index': 1
            }
        ]
    }]

    def tearDown(self):
        if self.check:
            self.check.stop()

    @classmethod
    def generate_instance_config(cls, metrics):
        instance_config = copy.copy(cls.INSTANCE_CONF)
        instance_config['metrics'] = metrics
        instance_config['name'] = "localhost"
        return instance_config

    def wait_for_async(self, method, attribute, count):
        """
        Loop on `self.check.method` until `self.check.attribute >= count`.

        Raise after
        """
        i = 0
        while i < RESULTS_TIMEOUT:
            self.check._process_results()
            if len(getattr(self.check, attribute)) >= count:
                return getattr(self.check, method)()
            time.sleep(1)
            i += 1
        raise Exception("Didn't get the right count for {attribute} in time, {total}/{expected} in {seconds}s: {attr}"
                        .format(attribute=attribute, total=len(getattr(self.check, attribute)), expected=count, seconds=i,
                                attr=getattr(self.check, attribute)))


    def test_check(self):
        """
        Testing Snmpwrap check.
        """
        config = {
            'instances': [self.generate_instance_config(self.TABULAR_OBJECTS)]
        }
        self.run_check_n(config, repeat=3, sleep=2)
        self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1)

        # Test metrics
        for symbol in self.TABULAR_OBJECTS[0]['symbols']:
            metric_name = '{}.{}'.format(self.CHECK_NAME, symbol)
            self.assertMetric(metric_name, at_least=1)
            self.assertMetricTag(metric_name, self.CHECK_TAGS[0], at_least=1)

            for mtag in self.TABULAR_OBJECTS[0]['metric_tags']:
                tag = mtag['tag']
                if tag is 'dumbindex':  # unsupported
                    self.assertMetricTagPrefix(metric_name, tag, count=0)
                else:
                    self.assertMetricTagPrefix(metric_name, tag, at_least=1)

        # Test service check
        svcchk_name = '{}.can_check'.format(self.CHECK_NAME)
        self.assertServiceCheck(svcchk_name, status=AgentCheck.OK,
                                tags=[':'.join(self.CHECK_TAGS[0].split(':')[:-1])], count=1)

        self.coverage_report()

    def test_unavailable_binary(self):
        """
        Should raise exception if binary is unavailable.
        """
        config = {
            'init_config': {'binary': '/path/to/nonexistant/snmpwalk'},
            'instances': [self.generate_instance_config(self.TABULAR_OBJECTS)]
        }

        self.run_check(config)
        self.assertRaises(
            Exception,
            lambda: self.wait_for_async('get_service_checks', 'service_checks', 1)
        )
