# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.bind9 import Bind9Check

EXPECTED_VALUES = (
    ('bind9.opcode_QUERY', 0),
    ('bind9.opcode_IQUERY', 0),
    ('bind9.opcode_STATUS', 0),
    ('bind9.opcode_RESERVED3', 0),
    ('bind9.opcode_NOTIFY', 0),
    ('bind9.opcode_UPDATE', 0),
    ('bind9.opcode_RESERVED6', 0),
    ('bind9.opcode_RESERVED7', 0),
    ('bind9.opcode_RESERVED8', 0),
    ('bind9.opcode_RESERVED9', 0),
    ('bind9.opcode_RESERVED10', 0),
    ('bind9.opcode_RESERVED11', 0),
    ('bind9.opcode_RESERVED12', 0),
    ('bind9.opcode_RESERVED13', 0),
    ('bind9.opcode_RESERVED14', 0),
    ('bind9.opcode_RESERVED15', 0),
    ('bind9.nsstat_Requestv4', 0),
    ('bind9.nsstat_Requestv6', 0),
    ('bind9.nsstat_ReqEdns0', 0),
    ('bind9.nsstat_ReqBadEDNSVer', 0),
    ('bind9.nsstat_ReqTSIG', 0),
    ('bind9.nsstat_ReqSIG0', 0),
    ('bind9.nsstat_ReqBadSIG', 0),
    ('bind9.nsstat_ReqTCP', 0),
    ('bind9.nsstat_AuthQryRej', 0),
    ('bind9.nsstat_RecQryRej', 0),
    ('bind9.nsstat_XfrRej', 0),
    ('bind9.nsstat_UpdateRej', 0),
    ('bind9.nsstat_Response', 0),
    ('bind9.nsstat_TruncatedResp', 0),
    ('bind9.nsstat_RespEDNS0', 0),
    ('bind9.nsstat_RespTSIG', 0),
    ('bind9.nsstat_RespSIG0', 0),
    ('bind9.nsstat_QrySuccess', 0),
    ('bind9.nsstat_QryAuthAns', 0),
    ('bind9.nsstat_QryNoauthAns', 0),
    ('bind9.nsstat_QryReferral', 0),
    ('bind9.nsstat_QryNxrrset', 0),
    ('bind9.nsstat_QrySERVFAIL', 0),
    ('bind9.nsstat_QryFORMERR', 0),
    ('bind9.nsstat_QryNXDOMAIN', 0),
    ('bind9.nsstat_QryRecursion', 0),
    ('bind9.nsstat_QryDuplicate', 0),
    ('bind9.nsstat_QryDropped', 0),
    ('bind9.nsstat_QryFailure', 0),
    ('bind9.nsstat_XfrReqDone', 0),
    ('bind9.nsstat_UpdateReqFwd', 0),
    ('bind9.nsstat_UpdateRespFwd', 0),
    ('bind9.nsstat_UpdateFwdFail', 0),
    ('bind9.nsstat_UpdateDone', 0),
    ('bind9.nsstat_UpdateFail', 0),
    ('bind9.nsstat_UpdateBadPrereq', 0),
    ('bind9.nsstat_RecursClients', 0),
    ('bind9.nsstat_DNS64', 0),
    ('bind9.nsstat_RateDropped', 0),
    ('bind9.nsstat_RateSlipped', 0),
    ('bind9.nsstat_RPZRewrites', 0),
    ('bind9.nsstat_QryUDP', 0),
    ('bind9.nsstat_QryTCP', 0),
    ('bind9.nsstat_NSIDOpt', 0),
    ('bind9.nsstat_ExpireOpt', 0),
    ('bind9.nsstat_OtherOpt', 0),
    ('bind9.nsstat_SitOpt', 0),
    ('bind9.nsstat_SitNew', 0),
    ('bind9.nsstat_SitBadSize', 0),
    ('bind9.nsstat_SitBadTime', 0),
    ('bind9.nsstat_SitNoMatch', 0),
    ('bind9.nsstat_SitMatch', 0),
    ('bind9.zonestat_NotifyOutv4', 0),
    ('bind9.zonestat_NotifyOutv6', 0),
    ('bind9.zonestat_NotifyInv4', 0),
    ('bind9.zonestat_NotifyInv6', 0),
    ('bind9.zonestat_NotifyRej', 0),
    ('bind9.zonestat_SOAOutv4', 0),
    ('bind9.zonestat_SOAOutv6', 0),
    ('bind9.zonestat_AXFRReqv4', 0),
    ('bind9.zonestat_AXFRReqv6', 0),
    ('bind9.zonestat_IXFRReqv4', 0),
    ('bind9.zonestat_IXFRReqv6', 0),
    ('bind9.zonestat_XfrSuccess', 0),
    ('bind9.zonestat_XfrFail', 0),
    ('bind9.sockstat_UDP4Open', 11),
    ('bind9.sockstat_UDP6Open', 5),
    ('bind9.sockstat_TCP4Open', 8),
    ('bind9.sockstat_TCP6Open', 2),
    ('bind9.sockstat_UnixOpen', 0),
    ('bind9.sockstat_RawOpen', 1),
    ('bind9.sockstat_UDP4OpenFail', 0),
    ('bind9.sockstat_UDP6OpenFail', 0),
    ('bind9.sockstat_TCP4OpenFail', 0),
    ('bind9.sockstat_TCP6OpenFail', 0),
    ('bind9.sockstat_UnixOpenFail', 0),
    ('bind9.sockstat_RawOpenFail', 0),
    ('bind9.sockstat_UDP4Close', 5),
    ('bind9.sockstat_UDP6Close', 3),
    ('bind9.sockstat_TCP4Close', 93),
    ('bind9.sockstat_TCP6Close', 0),
    ('bind9.sockstat_UnixClose', 0),
    ('bind9.sockstat_FDWatchClose', 0),
    ('bind9.sockstat_RawClose', 0),
    ('bind9.sockstat_UDP4BindFail', 0),
    ('bind9.sockstat_UDP6BindFail', 0),
    ('bind9.sockstat_TCP4BindFail', 0),
    ('bind9.sockstat_TCP6BindFail', 0),
    ('bind9.sockstat_UnixBindFail', 0),
    ('bind9.sockstat_FdwatchBindFail', 0),
    ('bind9.sockstat_UDP4ConnFail', 0),
    ('bind9.sockstat_UDP6ConnFail', 3),
    ('bind9.sockstat_TCP4ConnFail', 0),
    ('bind9.sockstat_TCP6ConnFail', 0),
    ('bind9.sockstat_UnixConnFail', 0),
    ('bind9.sockstat_FDwatchConnFail', 0),
    ('bind9.sockstat_UDP4Conn', 5),
    ('bind9.sockstat_UDP6Conn', 0),
    ('bind9.sockstat_TCP4Conn', 3),
    ('bind9.sockstat_TCP6Conn', 0),
    ('bind9.sockstat_UnixConn', 0),
    ('bind9.sockstat_FDwatchConn', 0),
    ('bind9.sockstat_TCP4AcceptFail', 0),
    ('bind9.sockstat_TCP6AcceptFail', 0),
    ('bind9.sockstat_UnixAcceptFail', 0),
    ('bind9.sockstat_TCP4Accept', 64),
    ('bind9.sockstat_TCP6Accept', 0),
    ('bind9.sockstat_UnixAccept', 0),
    ('bind9.sockstat_UDP4SendErr', 0),
    ('bind9.sockstat_UDP6SendErr', 3),
    ('bind9.sockstat_TCP4SendErr', 0),
    ('bind9.sockstat_TCP6SendErr', 0),
    ('bind9.sockstat_UnixSendErr', 0),
    ('bind9.sockstat_FDwatchSendErr', 0),
    ('bind9.sockstat_UDP4RecvErr', 0),
    ('bind9.sockstat_UDP6RecvErr', 0),
    ('bind9.sockstat_TCP4RecvErr', 0),
    ('bind9.sockstat_TCP6RecvErr', 0),
    ('bind9.sockstat_UnixRecvErr', 0),
    ('bind9.sockstat_FDwatchRecvErr', 0),
    ('bind9.sockstat_RawRecvErr', 0),
    ('bind9.sockstat_UDP4Active', 6),
    ('bind9.sockstat_UDP6Active', 2),
    ('bind9.sockstat_TCP4Active', 69),
    ('bind9.sockstat_TCP6Active', 2),
    ('bind9.sockstat_UnixActive', 0),
    ('bind9.sockstat_RawActive', 1)
)

Date = ["2018-08-08T01-15-46Z", "2010-08-08T01-15-46Z"]
Epoch = ["1533690946", "1281230146"]


def test_check(aggregator, instance):
    c = Bind9Check('bind9', {}, {}, None)

    with pytest.raises(ConfigurationError):
        c.check({})

    c.check(instance)

    for metric, value in EXPECTED_VALUES:
        aggregator.assert_metric(metric, value=value)

    aggregator.assert_service_check(c.BIND_SERVICE_CHECK, c.OK)
    aggregator.assert_all_metrics_covered()


def test_DateTimeToEpoch():
    c = Bind9Check('bind9', {}, {}, None)
    assert c.DateTimeToEpoch(Date[0]) == Epoch[0]
    assert c.DateTimeToEpoch(Date[1]) == Epoch[1]
