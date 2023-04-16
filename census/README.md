# Agent Check: Census

## Overview

[Census][1] is a reverse ETL platform that turns your data warehouse into a hub for marketing and business operations, empowering teams with trustworthy and actionable data. Sync data from a source of truth like a data warehouse to a system of actions like a CRM, advertising platform, or other SaaS app to operationalize data.

Census integrates with Datadog to provide developers the ability to monitor their Census workflows and track the number of successful and failed syncs. This integration sends [metrics](#metrics) and events to Datadog from Census.

## Requirements

A Census Platform tier (or higher) subscription is required to enable this integration.

## Setup

1. Login to your [Census account][2].
2. Navigate to the Census workspace that you wish to connect to your Datadog account.
3. Go to the workspace settings tab, and click on **Configure** on the Datadog tile.
4. Click on **Connect** to connect to your Datadog account through OAuth2.
5. Return to Datadog and open the out-of-the-box Census dashboard.

### Validation

Execute a sync on your Census workspace, and check for the corresponding metrics and events on the Census dashboard in your Datadog account. Events and metrics for a sync may take up to a couple of minutes to be transmitted to Datadog after sync completion.

## Data Collected

### Metrics

See [metadata.csv][3] for a list of metrics provided by this check.

### Service Checks

Census does not include any service checks.

### Events

This integration sends sync completion events to Datadog.

## Troubleshooting

Need help? Contact [Datadog support][4].

[1]: https://www.getcensus.com/
[2]: https://app.getcensus.com/
[3]: https://github.com/DataDog/integrations-extras/blob/master/census/metadata.csv
[4]: https://docs.datadoghq.com/help/
