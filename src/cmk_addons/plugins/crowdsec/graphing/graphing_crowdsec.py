#!/usr/bin/env python3
from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import Color, DecimalNotation, StrictPrecision, Metric, Unit
from cmk.graphing.v1.perfometers import Closed, FocusRange, Perfometer

# Metrics
metric_crowdsec_alerts_last_24h = Metric(
    name="alerts_last_24h",
    title=Title("CrowdSec Alerts last 24h"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.YELLOW,
)

metric_crowdsec_alerts_last_1h = Metric(
    name="alerts_last_1h",
    title=Title("CrowdSec Alerts last 1h"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.YELLOW,
)

# GEÄNDERT: Von "Total Alerts" zu "Alerts total"
metric_crowdsec_alerts_total = Metric(
    name="alerts_total",
    title=Title("CrowdSec Alerts total"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.YELLOW,
)

metric_crowdsec_success_rate = Metric(
    name="success_rate",
    title=Title("CrowdSec Parser Success Rate"),
    unit=Unit(DecimalNotation(" %"), StrictPrecision(2)),
    color=Color.GREEN,
)

metric_crowdsec_parser_ok = Metric(
    name="parser_ok",
    title=Title("CrowdSec Parser OK"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.GREEN,
)

metric_crowdsec_parser_total = Metric(
    name="parser_total",
    title=Title("CrowdSec Parser Total"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.GREEN,
)

metric_crowdsec_droprate_pct = Metric(
    name="droprate_pct",
    title=Title("CrowdSec Drop Rate"),
    unit=Unit(DecimalNotation(" %"), StrictPrecision(2)),
    color=Color.YELLOW,
)

metric_crowdsec_dropped_requests = Metric(
    name="dropped_requests",
    title=Title("CrowdSec Dropped Requests"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.YELLOW,
)

metric_crowdsec_processed_requests = Metric(
    name="processed_requests",
    title=Title("CrowdSec Processed Requests"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.YELLOW,
)

metric_crowdsec_decisions_local = Metric(
    name="decisions_local",
    title=Title("CrowdSec Decisions Local"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.RED,
)

metric_crowdsec_decisions_capi = Metric(
    name="decisions_capi",
    title=Title("CrowdSec Decisions CAPI"),
    unit=Unit(DecimalNotation(""), StrictPrecision(0)),
    color=Color.RED,
)

# Perf-O-Meters
perfometer_crowdsec_success_rate = Perfometer(
    name="crowdsec_success_rate_perfometer",
    focus_range=FocusRange(Closed(0), Closed(100)),
    segments=["success_rate"],
)

perfometer_crowdsec_droprate = Perfometer(
    name="crowdsec_droprate_perfometer",
    focus_range=FocusRange(Closed(0), Closed(10)),
    segments=["droprate_pct"],
)

perfometer_crowdsec_alerts = Perfometer(
    name="crowdsec_alerts_perfometer",
    focus_range=FocusRange(Closed(0), Closed(1000)),
    segments=["alerts_last_24h"],
)

perfometer_crowdsec_dropped = Perfometer(
    name="crowdsec_dropped_requests_perfometer",
    focus_range=FocusRange(Closed(0), Closed(20000)),
    segments=["dropped_requests"],
)

perfometer_crowdsec_processed = Perfometer(
    name="crowdsec_processed_requests_perfometer",
    focus_range=FocusRange(Closed(0), Closed(500000)),
    segments=["processed_requests"],
)

perfometer_crowdsec_decisions_local = Perfometer(
    name="crowdsec_decisions_local_perfometer",
    focus_range=FocusRange(Closed(0), Closed(100)),
    segments=["decisions_local"],
)

perfometer_crowdsec_decisions_capi = Perfometer(
    name="crowdsec_decisions_capi_perfometer",
    focus_range=FocusRange(Closed(0), Closed(20000)),
    segments=["decisions_capi"],
)
