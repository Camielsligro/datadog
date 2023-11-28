## Overview

Statsig's feature flag tracking integration enriches your Datadog RUM data with feature gate information, allowing you to measure causality between your product features and your system and performance metrics.

## Setup

### Feature flag tracking setup

Feature flag tracking is available in the RUM Browser SDK. For detailed set up instructions, visit [Getting started with feature flag data in RUM](https://docs.datadoghq.com/real_user_monitoring/guide/setup-feature-flag-data-collection).

1. Update your Browser RUM SDK version to 4.25.0 or above.
2. Initialize the RUM SDK and configure the `enableExperimentalFeatures` initialization parameter with `["feature_flags"]`.
3. Initialize Statsig's SDK (`>= v4.34.0`) and implement the `gateEvaluationCallback` option as shown below:

```js
await statsig.initialize('client-<STATSIG CLIENT KEY>',
  {userID: '<USER ID>'},
  {     
    gateEvaluationCallback: (key, value) => {
      datadogRum.addFeatureFlagEvaluation(key, value);
    }
  }
); 
```

## Support 

Join the [Statsig Slack community](https://join.slack.com/t/statsigcommunity/shared_invite/zt-pbp005hg-VFQOutZhMw5Vu9eWvCro9g) for support on enabling this integration. 