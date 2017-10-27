# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from collections import defaultdict
from nose.plugins.attrib import attr

# 3p
import responses

# project
from checks import AgentCheck
from tests.checks.common import AgentCheckTest


instance = {
    'server': 'localhost:9005',
    'environment': 'test'
}

TEST_STORM_CLUSTER_SUMMARY = {
    "executorsTotal": 33,
    "stormVersion": "1.0.3",
    "slotsTotal": 10,
    "slotsFree": 4,
    "user": None,
    "topologies": 1,
    "supervisors": 1,
    "central-log-url": None,
    "bugtracker-url": None,
    "tasksTotal": 33,
    "slotsUsed": 6
}

TEST_STORM_NIMBUSES_SUMMARY = {
    "nimbuses": [
        {
            "nimbusUptimeSeconds": "Not applicable",
            "nimbusUpTime": "Not applicable",
            "version": "Not applicable",
            "status": "Offline",
            "nimbusLogLink": "http://nimbus01.example.com:9006/daemonlog?file=nimbus.log",
            "port": "6627",
            "host": "nimbus01.example.com"
        },
        {
            "nimbusUpTimeSeconds": 25842,
            "nimbusUpTime": "7h 10m 42s",
            "version": "1.0.3",
            "status": "Leader",
            "nimbusLogLink": "http://1.2.3.4:9006/daemonlog?file=nimbus.log",
            "port": 6627,
            "host": "1.2.3.4"
        }
    ]
}

TEST_STORM_SUPERVISOR_SUMMARY = {
    "logviewerPort": 9006,
    "schedulerDisplayResource": False,
    "supervisors": [
        {
            "uptimeSeconds": 31559,
            "slotsTotal": 10,
            "version": "1.0.3",
            "slotsUsed": 6,
            "totalMem": 3072,
            "host": "1.2.3.4",
            "id": "11111111-1111-1111-1111-111111111111",
            "uptime": "8h 45m 59s",
            "totalCpu": 900,
            "usedCpu": 0,
            "logLink": "http://1.2.3.4:9006/daemonlog?file=supervisor.log",
            "usedMem": 4992
        }
    ]
}

TEST_STORM_TOPOLOGY_SUMMARY = {
    "schedulerDisplayResource": False,
    "topologies": [
        {
            "requestedTotalMem": 0,
            "assignedMemOffHeap": 0,
            "assignedCpu": 0,
            "uptimeSeconds": 1525505,
            "schedulerInfo": None,
            "uptime": "17d 15h 45m 5s",
            "id": "my_topology-1-1489183263",
            "assignedMemOnHeap": 4992,
            "encodedId": "my_topology-1-1489183263",
            "requestedMemOnHeap": 0,
            "owner": "storm",
            "assignedTotalMem": 4992,
            "name": "my_topology",
            "workersTotal": 6,
            "status": "ACTIVE",
            "requestedMemOffHeap": 0,
            "tasksTotal": 33,
            "requestedCpu": 0,
            "replicationCount": 1,
            "executorsTotal": 33
        }
    ]
}

TEST_STORM_TOPOLOGY_RESP = {
    "assignedMemOffHeap": 0,
    "topologyStats": [
        {
            "failed": None,
            "acked": 104673,
            "completeLatency": "285.950",
            "transferred": 307606,
            "emitted": 307606,
            "window": ":all-time",
            "windowPretty": "All time"
        }
    ],
    "assignedCpu": 0,
    "uptimeSeconds": 1525788,
    "executorsTotal": 33,
    "bolts": [
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "201.474",
            "executors": 3,
            "boltId": "Bolt1",
            "failed": 0,
            "errorHost": "",
            "tasks": 3,
            "errorTime": None,
            "emitted": 101309,
            "executeLatency": "0.001",
            "transferred": 101309,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 212282,
            "encodedBoltId": "Bolt1",
            "lastError": "",
            "executed": 106311
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "0.010",
            "executors": 2,
            "boltId": "Bolt2",
            "failed": 0,
            "errorHost": "",
            "tasks": 2,
            "errorTime": None,
            "emitted": 0,
            "executeLatency": "0.015",
            "transferred": 0,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 3153,
            "encodedBoltId": "Bolt2",
            "lastError": "",
            "executed": 3153
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "0.003",
            "executors": 3,
            "boltId": "Bolt3",
            "failed": 0,
            "errorHost": "",
            "tasks": 3,
            "errorTime": None,
            "emitted": 0,
            "executeLatency": "0.009",
            "transferred": 0,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 4704,
            "encodedBoltId": "Bolt3",
            "lastError": "",
            "executed": 4704
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "291.756",
            "executors": 4,
            "boltId": "Bolt4",
            "failed": 0,
            "errorHost": "",
            "tasks": 4,
            "errorTime": None,
            "emitted": 101607,
            "executeLatency": "0.001",
            "transferred": 101607,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 218808,
            "encodedBoltId": "Bolt4",
            "lastError": "",
            "executed": 110946
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "1014.634",
            "executors": 2,
            "boltId": "Bolt5",
            "failed": 0,
            "errorHost": "",
            "tasks": 2,
            "errorTime": None,
            "emitted": 17,
            "executeLatency": "0.001",
            "transferred": 17,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 208890,
            "encodedBoltId": "Bolt5",
            "lastError": "",
            "executed": 104445
        },
        {
            "errorWorkerLogLink": "",
            "capacity": "0.000",
            "processLatency": "0.005",
            "executors": 3,
            "boltId": "Bolt6",
            "failed": 0,
            "errorHost": "",
            "tasks": 3,
            "errorTime": None,
            "emitted": 0,
            "executeLatency": "0.010",
            "transferred": 0,
            "errorPort": "",
            "errorLapsedSecs": None,
            "acked": 4705,
            "encodedBoltId": "Bolt6",
            "lastError": "",
            "executed": 4705
        }
    ],
    "schedulerDisplayResource": False,
    "replicationCount": 1,
    "requestedCpu": 0,
    "tasksTotal": 33,
    "visualizationTable": [],
    "debug": False,
    "requestedMemOffHeap": 0,
    "spouts": [
        {
            "errorWorkerLogLink": "http://1.2.3.4:9006/log?file=my_topology-1-1489183263%2F6707%2Fworker.log",
            "lastError": "com.rabbitmq.client.ShutdownSignalException: clean connection shutdown; protocol method: #method<connection.close>(reply-code=200, reply-text=OK, class-id=0, method-id=0)\n\tat com.rabbitmq.client.impl.",
            "acked": 104673,
            "errorLapsedSecs": 38737,
            "errorPort": 6707,
            "transferred": 104673,
            "encodedSpoutId": "source",
            "emitted": 104673,
            "spoutId": "source",
            "errorTime": 1490670314,
            "tasks": 8,
            "errorHost": "1.2.3.4",
            "failed": 0,
            "completeLatency": "285.950",
            "executors": 8
        }
    ],
    "status": "ACTIVE",
    "user": None,
    "msgTimeout": 300,
    "windowHint": "All time",
    "encodedId": "my_topology-1-1489183263",
    "requestedMemOnHeap": 0,
    "owner": "storm",
    "window": ":all-time",
    "assignedTotalMem": 4992,
    "samplingPct": 10,
    "assignedMemOnHeap": 4992,
    "id": "my_topology-1-1489183263",
    "configuration": {
        "drpc.request.timeout.secs": 600,
        "storm.auth.simple-acl.users.commands": [],
        "nimbus.thrift.max_buffer_size": 1048576,
        "logviewer.appender.name": "A1",
        "storm.messaging.netty.transfer.batch.size": 262144,
        "storm.exhibitor.poll.uripath": "/exhibitor/v1/cluster/list",
        "topology.name": "my_topology",
        "storm.id": "my_topology-1-1489183263",
        "topology.kryo.decorators": [],
        "ui.port": 9005,
        "java.library.path": "/usr/local/lib:/opt/local/lib:/usr/lib",
        "drpc.invocations.threads": 64,
        "storm.auth.simple-acl.users": [],
        "topology.trident.batch.emit.interval.millis": 500,
        "storm.nimbus.retry.intervalceiling.millis": 60000,
        "topology.disruptor.wait.timeout.millis": 1000,
        "topology.min.replication.count": 1,
        "ui.header.buffer.bytes": 4096,
        "ui.filter": None,
        "backpressure.disruptor.high.watermark": 0.9,
        "ui.http.x-frame-options": "DENY",
        "topology.worker.max.heap.size.mb": 1024,
        "supervisor.childopts": "-Xmx256m",
        "client.blobstore.class": "org.apache.storm.blobstore.NimbusBlobStore",
        "storm.blobstore.acl.validation.enabled": False,
        "storm.zookeeper.auth.password": None,
        "supervisor.worker.timeout.secs": 30,
        "transactional.zookeeper.servers": None,
        "ui.users": None,
        "pacemaker.childopts": "-Xmx1024m",
        "logviewer.max.sum.worker.logs.size.mb": 4096,
        "worker.heap.memory.mb": 768,
        "storm.blobstore.replication.factor": 3,
        "nimbus.cleanup.inbox.freq.secs": 600,
        "nimbus.queue.size": 100000,
        "nimbus.seeds": [
            "nimbus01.example.com"
        ],
        "nimbus.topology.validator": "org.apache.storm.nimbus.DefaultTopologyValidator",
        "worker.gc.childopts": "",
        "topology.kryo.register": None,
        "topology.kryo.factory": "org.apache.storm.serialization.DefaultKryoFactory",
        "topology.component.resources.onheap.memory.mb": 256,
        "storm.messaging.netty.authentication": False,
        "topology.disable.loadaware.messaging": False,
        "storm.messaging.transport": "org.apache.storm.messaging.netty.Context",
        "topology.error.throttle.interval.secs": 10,
        "drpc.http.port": 3774,
        "topology.component.resources.offheap.memory.mb": 0,
        "storm.messaging.netty.max_wait_ms": 1000,
        "pacemaker.port": 6699,
        "task.heartbeat.frequency.secs": 3,
        "storm.exhibitor.port": 8080,
        "topology.metrics.consumer.register": [
            {
                "parallelism.hint": 2,
                "class": "com.accelerate_experience.storm.metrics.statsd.StatsdMetricConsumer",
                "argument": {
                    "metrics.statsd.prefix": "storm.metrics.",
                    "metrics.statsd.port": 8125,
                    "metrics.statsd.host": "127.0.0.1"
                }
            }
        ],
        "task.refresh.poll.secs": 10,
        "supervisor.blobstore.download.max_retries": 3,
        "storm.workers.artifacts.dir": "workers-artifacts",
        "drpc.https.port": -1,
        "topology.tick.tuple.freq.secs": 4,
        "topology.submitter.user": "storm",
        "storm.zookeeper.root": "/storm",
        "ui.http.creds.plugin": "org.apache.storm.security.auth.DefaultHttpCredentialsPlugin",
        "storm.log4j2.conf.dir": "log4j2",
        "worker.heartbeat.frequency.secs": 1,
        "storm.cluster.state.store": "org.apache.storm.cluster_state.zookeeper_state_factory",
        "storm.messaging.netty.buffer_size": 5242880,
        "storm.local.mode.zmq": False,
        "nimbus.task.launch.secs": 120,
        "topology.users": [],
        "backpressure.disruptor.low.watermark": 0.4,
        "topology.executor.receive.buffer.size": 1024,
        "worker.profiler.childopts": "-XX:+UnlockCommercialFeatures -XX:+FlightRecorder",
        "nimbus.file.copy.expiration.secs": 600,
        "drpc.authorizer.acl.strict": False,
        "topology.worker.shared.thread.pool.size": 4,
        "storm.health.check.dir": "/var/lib/storm/healthchecks",
        "topology.transfer.buffer.size": 1024,
        "supervisor.slots.ports": [
            6700
        ],
        "topology.state.checkpoint.interval.ms": 1000,
        "topology.worker.receiver.thread.count": 1,
        "drpc.https.keystore.type": "JKS",
        "task.credentials.poll.secs": 30,
        "pacemaker.thread.timeout": 10,
        "drpc.max_buffer_size": 1048576,
        "transactional.zookeeper.port": None,
        "dev.zookeeper.path": "/tmp/dev-storm-zookeeper",
        "nimbus.inbox.jar.expiration.secs": 3600,
        "storm.nimbus.retry.interval.millis": 2000,
        "topology.submitter.principal": "",
        "ui.host": "0.0.0.0",
        "topology.spout.wait.strategy": "org.apache.storm.spout.SleepSpoutWaitStrategy",
        "topology.worker.logwriter.childopts": "-Xmx64m",
        "storm.daemon.metrics.reporter.plugins": [
            "org.apache.storm.daemon.metrics.reporters.JmxPreparableReporter"
        ],
        "pacemaker.auth.method": "NONE",
        "resource.aware.scheduler.priority.strategy": "org.apache.storm.scheduler.resource.strategies.priority.DefaultSchedulingPriorityStrategy",
        "topology.executor.send.buffer.size": 1024,
        "topology.scheduler.strategy": "org.apache.storm.scheduler.resource.strategies.scheduling.DefaultResourceAwareStrategy",
        "logviewer.port": 9006,
        "nimbus.code.sync.freq.secs": 120,
        "drpc.https.keystore.password": "",
        "topology.shellbolt.max.pending": 100,
        "storm.blobstore.inputstream.buffer.size.bytes": 65536,
        "supervisor.blobstore.class": "org.apache.storm.blobstore.NimbusBlobStore",
        "topology.backpressure.enable": False,
        "drpc.queue.size": 128,
        "task.backpressure.poll.secs": 30,
        "supervisor.blobstore.download.thread.count": 5,
        "drpc.worker.threads": 64,
        "supervisor.cpu.capacity": 300,
        "topology.enable.message.timeouts": True,
        "supervisor.heartbeat.frequency.secs": 5,
        "storm.zookeeper.port": 2181,
        "worker.log.level.reset.poll.secs": 30,
        "storm.messaging.netty.min_wait_ms": 100,
        "topology.stats.sample.rate": 1,
        "supervisor.enable": True,
        "zmq.linger.millis": 5000,
        "topology.max.replication.wait.time.sec": 60,
        "scheduler.display.resource": False,
        "topology.sleep.spout.wait.strategy.time.ms": 1,
        "logviewer.cleanup.interval.secsInterval": 86400,
        "transactional.zookeeper.root": "/transactional",
        "storm.group.mapping.service": "org.apache.storm.security.auth.ShellBasedGroupsMapping",
        "zmq.threads": 1,
        "topology.priority": 29,
        "topology.builtin.metrics.bucket.size.secs": 60,
        "nimbus.childopts": "-Xmx2048m",
        "ui.filter.params": None,
        "storm.cluster.mode": "distributed",
        "storm.messaging.netty.client_worker_threads": 1,
        "logviewer.max.per.worker.logs.size.mb": 2048,
        "supervisor.run.worker.as.user": False,
        "topology.max.task.parallelism": None,
        "drpc.invocations.port": 3773,
        "supervisor.localizer.cache.target.size.mb": 10240,
        "topology.multilang.serializer": "org.apache.storm.multilang.JsonSerializer",
        "storm.messaging.netty.server_worker_threads": 1,
        "nimbus.blobstore.class": "org.apache.storm.blobstore.LocalFsBlobStore",
        "resource.aware.scheduler.eviction.strategy": "org.apache.storm.scheduler.resource.strategies.eviction.DefaultEvictionStrategy",
        "topology.max.error.report.per.interval": 5,
        "storm.thrift.transport": "org.apache.storm.security.auth.SimpleTransportPlugin",
        "zmq.hwm": 0,
        "storm.group.mapping.service.params": None,
        "worker.profiler.enabled": False,
        "storm.principal.tolocal": "org.apache.storm.security.auth.DefaultPrincipalToLocal",
        "supervisor.worker.shutdown.sleep.secs": 1,
        "pacemaker.host": "localhost",
        "storm.zookeeper.retry.times": 5,
        "ui.actions.enabled": True,
        "topology.acker.executors": None,
        "topology.fall.back.on.java.serialization": True,
        "topology.eventlogger.executors": 0,
        "supervisor.localizer.cleanup.interval.ms": 600000,
        "storm.zookeeper.servers": [
            "zookeeper01.example.com"
        ],
        "nimbus.thrift.threads": 64,
        "logviewer.cleanup.age.mins": 10080,
        "topology.worker.childopts": None,
        "topology.classpath": None,
        "supervisor.monitor.frequency.secs": 3,
        "nimbus.credential.renewers.freq.secs": 600,
        "topology.skip.missing.kryo.registrations": False,
        "drpc.authorizer.acl.filename": "drpc-auth-acl.yaml",
        "pacemaker.kerberos.users": [],
        "storm.group.mapping.service.cache.duration.secs": 120,
        "topology.testing.always.try.serialize": False,
        "nimbus.monitor.freq.secs": 10,
        "worker.childops": "-Xmx2048m -XX:+PrintGCDetails -Xloggc:artifacts/gc.log -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=1M -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=artifacts/heapdump",
        "storm.health.check.timeout.ms": 10000,
        "supervisor.supervisors": [],
        "topology.tasks": None,
        "topology.bolts.outgoing.overflow.buffer.enable": False,
        "storm.messaging.netty.socket.backlog": 500,
        "topology.workers": 6,
        "pacemaker.base.threads": 10,
        "storm.local.dir": "/var/lib/storm/data",
        "worker.childopts": "-Xmx%HEAP-MEM%m -XX:+PrintGCDetails -Xloggc:artifacts/gc.log -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=1M -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=artifacts/heapdump",
        "storm.auth.simple-white-list.users": [],
        "topology.disruptor.batch.timeout.millis": 1,
        "topology.message.timeout.secs": 300,
        "topology.state.synchronization.timeout.secs": 60,
        "topology.tuple.serializer": "org.apache.storm.serialization.types.ListDelegateSerializer",
        "supervisor.supervisors.commands": [],
        "nimbus.blobstore.expiration.secs": 600,
        "logviewer.childopts": "-Xmx128m",
        "topology.environment": {
            "mytopology.foo": "bar"
        },
        "topology.debug": False,
        "topology.disruptor.batch.size": 100,
        "storm.messaging.netty.max_retries": 300,
        "ui.childopts": "-Xmx768m",
        "storm.network.topography.plugin": "org.apache.storm.networktopography.DefaultRackDNSToSwitchMapping",
        "storm.zookeeper.session.timeout": 20000,
        "drpc.childopts": "-Xmx768m",
        "drpc.http.creds.plugin": "org.apache.storm.security.auth.DefaultHttpCredentialsPlugin",
        "storm.zookeeper.connection.timeout": 15000,
        "storm.zookeeper.auth.user": None,
        "storm.meta.serialization.delegate": "org.apache.storm.serialization.GzipThriftSerializationDelegate",
        "topology.max.spout.pending": 500,
        "storm.codedistributor.class": "org.apache.storm.codedistributor.LocalFileSystemCodeDistributor",
        "nimbus.supervisor.timeout.secs": 60,
        "nimbus.task.timeout.secs": 30,
        "storm.zookeeper.superACL": None,
        "drpc.port": 3772,
        "pacemaker.max.threads": 50,
        "storm.zookeeper.retry.intervalceiling.millis": 30000,
        "nimbus.thrift.port": 6627,
        "storm.auth.simple-acl.admins": [],
        "topology.component.cpu.pcore.percent": 10,
        "supervisor.memory.capacity.mb": 3072,
        "storm.nimbus.retry.times": 5,
        "supervisor.worker.start.timeout.secs": 120,
        "storm.zookeeper.retry.interval": 1000,
        "logs.users": None,
        "worker.profiler.command": "flight.bash"
    },
    "uptime": "17d 15h 49m 48s",
    "schedulerInfo": None,
    "name": "my_topology",
    "workersTotal": 6
}


TEST_STORM_TOPOLOGY_METRICS_RESP = {
    "window": ":all-time",
    "window-hint": "All time",
    "spouts": [
        {
            "id": "spout",
            "emitted": [
                {"stream_id": "__metrics", "value": 20},
                {"stream_id": "default", "value": 17350280},
                {"stream_id": "__ack_init", "value": 17328160},
                {"stream_id": "__system", "value": 20}
            ],
            "transferred": [
                {"stream_id": "__metrics", "value": 20},
                {"stream_id": "default", "value": 17350280},
                {"stream_id": "__ack_init", "value": 17328160},
                {"stream_id": "__system", "value": 0}
            ],
            "acked": [
                {"stream_id": "default", "value": 17339180}
            ],
            "failed": [],
            "complete_ms_avg": [
                {"stream_id": "default", "value": "920.497"}
            ]
        }
    ],
    "bolts": [
        {
            "id": "count",
            "emitted": [
                {"stream_id": "__metrics", "value": 120},
                {"stream_id": "default", "value": 190748180},
                {"stream_id": "__ack_ack", "value": 190718100},
                {"stream_id": "__system", "value": 20}
            ],
            "transferred": [
                {"stream_id": "__metrics", "value": 120},
                {"stream_id": "default", "value": 0},
                {"stream_id": "__ack_ack", "value": 190718100},
                {"stream_id": "__system", "value": 0}
            ],
            "acked": [
                {"component_id": "split", "stream_id": "default", "value": 190733160}
            ],
            "failed": [],
            "process_ms_avg": [
                {"component_id": "split", "stream_id": "default", "value": "0.004"}
            ],
            "executed": [
                {"component_id": "split", "stream_id": "default", "value": 190733140}
            ],
            "executed_ms_avg": [
                {"component_id": "split", "stream_id": "default", "value": "0.005"}
            ]
        },
        {
            "id": "split",
            "emitted": [
                {"stream_id": "__metrics", "value": 60},
                {"stream_id": "default", "value": 190754740},
                {"stream_id": "__ack_ack", "value": 17317580},
                {"stream_id": "__system", "value": 20}
            ],
            "transferred": [
                {"stream_id": "__metrics", "value": 60},
                {"stream_id": "default", "value": 190754740},
                {"stream_id": "__ack_ack", "value": 17317580},
                {"stream_id": "__system", "value": 0}
            ],
            "acked":[
                {"component_id": "spout", "stream_id": "default", "value": 17339180}
            ],
            "failed": [],
            "process_ms_avg": [
                {"component_id": "spout", "stream_id": "default", "value": "0.051"}
            ],
            "executed": [
                {"component_id": "spout", "stream_id": "default", "value": 17339240}
            ],
            "executed_ms_avg": [
                {"component_id": "spout", "stream_id": "default", "value": "0.052"}
            ]
        }
    ]
}


@attr(requires='storm')
class TestStorm(AgentCheckTest):
    """Basic Test for storm integration."""
    CHECK_NAME = 'storm'
    STORM_CHECK_CONFIG = {'instances': [{'server': 'http://localhost:9005', 'environment': 'test'}]}
    STORM_CHECK_INTEGRATION_CONFIG = {'instances': [{'server': 'http://localhost:9005', 'environment': 'integration'}]}

    def assertHistogramMetric(self, metric_name, value=None, tags=None, count=None, at_least=1, hostname=None,
                              device_name=None):
        for postfix in ['max', 'median', 'avg', '95percentile']:
            self.assertMetric(
                metric_name='{}.{}'.format(metric_name, postfix), value=value, tags=tags, count=count,
                at_least=at_least, hostname=hostname, device_name=device_name
            )
        self.assertMetric(
            metric_name='{}.count'.format(metric_name), value=count, tags=tags, count=count, at_least=at_least,
            hostname=hostname, device_name=device_name
        )

    def assign_self_info_from_check(self):
        self.service_checks = self.check.service_checks
        self.metrics = self.check.aggregator.metrics
        self.events = self.check.events
        self.service_metadata = self.check.svc_metadata
        self.warnings = self.check.warnings

    @attr('config')
    def test_load_from_config(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])
        self.assertEqual('http://localhost:9005', self.check.nimbus_server)
        self.assertEqual('test', self.check.environment_name)
        self.assertListEqual([], self.check.additional_tags)
        self.assertListEqual([], self.check.excluded_topologies)
        print type(self.check.intervals), self.check.intervals
        self.assertListEqual([60], self.check.intervals)

    @attr('helper')
    def test_g(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        module = __import__(self.check.__class__.__module__)
        _g = module._g
        _long = module._long
        _float = module._float

        test_cases = ( # ((func, expected, default, input), ...)
            # Long tests
            (_long, None, None, None),
            (_long, None, None, ''),
            (_long, 0, None, 'test'),
            (_long, 0, 0, ''),
            (_long, 0, 0, None),
            (_long, 0, 0, 'test'),
            (_long, 0, 0, ''),
            (_long, 0, 0, 0),
            (_long, 0, 0, '0'),
            (_long, 1, 0, 1),
            (_long, 1, 0, '1'),

            # Float tests
            (_float, None, None, None),
            (_float, None, None, ''),
            (_float, 0.0, None, 'test'),
            (_float, 0.0, 0.0, ''),
            (_float, 0.0, 0, None),
            (_float, 0.0, 0, 'test'),
            (_float, 0.0, 0, ''),
            (_float, 0.0, 0, 0.0),
            (_float, 0.0, 0, '0'),
            (_float, 0.0, 0, '0.0'),
            (_float, 1.0, 0, '1'),
            (_float, 1.1, 0, 1.1),
            (_float, 1.1, 0, '1.1'),

            # Other tests
            (None, None, None, None),
            (None, 'test', None, 'test'),
            (None, None, None, ''),
        )

        for test_case in test_cases:
            func, expected, default, input_value = test_case
            if input_value is None:
                input_dict = {}
            else:
                input_dict = {'input': input_value}
            result = _g(input_dict, default, func, 'input')
            if func == _float:
                self.assertAlmostEqual(expected, result, 0.01,
                                       "Expected value to match for test case: {} but got {}".format(test_case, result))
            else:
                self.assertEqual(expected, result,
                                 "Expected value to match for test case: {} but got {}".format(test_case, result))

    @attr('helper')
    def test_try_float(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})

        _float = __import__(self.check.__class__.__module__)._float
        self.assertEquals(0.1, _float("0.1"))
        self.assertEquals(0.0, _float("garbage"))

    @attr('helper')
    def test_try_long(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        _long = __import__(self.check.__class__.__module__)._long
        self.assertEquals(1, _long("1"))
        self.assertEquals(0.0, _long("garbage"))

    @attr('helper')
    def test_try_bool(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        _bool = __import__(self.check.__class__.__module__)._bool
        for i, case in enumerate(['1', 1, 'true', 'True', True]):
            self.assertTrue(_bool(case), "Expected Truthy conversion for case[{}] = {}".format(i, case))
        for i, case in enumerate(['0', 0, 'false', 'False', False, None]):
            self.assertFalse(_bool(case), "Expected False conversion for case[{}] = {}".format(i, case))

    @attr('request', 'cluster')
    @responses.activate
    def test_get_storm_cluster_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/cluster/summary',
            json=TEST_STORM_CLUSTER_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])
        result = self.check.get_storm_cluster_summary()
        self.assertEquals(TEST_STORM_CLUSTER_SUMMARY, result)

    @attr('request', 'nimbus')
    @responses.activate
    def test_get_storm_nimbus_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/nimbus/summary',
            json=TEST_STORM_NIMBUSES_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])
        result = self.check.get_storm_nimbus_summary()
        self.assertEquals(TEST_STORM_NIMBUSES_SUMMARY, result)

    @attr('request', 'supervisor')
    @responses.activate
    def test_get_storm_supervisor_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/supervisor/summary',
            json=TEST_STORM_SUPERVISOR_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])
        result = self.check.get_storm_supervisor_summary()
        self.assertEquals(TEST_STORM_SUPERVISOR_SUMMARY, result)

    @attr('request', 'topology_summary')
    @responses.activate
    def test_get_storm_topology_summary(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/summary',
            json=TEST_STORM_TOPOLOGY_SUMMARY,
            status=200
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])
        result = self.check.get_storm_topology_summary()
        self.assertEquals(TEST_STORM_TOPOLOGY_SUMMARY, result)

    @attr('request', 'topology')
    @responses.activate
    def test_get_storm_topology_info(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/my_topology-1-1489183263?window=60',
            json=TEST_STORM_TOPOLOGY_RESP,
            status=200,
            match_querystring=True
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])
        result = self.check.get_topology_info('my_topology-1-1489183263')
        self.assertEquals(TEST_STORM_TOPOLOGY_RESP, result)

    @attr('request', 'topology_metrics')
    @responses.activate
    def test_get_storm_topology_metrics(self):
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/my_topology-1-1489183263/metrics?window=60',
            json=TEST_STORM_TOPOLOGY_METRICS_RESP,
            status=200,
            match_querystring=True
        )

        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])
        result = self.check.get_topology_metrics('my_topology-1-1489183263')
        self.assertEquals(TEST_STORM_TOPOLOGY_METRICS_RESP, result)

    @attr('process', 'cluster')
    def test_process_cluster_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])

        results = defaultdict(list)

        def report_gauge(metric, value, tags, additional_tags):
            results[metric].append(value)

        self.check.report_gauge = report_gauge

        self.check.process_cluster_stats('test', TEST_STORM_CLUSTER_SUMMARY)
        self.assertEquals(13, len(results))

        # Check Cluster Stats
        self.assertEquals(33, results['storm.cluster.executorsTotal'][0])
        self.assertEquals(10, results['storm.cluster.slotsTotal'][0])
        self.assertEquals(4, results['storm.cluster.slotsFree'][0])
        self.assertEquals(1, results['storm.cluster.topologies'][0])
        self.assertEquals(1, results['storm.cluster.supervisors'][0])
        self.assertEquals(33, results['storm.cluster.tasksTotal'][0])
        self.assertEquals(6, results['storm.cluster.slotsUsed'][0])

    @attr('process', 'nimbus')
    def test_process_nimbus_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])

        results = defaultdict(list)

        def report_gauge(metric, value, tags, additional_tags):
            results[metric].append(value)

        self.check.report_gauge = report_gauge

        self.check.process_nimbus_stats('test', TEST_STORM_NIMBUSES_SUMMARY)
        self.assertEquals(5, len(results))

        # Check Leader Stats
        self.assertEquals(0, results['storm.nimbus.upTimeSeconds'][0])
        self.assertEquals(25842, results['storm.nimbus.upTimeSeconds'][1])

        # Check General Stats
        self.assertEquals(1, results['storm.nimbus.numLeaders'][0])
        self.assertEquals(0, results['storm.nimbus.numFollowers'][0])
        self.assertEquals(1, results['storm.nimbus.numOffline'][0])
        self.assertEquals(0, results['storm.nimbus.numDead'][0])

    @attr('process', 'supervisor')
    def test_process_supervisor_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])

        results = defaultdict(list)

        def report_gauge(metric, value, tags, additional_tags):
            results[metric].append(value)

        self.check.report_gauge = report_gauge

        self.check.process_supervisor_stats(TEST_STORM_SUPERVISOR_SUMMARY)
        self.assertEquals(7, len(results))

        # Check Supervisor Stats
        self.assertEquals(31559, results['storm.supervisor.uptimeSeconds'][0])
        self.assertEquals(10, results['storm.supervisor.slotsTotal'][0])
        self.assertEquals(6, results['storm.supervisor.slotsUsed'][0])
        self.assertEquals(3072, results['storm.supervisor.totalMem'][0])
        self.assertEquals(4992, results['storm.supervisor.usedMem'][0])
        self.assertEquals(900, results['storm.supervisor.totalCpu'][0])
        self.assertEquals(0, results['storm.supervisor.usedCpu'][0])

    @attr('process', 'topology')
    def test_process_topology_stats(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])

        results = defaultdict(list)

        def report_histogram(metric, value, tags, additional_tags):
            results[metric].append((value, tags, additional_tags))

        self.check.report_histogram = report_histogram

        self.check.process_topology_stats(TEST_STORM_TOPOLOGY_RESP, interval=60)
        self.assertEqual(47, len(results))

        # Check Topology Stats
        self.assertEquals(307606, results['storm.topologyStats.last_60.emitted'][0][0])
        self.assertEquals(307606, results['storm.topologyStats.last_60.transferred'][0][0])
        self.assertEquals(104673, results['storm.topologyStats.last_60.acked'][0][0])
        self.assertEquals(0, results['storm.topologyStats.last_60.failed'][0][0])
        self.assertEquals(285.950, results['storm.topologyStats.last_60.completeLatency'][0][0])
        self.assertEquals(1525788, results['storm.topologyStats.last_60.uptimeSeconds'][0][0])
        self.assertEquals(33, results['storm.topologyStats.last_60.executorsTotal'][0][0])
        self.assertEquals(6, results['storm.topologyStats.last_60.numBolts'][0][0])
        self.assertEquals(1, results['storm.topologyStats.last_60.replicationCount'][0][0])
        self.assertEquals(33, results['storm.topologyStats.last_60.tasksTotal'][0][0])
        self.assertEquals(1, results['storm.topologyStats.last_60.numSpouts'][0][0])
        self.assertEquals(6, results['storm.topologyStats.last_60.workersTotal'][0][0])

        # Check Bolt Stats
        self.assertEquals(3, results['storm.bolt.last_60.tasks'][0][0])
        self.assertTrue('bolt:Bolt1' in results['storm.bolt.last_60.tasks'][0][1])
        print results['storm.bolt.last_60.executeLatency']
        self.assertEquals(0.001, results['storm.bolt.last_60.executeLatency'][0][0])
        self.assertEquals(201.474, results['storm.bolt.last_60.processLatency'][0][0])
        self.assertEquals(0.000, results['storm.bolt.last_60.capacity'][0][0])
        self.assertEquals(0, results['storm.bolt.last_60.failed'][0][0])
        self.assertEquals(101309, results['storm.bolt.last_60.emitted'][0][0])
        self.assertEquals(212282, results['storm.bolt.last_60.acked'][0][0])
        self.assertEquals(101309, results['storm.bolt.last_60.transferred'][0][0])
        self.assertEquals(106311, results['storm.bolt.last_60.executed'][0][0])
        self.assertEquals(3, results['storm.bolt.last_60.executors'][0][0])
        self.assertEquals(1E10, results['storm.bolt.last_60.errorLapsedSecs'][0][0])

        # Check Spout Stats
        self.assertEquals(8, results['storm.spout.last_60.tasks'][0][0])
        self.assertTrue('spout:source' in results['storm.spout.last_60.tasks'][0][1])
        self.assertEquals(285.950, results['storm.spout.last_60.completeLatency'][0][0])
        self.assertEquals(0, results['storm.spout.last_60.failed'][0][0])
        self.assertEquals(104673, results['storm.spout.last_60.acked'][0][0])
        self.assertEquals(104673, results['storm.spout.last_60.transferred'][0][0])
        self.assertEquals(104673, results['storm.spout.last_60.emitted'][0][0])
        self.assertEquals(8, results['storm.spout.last_60.executors'][0][0])
        self.assertEquals(38737, results['storm.spout.last_60.errorLapsedSecs'][0][0])

    @attr('process', 'topology_metrics')
    def test_process_topology_metrics(self):
        self.load_check(self.STORM_CHECK_CONFIG, {})
        self.check.update_from_config(self.STORM_CHECK_CONFIG['instances'][0])

        results = defaultdict(list)

        def report_histogram(metric, value, tags, additional_tags):
            results[metric].append((value, tags, additional_tags))

        self.check.report_histogram = report_histogram

        self.check.process_topology_metrics('test', TEST_STORM_TOPOLOGY_METRICS_RESP, 60)
        self.assertEqual(10, len(results))

        # Check Bolt Stats
        self.assertEquals(120, results['storm.topologyStats.metrics.bolts.last_60.emitted'][0][0])
        self.assertIn('stream:__metrics', results['storm.topologyStats.metrics.bolts.last_60.emitted'][0][1])
        self.assertEquals(190748180, results['storm.topologyStats.metrics.bolts.last_60.emitted'][1][0])
        self.assertIn('stream:default', results['storm.topologyStats.metrics.bolts.last_60.emitted'][1][1])
        self.assertEquals(190718100, results['storm.topologyStats.metrics.bolts.last_60.emitted'][2][0])
        self.assertIn('stream:__ack_ack', results['storm.topologyStats.metrics.bolts.last_60.emitted'][2][1])
        self.assertEquals(20, results['storm.topologyStats.metrics.bolts.last_60.emitted'][3][0])
        self.assertIn('stream:__system', results['storm.topologyStats.metrics.bolts.last_60.emitted'][3][1])
        self.assertEquals(120, results['storm.topologyStats.metrics.bolts.last_60.transferred'][0][0])
        self.assertEquals(190733160, results['storm.topologyStats.metrics.bolts.last_60.acked'][0][0])
        self.assertEqual(0, len(results['storm.topologyStats.metrics.bolts.last_60.failed']))
        self.assertEqual(0, len(results['storm.topologyStats.metrics.bolts.last_60.complete_ms_avg']))
        self.assertEquals(0.004, results['storm.topologyStats.metrics.bolts.last_60.process_ms_avg'][0][0])
        self.assertEquals(190733140, results['storm.topologyStats.metrics.bolts.last_60.executed'][0][0])
        self.assertEquals(0.005, results['storm.topologyStats.metrics.bolts.last_60.executed_ms_avg'][0][0])

        # Check Spout Stats
        self.assertEquals(20, results['storm.topologyStats.metrics.spouts.last_60.emitted'][0][0])
        self.assertIn('stream:__metrics', results['storm.topologyStats.metrics.spouts.last_60.emitted'][0][1])
        self.assertEquals(17350280, results['storm.topologyStats.metrics.spouts.last_60.emitted'][1][0])
        self.assertIn('stream:default', results['storm.topologyStats.metrics.spouts.last_60.emitted'][1][1])
        self.assertEquals(17328160, results['storm.topologyStats.metrics.spouts.last_60.emitted'][2][0])
        self.assertIn('stream:__ack_init', results['storm.topologyStats.metrics.spouts.last_60.emitted'][2][1])
        self.assertEquals(20, results['storm.topologyStats.metrics.spouts.last_60.emitted'][3][0])
        self.assertIn('stream:__system', results['storm.topologyStats.metrics.spouts.last_60.emitted'][3][1])
        self.assertEquals(20, results['storm.topologyStats.metrics.spouts.last_60.transferred'][0][0])
        self.assertEquals(17339180, results['storm.topologyStats.metrics.spouts.last_60.acked'][0][0])
        self.assertEqual(0, len(results['storm.topologyStats.metrics.spouts.last_60.failed']))
        self.assertEqual(0, len(results['storm.topologyStats.metrics.spouts.last_60.process_ms_avg']))
        self.assertEqual(0, len(results['storm.topologyStats.metrics.spouts.last_60.executed_ms_avg']))
        self.assertEqual(0, len(results['storm.topologyStats.metrics.spouts.last_60.executed']))
        self.assertEquals(920.497, results['storm.topologyStats.metrics.spouts.last_60.complete_ms_avg'][0][0])

    @attr('check')
    @responses.activate
    def test_check(self):
        """
        Testing Storm check.
        """
        self.load_check(self.STORM_CHECK_CONFIG, {})

        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/cluster/summary',
            json=TEST_STORM_CLUSTER_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/nimbus/summary',
            json=TEST_STORM_NIMBUSES_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/supervisor/summary',
            json=TEST_STORM_SUPERVISOR_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/summary',
            json=TEST_STORM_TOPOLOGY_SUMMARY,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/my_topology-1-1489183263',
            json=TEST_STORM_TOPOLOGY_RESP,
            status=200
        )
        responses.add(
            responses.GET,
            'http://localhost:9005/api/v1/topology/my_topology-1-1489183263/metrics',
            json=TEST_STORM_TOPOLOGY_METRICS_RESP,
            status=200
        )

        # run your actual tests...
        self.run_check(self.STORM_CHECK_CONFIG['instances'][0])

        topology_tags = ['topology:my_topology']
        env_tags = ['env:test', 'environment:test']
        storm_version_tags = ['stormVersion:1.0.3']
        storm_cluster_environment_tags = ['stormClusterEnvironment:test']

        # Service Check
        self.assertServiceCheck(
            'topology-check.my_topology',
            count=1,
            status=AgentCheck.OK,
            tags=env_tags + storm_version_tags
        )

        # Cluster Stats
        test_cases = (
            ('executorsTotal', 1, 33),
            ('slotsTotal', 1, 10),
            ('slotsFree', 1, 4),
            ('topologies', 1, 1),
            ('supervisors', 1, 1),
            ('tasksTotal', 1, 33),
            ('slotsUsed', 1, 6),
            ('availCpu', 1, 0),
            ('totalCpu', 1, 0),
            ('cpuAssignedPercentUtil', 1, 0),
            ('availMem', 1, 0),
            ('totalMem', 1, 0),
            ('memAssignedPercentUtil', 1, 0)
        )
        test_tags = env_tags + storm_version_tags + storm_cluster_environment_tags
        for name, count, value in test_cases:
            self.assertMetric(
                'storm.cluster.{}'.format(name),
                count=count,
                value=value,
                tags=test_tags
            )

        # Nimbus Stats
        test_cases = (
            ('upTimeSeconds', 1, 25842, ['stormStatus:leader', 'stormHost:1.2.3.4']),
            ('upTimeSeconds', 1, 0, ['stormStatus:offline', 'stormHost:nimbus01.example.com']),
            ('numLeaders', 1, 1, []),
            ('numFollowers', 1, 0, []),
            ('numOffline', 1, 1, []),
            ('numDead', 1, 0, [])
        )
        test_tags = storm_cluster_environment_tags + env_tags + storm_version_tags

        for name, count, value, additional_tags in test_cases:
            self.assertMetric(
                'storm.nimbus.{}'.format(name),
                count=count,
                value=value,
                tags=test_tags + additional_tags
            )

        # Supervisor Stats
        test_cases = (
            ('uptimeSeconds', 1, 31559),
            ('slotsTotal', 1, 10),
            ('slotsUsed', 1, 6),
            ('totalMem', 1, 3072),
            ('usedMem', 1, 4992),
            ('totalCpu', 1, 900),
            ('usedCpu', 1, 0),

        )

        for name, count, value in test_cases:
            self.assertMetric(
                'storm.supervisor.{}'.format(name),
                count=count,
                value=value
            )

        # Topology Stats
        test_cases = (
            ('emitted', 1, 307606),
            ('transferred', 1, 307606),
            ('acked', 1, 104673),
            ('failed', 1, 0),
            ('completeLatency', 1, 285.950),
            ('uptimeSeconds', 1, 1525788),
            ('executorsTotal', 1, 33),
            ('numBolts', 1, 6),
            ('replicationCount', 1, 1),
            ('tasksTotal', 1, 33),
            ('numSpouts', 1, 1),
            ('workersTotal', 1, 6),
            ('assignedMemOnHeap', 1, 4992),
            ('assignedMemOffHeap', 1, 0),
            ('assignedTotalMem', 1, 4992),
            ('requestedMemOnHeap', 1, 0),
            ('requestedMemOffHeap', 1, 0),
            ('requestedCpu', 1, 0),
            ('assignedCpu', 1, 0),
            ('msgTimeout', 1, 300),
            ('debug', 1, 0),
            ('samplingPct', 1, 10)
        )

        test_tags = topology_tags + env_tags + storm_version_tags
        interval = 'last_60'

        for name, count, value in test_cases:
            self.assertHistogramMetric(
                'storm.topologyStats.{}.{}'.format(interval, name),
                count=count,
                value=value,
                tags=test_tags
            )

        # Bolt Stats
        for name, values in [
            ('Bolt1', (3, 0.001, 201.474, 0.000, 0, 212282, 101309, 106311, 101309, 3, 1E10, 0, 0, 0)),
            ('Bolt2', (2, 0.015, 0.010, 0.000, 0, 3153, 0, 3153, 0, 2, 1E10, 0, 0, 0)),
            ('Bolt3', (3, 0.009, 0.003, 0.000, 0, 4704, 0, 4704, 0, 3, 1E10, 0, 0, 0)),
            ('Bolt4', (4, 0.001, 291.756, 0.000, 0, 218808, 101607, 110946, 101607, 4, 1E10, 0, 0, 0)),
            ('Bolt5', (2, 0.001, 1014.634, 0.000, 0, 208890, 17, 104445, 17, 2, 1E10, 0, 0, 0)),
            ('Bolt6', (3, 0.010, 0.005, 0.000, 0, 4705, 0, 4705, 0, 3, 1E10, 0, 0, 0))
        ]:
            test_tags = storm_version_tags + env_tags + topology_tags + ['bolt:{}'.format(name)]
            for i, metric_name in enumerate([
                'tasks', 'executeLatency', 'processLatency', 'capacity', 'failed', 'acked', 'transferred', 'executed',
                'emitted', 'executors', 'errorLapsedSecs', 'requestedMemOnHeap', 'requestedCpu', 'requestedMemOffHeap'
            ]):
                self.assertHistogramMetric(
                    'storm.bolt.last_60.{}'.format(metric_name),
                    value=values[i],
                    tags=test_tags,
                    count=1
                )

        # Spout Stats
        for name, values in [
            ('source', (8, 285.950, 0, 104673, 104673, 104673, 8, 38737, 0, 0, 0)),
        ]:
            test_tags = storm_version_tags + topology_tags + env_tags + ['spout:{}'.format(name)]
            for i, metric_name in enumerate([
                'tasks', 'completeLatency', 'failed', 'acked', 'transferred', 'emitted', 'executors', 'errorLapsedSecs',
                'requestedMemOffHeap', 'requestedCpu', 'requestedMemOnHeap'
            ]):
                self.assertHistogramMetric(
                    'storm.spout.last_60.{}'.format(metric_name),
                    value=values[i],
                    tags=test_tags,
                    count=1
                )

        # Topology Metrics
        metric_cases = (
            # Topology Metrics By Bolt
            ('storm.topologyStats.metrics.bolts.last_60.transferred', 0.0,
             storm_version_tags + topology_tags + env_tags + ['bolts:count', 'stream:__system']),
        )

        for m in ['acked', 'complete_ms_avg', 'emitted', 'transferred']:
            self.assertHistogramMetric(
                'storm.topologyStats.metrics.spouts.last_60.{}'.format(m),
                at_least=1
            )

        for m in ['acked', 'emitted', 'executed', 'executed_ms_avg', 'process_ms_avg', 'transferred']:
            self.assertHistogramMetric(
                'storm.topologyStats.metrics.bolts.last_60.{}'.format(m),
                at_least=1
            )

        for case in metric_cases:
            self.assertHistogramMetric(case[0], value=case[1], tags=case[2], count=1)

        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()

    @attr('integration', 'check')
    def test_integration_with_ci_cluster(self):
        self.load_check(self.STORM_CHECK_INTEGRATION_CONFIG, {})

        # run your actual tests...
        self.run_check(self.STORM_CHECK_CONFIG['instances'][0])

        # Service Check
        self.assertServiceCheck(
            'topology-check.topology',
            count=1,
            status=AgentCheck.OK,
            tags=['env:integration', 'environment:integration', 'stormVersion:1.1.1']
        )

        topology_tags = ['topology:topology']
        env_tags = ['env:integration', 'environment:integration']
        storm_version_tags = ['stormVersion:1.1.1']
        storm_cluster_environment_tags = ['stormClusterEnvironment:integration']

        self.assertMetric(
            'storm.cluster.supervisors', value=1, count=1,
            tags=storm_cluster_environment_tags + storm_version_tags + env_tags
        )

        # Cluster Stats
        test_cases = (
            ('executorsTotal', 1, 28, True),
            ('slotsTotal', 1, 4, True),
            ('slotsFree', 1, 1, True),
            ('topologies', 1, 1, True),
            ('supervisors', 1, 1, True),
            ('tasksTotal', 1, 28, True),
            ('slotsUsed', 1, 3, True),
            ('availCpu', 1, None, False),
            ('totalCpu', 1, None, False),
            ('cpuAssignedPercentUtil', 1, None, False),
            ('availMem', 1, None, False),
            ('totalMem', 1, None, False),
            ('memAssignedPercentUtil', 1, None, False)
        )
        test_tags = storm_cluster_environment_tags + storm_version_tags + env_tags
        for name, count, value, test_value in test_cases:
            self.assertMetric(
                'storm.cluster.{}'.format(name),
                count=count,
                value=value if test_value else None,
                tags=test_tags
            )

        # Nimbus Stats
        test_cases = (
            ('numLeaders', 1, 1, []),
            ('numFollowers', 1, 0, []),
            ('numOffline', 1, 1, []),
            ('numDead', 1, 0, [])
        )
        test_tags = storm_cluster_environment_tags + env_tags + storm_version_tags

        for name, count, value, additional_tags in test_cases:
            self.assertMetric(
                'storm.nimbus.{}'.format(name),
                count=count,
                value=value,
                tags=test_tags + additional_tags
            )

        # Supervisor Stats
        test_cases = (
            ('slotsTotal', 1, 4, True),
            ('slotsUsed', 1, 3, True),
            ('totalMem', 1, None, False),
            ('usedMem', 1, None, False),
            ('totalCpu', 1, None, False),
            ('usedCpu', 1, None, False),

        )

        for name, count, value, test_value in test_cases:
            self.assertMetric(
                'storm.supervisor.{}'.format(name),
                count=count,
                value=value if test_value else None
            )

        # Topology Stats
        test_cases = (
            ('emitted', 1, None, False),
            ('transferred', 1, None, False),
            ('acked', 1, None, False),
            ('failed', 1, None, False),
            ('completeLatency', 1, None, False),
            ('uptimeSeconds', 1, None, False),
            ('executorsTotal', 1, 28, True),
            ('numBolts', 1, 2, True),
            ('replicationCount', 1, 1, True),
            ('tasksTotal', 1, 28, True),
            ('numSpouts', 1, 1, True),
            ('workersTotal', 1, 3, True),
            ('assignedMemOnHeap', 1, None, False),
            ('assignedMemOffHeap', 1, None, False),
            ('assignedTotalMem', 1, None, False),
            ('requestedMemOnHeap', 1, None, False),
            ('requestedMemOffHeap', 1, None, False),
            ('requestedCpu', 1, None, False),
            ('assignedCpu', 1, None, False),
            ('msgTimeout', 1, 30, True),
            ('debug', 1, 0, True),
            ('samplingPct', 1, None, False)
        )

        test_tags = topology_tags + env_tags + storm_version_tags
        interval = 'last_60'

        for name, count, value, test_value in test_cases:
            self.assertHistogramMetric(
                'storm.topologyStats.{}.{}'.format(interval, name),
                at_least=count,
                value=value if test_value else None,
                tags=test_tags
            )

        # Bolt Stats
        for name, values in [
            ('split', (8, None, None, None, None, None, None, None, None, 8, None, None, None, None)),
            ('count', (12, None, None, None, None, None, None, None, None, 12, None, None, None, None))
        ]:
            test_tags = env_tags + topology_tags + ['bolt:{}'.format(name)] + storm_version_tags
            for i, metric_name in enumerate([
                'tasks', 'executeLatency', 'processLatency', 'capacity', 'failed', 'acked', 'transferred', 'executed',
                'emitted', 'executors', 'errorLapsedSecs', 'requestedMemOnHeap', 'requestedCpu', 'requestedMemOffHeap'
            ]):
                self.assertHistogramMetric(
                    'storm.bolt.last_60.{}'.format(metric_name),
                    value=values[i],
                    tags=test_tags,
                    at_least=1
                )

        # Spout Stats
        for name, values in [
            ('spout', (5, None, None, None, None, None, 5, None, None, None, None)),
        ]:
            test_tags = topology_tags + ['spout:{}'.format(name)] + env_tags + storm_version_tags
            for i, metric_name in enumerate([
                'tasks', 'completeLatency', 'failed', 'acked', 'transferred', 'emitted', 'executors', 'errorLapsedSecs',
                'requestedMemOffHeap', 'requestedCpu', 'requestedMemOnHeap'
            ]):
                self.assertHistogramMetric(
                    'storm.spout.last_60.{}'.format(metric_name),
                    value=values[i],
                    tags=test_tags,
                    at_least=1
                )
