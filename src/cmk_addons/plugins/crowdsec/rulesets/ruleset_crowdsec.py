from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostCondition

def _parameter_form():
    return Dictionary(
        elements={
            "parser_warn": DictElement(
                parameter_form=Float(
                    title=Title("Parser success WARN below (%)"),
                    prefill=DefaultValue(98.0),
                ),
                required=True,
            ),
            "parser_crit": DictElement(
                parameter_form=Float(
                    title=Title("Parser success CRIT below (%)"),
                    prefill=DefaultValue(95.0),
                ),
                required=True,
            ),
            "droprate_warn": DictElement(
                parameter_form=Float(
                    title=Title("Drop rate WARN at/above (%)"),
                    prefill=DefaultValue(1.0),
                ),
                required=True,
            ),
            "droprate_crit": DictElement(
                parameter_form=Float(
                    title=Title("Drop rate CRIT at/above (%)"),
                    prefill=DefaultValue(5.0),
                ),
                required=True,
            ),
            "alerts_1h_warn": DictElement(
                parameter_form=Integer(
                    title=Title("Alerts last 1h WARN at/above"),
                    prefill=DefaultValue(20),
                ),
                required=True,
            ),
            "alerts_1h_crit": DictElement(
                parameter_form=Integer(
                    title=Title("Alerts last 1h CRIT at/above"),
                    prefill=DefaultValue(50),
                ),
                required=True,
            ),
            "alerts_24h_warn": DictElement(
                parameter_form=Integer(
                    title=Title("Alerts last 24h WARN at/above"),
                    prefill=DefaultValue(100),
                ),
                required=True,
            ),
            "alerts_24h_crit": DictElement(
                parameter_form=Integer(
                    title=Title("Alerts last 24h CRIT at/above"),
                    prefill=DefaultValue(500),
                ),
                required=True,
            ),
            "top_reasons": DictElement(
                parameter_form=Integer(
                    title=Title("Top-N Szenarien in Decisions-Summary"),
                    prefill=DefaultValue(5),
                ),
                required=True,
            ),
        }
    )

rule_spec_crowdsec_parameters = CheckParameters(
    name="crowdsec_parameters",
    title=Title("CrowdSec level"),
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_form,
)
