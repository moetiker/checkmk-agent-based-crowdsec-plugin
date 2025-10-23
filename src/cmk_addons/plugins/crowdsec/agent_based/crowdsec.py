from cmk.agent_based.v2 import (
    AgentSection, CheckPlugin, Service, Result, State, Metric,
    DiscoveryResult, StringTable, check_levels,
)
import json
from typing import Dict, Iterator, Union, List

Section = Dict[str, object]

def parse_crowdsec(string_table: StringTable) -> Union[Section, None]:
    if not string_table or not string_table[0]:
        return None
    line = " ".join(string_table[0]).strip()
    try:
        data = json.loads(line)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    return data

agent_section_crowdsec = AgentSection(
    name="crowdsec",
    parse_function=parse_crowdsec,
)

def _int(v, d=0) -> int:
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return d

def _fmt_top(agent_list: List[List[object]], n: int) -> str:
    if not agent_list or n <= 0:
        return "none"
    return ", ".join(f"{name}:{cnt}" for name, cnt in agent_list[:n])

def discover_crowdsec(section: Section) -> DiscoveryResult:
    if not section:
        return
    yield Service(item="Parser Health")
    yield Service(item="Alerts")
    yield Service(item="Bouncer Dropped")
    yield Service(item="Decisions Local")
    yield Service(item="Decisions CAPI")

def check_crowdsec(item: str, params: dict, section: Section):
    params = params or {}
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data received")
        return

    if item == "Parser Health":
        ok = _int(section.get("parser_ok"), 0)
        total = _int(section.get("parser_total"), 0)
        rate = float(section.get("success_rate", 0.0))
        if total <= 0:
            yield Result(state=State.OK, summary="Parser success rate: 0.00% (Parsed 0 / Total 0)")
            yield Metric("success_rate", 0.0)
            return
        warn = float(params.get("parser_warn", 98.0))
        crit = float(params.get("parser_crit", 95.0))
        summary = f"Parser success rate: {rate:.2f}% (Parsed {ok} / Total {total})"
        for entry in check_levels(
            value=rate,
            metric_name="success_rate",
            label="Parser success rate (%)",
            levels_lower=("fixed", (warn, crit)),
            boundaries=(0.0, 100.0),
            notice_only=False,
        ):
            if isinstance(entry, Result):
                yield Result(state=entry.state, summary=summary)
            else:
                yield entry
        
        #yield Metric("parser_ok", ok)
        #yield Metric("parser_total", total)
        return

    if item == "Alerts":
        v24 = _int(section.get("alerts_last_24h"), 0)
        v1h = _int(section.get("alerts_last_1h"), 0)
        vtot = _int(section.get("alerts_total"), 0)
        warn_24h = int(params.get("alerts_24h_warn", 100))
        crit_24h = int(params.get("alerts_24h_crit", 500))
        warn_1h = int(params.get("alerts_1h_warn", 20))
        crit_1h = int(params.get("alerts_1h_crit", 50))
        state_24h = State.CRIT if v24 >= crit_24h else State.WARN if v24 >= warn_24h else State.OK
        state_1h = State.CRIT if v1h >= crit_1h else State.WARN if v1h >= warn_1h else State.OK
        overall_state = State.CRIT if State.CRIT in (state_24h, state_1h) else State.WARN if State.WARN in (state_24h, state_1h) else State.OK
        parts = []
        parts.append(f"24h: {v24}" + ("" if state_24h == State.OK else f" ({'CRIT' if state_24h == State.CRIT else 'WARN'})"))
        parts.append(f"1h: {v1h}" + ("" if state_1h == State.OK else f" ({'CRIT' if state_1h == State.CRIT else 'WARN'})"))
        parts.append(f"total: {vtot}")
        summary = "Alerts " + ", ".join(parts)
        yield Result(state=overall_state, summary=summary)
        yield Metric("alerts_last_24h", v24)
        yield Metric("alerts_last_1h", v1h)
        yield Metric("alerts_total", vtot)
        return

    if item == "Bouncer Dropped":
        processed = _int(section.get("processed_requests"), 0)
        dropped = _int(section.get("dropped_requests"), 0)
        rate = float(section.get("droprate_pct", 0.0))
        warn = float(params.get("droprate_warn", 1.0))
        crit = float(params.get("droprate_crit", 5.0))
        summary = f"Bouncer dropped rate: {rate:.2f}% (Dropped {dropped} / Processed {processed})"
        for entry in check_levels(
            value=rate,
            metric_name="droprate_pct",
            label="Drop rate (%)",
            levels_upper=("fixed", (warn, crit)),
            boundaries=(0.0, 100.0),
            notice_only=False,
        ):
            if isinstance(entry, Result):
                yield Result(state=entry.state, summary=summary)
            else:
                yield entry

        #yield Metric("dropped_requests", dropped)
        #yield Metric("processed_requests", processed)
        return

    if item == "Decisions Local":
        local_cnt = _int(section.get("decisions_local"), 0)
        top_local = section.get("top_local", [])
        top_n = int(params.get("top_reasons", 5))
        yield Result(state=State.OK, summary=f"Local decisions: {local_cnt}; top: {_fmt_top(top_local, top_n)}")
        yield Metric("decisions_local", local_cnt)
        return

    if item == "Decisions CAPI":
        capi_cnt = _int(section.get("decisions_capi"), 0)
        top_capi = section.get("top_capi", [])
        top_n = int(params.get("top_reasons", 5))
        yield Result(state=State.OK, summary=f"CAPI decisions: {capi_cnt}; top: {_fmt_top(top_capi, top_n)}")
        yield Metric("decisions_capi", capi_cnt)
        return

check_plugin_crowdsec = CheckPlugin(
    name="crowdsec",
    service_name="CrowdSec %s",
    discovery_function=discover_crowdsec,
    check_function=check_crowdsec,
    check_ruleset_name="crowdsec_parameters",
    sections=["crowdsec"],
    check_default_parameters={
        "parser_warn": 98.0,
        "parser_crit": 95.0,
        "droprate_warn": 1.0,
        "droprate_crit": 5.0,
        "alerts_1h_warn": 20,
        "alerts_1h_crit": 50,
        "alerts_24h_warn": 100,
        "alerts_24h_crit": 500,
        "top_reasons": 5,
    },
)
