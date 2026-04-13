#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""CheckMK plugin for baker"""
# ~/local/lib/check_mk/base/cee/plugins/bakery/crowdsec.py

from pathlib import Path
from typing import TypedDict

from .bakery_api.v1 import (
    OS,
    Plugin,
    register,
    FileGenerator,
)

class CrowdSecConfig(TypedDict, total=False):
    interval: float

def get_crowdsec_plugin_files(conf: CrowdSecConfig) -> FileGenerator:
    yield Plugin(
      base_os=OS.LINUX,
      source=Path('crowdsec'),
      target=Path('crowdsec'),
      interval = int(conf.get('interval', 300)),
    )

register.bakery_plugin(
      name="crowdsec",
      files_function=get_crowdsec_plugin_files,
)
