# (C) Datadog, Inc. 2020
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.stubs import aggregator

EXPECTED_AUDIT_METRICS = {
    'gatekeeper.audit.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.audit.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.audit.last_run_time': aggregator.GAUGE,
    'gatekeeper.constraint_template_ingestion.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.violations': aggregator.GAUGE,
    'gatekeeper.constraints': aggregator.GAUGE,
    'gatekeeper.constraint_templates': aggregator.GAUGE,
}

EXPECTED_CONTROLLER_METRICS = {
    'gatekeeper.request.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.request.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.duration.seconds.sum': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraint_template_ingestion.duration.seconds.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.constraints': aggregator.GAUGE,
    'gatekeeper.constraint_templates': aggregator.GAUGE,
    'gatekeeper.constraint_template_ingestion.count': aggregator.MONOTONIC_COUNT,
    'gatekeeper.request.count': aggregator.MONOTONIC_COUNT,
}


EXPECTED_CHECKS = {
    'gatekeeper.health',
    'gatekeeper.prometheus.health',
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/metrics',
    'gatekeeper_health_endpoint': 'http://fake.tld',
}
