# PacketFabric

## Overview

[PacketFabric][1] is a cloud fabric platform that...  
Connecting PacketFabric with Datadog automatically sends metrics data from PacketFabric to Datadog.  

This out-of-the-box integration enables you to:
- Send metrics data to Datadog. Examples of this metrics are `ifd_traffic_rate_metric`, `ifl_traffic_rate_metric`

![metrics dashboard][2]

## Setup

### Installation

OAUTH is used to authenticate the user from datadog to PacketFabric.

On clicking on install, You would be taken to the PacketFabric login page to login and authorize the required permission scope that would be needed by PacketFabric to send your data to Datadog.

![scope permission authorization][3]

The user installing the app i.e. (admin) must have the `api_keys_write` permission, as an api key is generated by Datadog and this is what we would be using to send the metrics data to Datadog.

On completing the installation process, you should be able to access your dashboard in Datadog and see your metrics updated every 15 minutes. 

## Data Collected

### Metrics
This intergrations sends the following metrics data to Datadog
- ifd_traffic_rate_metric
- ifl_traffic_rate_metric

See [metadata.csv][4] for a list of metrics provided by this integration.


## Support

Need help? Contact [packetfabric support](mailto:support@packetfabric.com).

[1]: https://packetfabric.com
[2]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/packetfabric/images/metrics_dashboard.png
[3]: https://raw.githubusercontent.com/DataDog/integrations-extras/master/packetfabric/images/scope_permission.png
[4]: https://github.com/DataDog/integrations-extras/blob/master/packetfabric/metadata.csv