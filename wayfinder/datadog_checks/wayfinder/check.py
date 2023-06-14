from datadog_checks.base import ConfigurationError, OpenMetricsBaseCheckV2


class WayfinderCheck(OpenMetricsBaseCheckV2):
    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'wayfinder'

    def __init__(self, name, init_config, instances):
        super(WayfinderCheck, self).__init__(name, init_config, instances)

        # Use self.instance to read the check configuration
        terranetes_url = self.instance.get("terranetes_controller_url")
        self.terranetes_controller_url = terranetes_url
        if not terranetes_url:
            raise ConfigurationError(
                'Configuration error. Missing URL for Terranenets endpoint. Please fix wayfinder.yaml'
            )

        self.metrics_map = {
            'controller_runtime_reconcile_total': 'controller_runtime_reconcile_total',
            'controller_runtime_webhook_requests_total': 'controller_runtime_webhook_requests.total',
            'configuration_monthly_cost_total': 'configuration_monthly_cost_total',
        }

    def get_default_config(self):
        return {'metrics': self.metrics_map}

    def _http_check(self, url, check_name):
        try:
            response = self.http.get(url)
            response.raise_for_status()
        except Exception as e:
            self.service_check(check_name, self.CRITICAL, message=str(e))
        else:
            if response.status_code == 200:
                self.service_check(check_name, self.OK)
            else:
                self.service_check(check_name, self.WARNING)

    def check(self, instance):
        terranetes_health_endpoint = self.terranetes_controller_url + "/healthz"
        self._http_check(terranetes_health_endpoint, 'terranetes_controller.health')

        super(WayfinderCheck, self).check(instance)
