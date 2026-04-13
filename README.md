# CrowdSec Monitoring Plugin for Checkmk

This plugin provides comprehensive monitoring of CrowdSec intrusion detection and prevention systems within Checkmk. It tracks parser health, alerts, bouncer activity, and decisions from both local and CAPI sources.

This plugin is designed for Checkmk 2.3 and above.

Based on the work of [nicoh88/checkmk-agent-based-crowdsec-plugin](https://github.com/nicoh88/checkmk-agent-based-crowdsec-plugin), extended with Agent Bakery support by [OETIKER+PARTNER AG](https://www.oetiker.ch).

## Features

This package includes five distinct checks:

- **CrowdSec Parser Health**: Monitors the parser success rate in percentage (configurable thresholds: WARN <80%, CRIT <60%).
- **CrowdSec Alerts**: Monitors alert counts for the last 1 hour and 24 hours, with configurable thresholds for both timeframes.
- **CrowdSec Bouncer Dropped**: Monitors the drop rate percentage of processed requests by bouncers (configurable thresholds: WARN >=1%, CRIT >=5%).
- **CrowdSec Decisions Local**: Tracks local decisions and displays the top N scenarios (default: top 5).
- **CrowdSec Decisions CAPI**: Tracks CAPI (Community API) decisions and displays the top N scenarios (default: top 5).

## 1. Installation (Checkmk Server)

The recommended installation method is using the MKP (Checkmk Extension Package).

### A. MKP Installation (Recommended)

1. Download the latest `.mkp` file from the Releases page.
2. In your Checkmk site, navigate to **Setup > Maintenance > Extension packages**.
3. Upload the downloaded `.mkp` file and activate the changes.

### B. Agent Bakery (Enterprise Edition)

If you are using the Checkmk Enterprise Edition, the agent plugin can be deployed automatically via the Agent Bakery:

1. Navigate to **Setup > Agents > Windows, Linux, Solaris, AIX > Agent rules**.
2. Search for **"CrowdSec (Linux)"** and create a new rule.
3. Configure the async execution interval (default: 300 seconds).
4. Bake and deploy the agent to the target hosts.

### C. Manual Agent Installation

If you are not using the Agent Bakery, deploy the agent plugin manually:

1. Copy the file `agent/crowdsec` from this repository to `/usr/lib/check_mk_agent/plugins/` on your target Linux machines.

2. Make the script executable:

   ```bash
   chmod +x /usr/lib/check_mk_agent/plugins/crowdsec
   ```

### Agent Configuration (Optional)

The agent plugin can be configured via configuration file or environment variables. Configuration precedence (highest to lowest):

1. Environment variables (prefix: `CROWDSEC_`)
2. Configuration file: `/etc/check_mk/crowdsec.cfg`
3. Default values

#### Configuration File Format

Create `/etc/check_mk/crowdsec.cfg` with the following content:

```bash
# Operating mode: "local" (default) or "docker"
MODE=local

# Path to cscli binary (for local mode)
CSCLI_BIN=/usr/bin/cscli

# Docker configuration (for docker mode)
DOCKER_BIN=/usr/bin/docker
CONTAINER=crowdsec

# Command timeout in seconds
TIMEOUT=15
```

#### Docker Mode

If CrowdSec is running in a Docker container, set `MODE=docker` in the configuration file. The plugin will then execute `cscli` commands inside the specified container.

Example for Docker mode:

```bash
MODE=docker
CONTAINER=crowdsec
```

#### Environment Variables

Alternatively, you can configure the plugin using environment variables:

```bash
export CROWDSEC_MODE=docker
export CROWDSEC_CONTAINER=crowdsec
export CROWDSEC_TIMEOUT=20
```

## 2. Configuration

1. After deploying the agent plugin and installing the MKP, go to the properties of a configured host in Checkmk.

2. Run a service discovery (**Setup > Services > Service discovery**). Checkmk should now discover the new "CrowdSec" services.

3. To adjust thresholds, search for **"CrowdSec level"** in the setup menu and create a new rule.

### Available Threshold Parameters

The following thresholds can be configured:

| Parameter | Description | Default WARN | Default CRIT |
|-----------|-------------|--------------|--------------|
| Parser success rate | Percentage of successfully parsed logs | <80% | <60% |
| Drop rate | Percentage of dropped requests by bouncers | >=1% | >=5% |
| Alerts (1h) | Number of alerts in the last hour | >=200 | >=500 |
| Alerts (24h) | Number of alerts in the last 24 hours | >=2000 | >=5000 |
| Top reasons | Number of top scenarios displayed in decisions summary | 5 | - |

## 3. Monitored Metrics

### Parser Health
- **success_rate**: Parser success rate in percentage
- **parser_ok**: Number of successfully parsed log entries
- **parser_total**: Total number of log entries processed

### Alerts
- **alerts_last_1h**: Number of alerts triggered in the last hour
- **alerts_last_24h**: Number of alerts triggered in the last 24 hours
- **alerts_total**: Total number of alerts since CrowdSec started

### Bouncer Activity
- **droprate_pct**: Percentage of requests dropped by bouncers
- **dropped_requests**: Total number of dropped requests
- **processed_requests**: Total number of processed requests

### Decisions
- **decisions_local**: Number of active local decisions
- **decisions_capi**: Number of active CAPI decisions
- **top_local**: List of top N local decision scenarios with counts
- **top_capi**: List of top N CAPI decision scenarios with counts

## 4. Building the MKP

Prerequisites:

```bash
python3 -m venv .venv
.venv/bin/pip install mkp
```

Build:

```bash
.venv/bin/python build_mkp.py
```

The MKP file will be created in `build/dist/`.

## 5. Troubleshooting

### Plugin Returns No Data

- Verify that CrowdSec is running: `systemctl status crowdsec`
- Check if `cscli` is accessible: `which cscli`
- Test the plugin manually: `/usr/lib/check_mk_agent/plugins/crowdsec`
- For Docker mode: Verify container name and Docker accessibility

### Permission Issues

The Checkmk agent needs permission to execute `cscli` commands. If running as non-root, you may need to configure sudo:

```bash
# /etc/sudoers.d/checkmk-crowdsec
cmkagent ALL=(ALL) NOPASSWD: /usr/bin/cscli metrics -o json
cmkagent ALL=(ALL) NOPASSWD: /usr/bin/cscli alerts list *
cmkagent ALL=(ALL) NOPASSWD: /usr/bin/cscli decisions list *
```

### Docker Mode Issues

- Verify the container is running: `docker ps | grep crowdsec`
- Test Docker exec manually: `docker exec crowdsec cscli metrics -o json`
- Ensure the Checkmk agent user has Docker permissions

### Slow or Hanging Commands

If `cscli alerts list` or `cscli decisions list` are slow or hang, this is typically caused by:

- A large number of CAPI decisions in the local database
- An unreachable remote LAPI server (check `/etc/crowdsec/local_api_credentials.yaml`)
- SQLite performance issues (consider enabling WAL mode with `use_wal: true` in `/etc/crowdsec/config.yaml`)

The plugin handles timeouts gracefully and will report partial data with error details.

## 6. Performance Considerations

The plugin executes multiple `cscli` commands per check cycle. To minimize performance impact:

- The default timeout is set to 15 seconds per command
- Consider increasing the check interval for high-traffic systems via the Agent Bakery rule
- With many CAPI decisions, the total runtime can be up to 5 x timeout (75 seconds default)
