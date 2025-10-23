# CrowdSec Monitoring Plugin for Checkmk

This plugin provides comprehensive monitoring of CrowdSec intrusion detection and prevention systems within Checkmk. It tracks parser health, alerts, bouncer activity, and decisions from both local and CAPI sources.

This plugin is designed for Checkmk 2.3 and above.

> **A Note from the Author**
>
> I am not a professional software developer, but an IT admin with a background in scripting. This project came to life through a combination of practical experience, assistance from AI / KI, and a good amount of trial and error to solve a real-world problem.
>
> Since this is a practical solution, improvements and suggestions are highly encouraged! Please feel free to submit a Pull Request with any enhancements. If you have any questions about the approach or need help, you're welcome to open an Issue.

## Features

This package includes five distinct checks:

- **CrowdSec Parser Health**: Monitors the parser success rate in percentage (configurable thresholds: WARN <98%, CRIT <95%).
- **CrowdSec Alerts**: Monitors alert counts for the last 1 hour and 24 hours, with configurable thresholds for both timeframes.
- **CrowdSec Bouncer Dropped**: Monitors the drop rate percentage of processed requests by bouncers (configurable thresholds: WARN ≥1%, CRIT ≥5%).
- **CrowdSec Decisions Local**: Tracks local decisions and displays the top N scenarios (default: top 5).
- **CrowdSec Decisions CAPI**: Tracks CAPI (Community API) decisions and displays the top N scenarios (default: top 5).

![CrowdSec Services in Checkmk](https://github.com/nicoh88/checkmk-agent-based-crowdsec-plugin/blob/main/screenshot.png?raw=true)

## 1. Agent Setup

This plugin requires an agent-side script to be deployed on the monitored hosts. The script queries CrowdSec metrics using the `cscli` command-line tool.

### Prerequisites

- CrowdSec must be installed and running on the target host
- The `cscli` binary must be accessible (default: `/usr/bin/cscli`)
- For Docker installations: Docker must be installed and the CrowdSec container must be running

### Installation Steps

1. Copy the file `agent/crowdsec` from this repository to `/usr/lib/check_mk_agent/plugins/` on your target Linux machines.

2. Make the script executable:

   ```bash
   chmod +x /usr/lib/check_mk_agent/plugins/crowdsec
   ```

### Configuration (Optional)

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

## 2. Installation (Checkmk Server)

The recommended installation method is using the MKP (Checkmk Extension Package).

### A. MKP Installation (Recommended)

1. Download the latest `.mkp` file from the Releases page.
2. In your Checkmk site, navigate to **Setup > Maintenance > Extension packages**.
3. Upload the downloaded `.mkp` file and activate the changes.

### B. Manual Installation

For development or testing, you can copy the plugin files manually into your Checkmk site. **Replace `mysite` with your site's name.**

1. Clone this repository to a temporary location on your Checkmk server.

2. Create the necessary directories within your site's `local` path:

   ```bash
   SITE_PATH=~/sites/mysite
   mkdir -p $SITE_PATH/local/lib/python3/cmk_addons/plugins/crowdsec/agent_based
   mkdir -p $SITE_PATH/local/lib/python3/cmk_addons/plugins/crowdsec/graphing
   mkdir -p $SITE_PATH/local/lib/python3/cmk_addons/plugins/crowdsec/rulesets
   ```

3. Copy the plugin files from the cloned repository into the newly created directories:

   ```bash
   # Copy agent-based checks
   cp src/cmk_addons/plugins/crowdsec/agent_based/*.py $SITE_PATH/local/lib/python3/cmk_addons/plugins/crowdsec/agent_based/

   # Copy graphing definitions
   cp src/cmk_addons/plugins/crowdsec/graphing/*.py $SITE_PATH/local/lib/python3/cmk_addons/plugins/crowdsec/graphing/

   # Copy ruleset definitions
   cp src/cmk_addons/plugins/crowdsec/rulesets/*.py $SITE_PATH/local/lib/python3/cmk_addons/plugins/crowdsec/rulesets/
   ```

4. Restart the site to apply the changes: `omd restart mysite`.

## 3. Configuration

1. After deploying the agent plugin and installing the MKP, go to the properties of a configured host in Checkmk.

2. Run a service discovery (**Setup > Services > Service discovery**). Checkmk should now discover the new "CrowdSec" services.

3. To adjust thresholds, search for **"CrowdSec – Schwellwerte"** (or **"CrowdSec thresholds"**) in the setup menu and create a new rule.

### Available Threshold Parameters

The following thresholds can be configured:

| Parameter | Description | Default WARN | Default CRIT |
|-----------|-------------|--------------|--------------|
| Parser success rate | Percentage of successfully parsed logs | <98% | <95% |
| Drop rate | Percentage of dropped requests by bouncers | ≥1% | ≥5% |
| Alerts (1h) | Number of alerts in the last hour | ≥20 | ≥50 |
| Alerts (24h) | Number of alerts in the last 24 hours | ≥100 | ≥500 |
| Top reasons | Number of top scenarios displayed in decisions summary | 5 | - |

## 4. Monitored Metrics

The plugin collects and monitors the following metrics:

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

## 6. Performance Considerations

The plugin executes multiple `cscli` commands per check cycle. To minimize performance impact:

- The default timeout is set to 15 seconds
- Consider increasing the check interval for high-traffic systems
- Use Docker mode if possible, as it may be more efficient than local execution