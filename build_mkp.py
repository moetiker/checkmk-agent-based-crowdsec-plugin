#!/usr/bin/env python3
"""Build the CrowdSec MKP package using the mkp library.

Usage: .venv/bin/python build_mkp.py
"""

import os
import shutil
import mkp

BASEDIR = os.path.dirname(os.path.realpath(__file__))
STAGEDIR = os.path.join(BASEDIR, "_stage")

INFO = {
    "author": "OETIKER+PARTNER AG",
    "description": "Monitoring of CrowdSec IDS/IPS",
    "download_url": "https://github.com/oetiker/checkmk_plugin_crowdsec",
    "name": "crowdsec",
    "title": "CrowdSec monitoring with agent plugin",
    "version": "0.3.3",
    "version.min_required": "2.3.0",
    "version.packaged": "python-mkp",
    "version.usable_until": None,
}

# Map source files to the mkp directory layout
FILES = {
    "agents/plugins/crowdsec":
        "agent/crowdsec",
    "cmk_addons_plugins/crowdsec/agent_based/crowdsec.py":
        "src/cmk_addons/plugins/crowdsec/agent_based/crowdsec.py",
    "cmk_addons_plugins/crowdsec/graphing/graphing_crowdsec.py":
        "src/cmk_addons/plugins/crowdsec/graphing/graphing_crowdsec.py",
    "cmk_addons_plugins/crowdsec/rulesets/ruleset_crowdsec.py":
        "src/cmk_addons/plugins/crowdsec/rulesets/ruleset_crowdsec.py",
    "cmk_addons_plugins/crowdsec/rulesets/ruleset_crowdsec_bakery.py":
        "src/cmk_addons/plugins/crowdsec/rulesets/ruleset_crowdsec_bakery.py",
    "lib/check_mk/base/cee/plugins/bakery/crowdsec.py":
        "bakery/crowdsec.py",
}


def main():
    # Clean and create staging directory
    if os.path.exists(STAGEDIR):
        shutil.rmtree(STAGEDIR)

    # Stage files into mkp-expected layout
    for dest, src in FILES.items():
        src_path = os.path.join(BASEDIR, src)
        dst_path = os.path.join(STAGEDIR, dest)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)

    # Build using mkp.dist which scans directories and creates the .mkp
    mkp.dist(INFO, path=STAGEDIR)

    # Move .mkp to build/dist/
    dist_src = os.path.join(STAGEDIR, "dist")
    dist_dst = os.path.join(BASEDIR, "build", "dist")
    if os.path.exists(dist_dst):
        shutil.rmtree(dist_dst)
    os.makedirs(dist_dst, exist_ok=True)

    for f in os.listdir(dist_src):
        shutil.move(os.path.join(dist_src, f), os.path.join(dist_dst, f))

    # Clean up staging
    shutil.rmtree(STAGEDIR)

    mkp_file = os.path.join(dist_dst, f"{INFO['name']}-{INFO['version']}.mkp")
    print(f"Built: {mkp_file}")


if __name__ == "__main__":
    main()
