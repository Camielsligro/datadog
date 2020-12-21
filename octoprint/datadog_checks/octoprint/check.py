# After installing the Datadog Agent on your OctoPrint device, create an API
# key from the OctoPrint service, and provide it.
# Drop this file into `/etc/datadog-agent/checks.d` along with an empty file
# named `octoprint.yaml` in `/etc/datadog-agent/conf.d`.  Pass in your
# OctoPrint API key as an instance value like so:
# ```
# instances:
#   - octo_api_key: APIKEYGOESHERE
# ```

# TODO:
# - Refactor Octo HTTP API calls

import logging
import os

import requests

from datadog_checks.base import AgentCheck
from datadog_checks.base.utils.subprocess_output import get_subprocess_output

__version__ = "0.1.2"

hostname = os.popen("hostname").readline().strip()
logging.debug('hostname: %s', hostname)
SERVER = "http://" + hostname
logging.debug('OctoSERVER: %s', SERVER)

TIMEOUT = 10


def __init__():
    logfile = "/var/log/datadog/octoprint.log"
    logdir = os.path.dirname(logfile)
    if not os.path.exists(logfile):
        os.makedirs(logdir)
        open(logfile, 'w')
    logging.basicConfig(filename=logfile, encoding="utf8", level=logging.DEBUG)


class OctoPrintCheck(AgentCheck):
    def get_rpi_core_temp(self):
        if os.path.isfile("/usr/bin/vcgencmd"):
            # temp = os.popen('sudo /usr/bin/vcgencmd measure_temp').readline()
            temp, err, retcode = get_subprocess_output(
                ["/usr/bin/vcgencmd", "measure_temp"], self.log, raise_on_empty_output=True
            )
            # self.log.debug('rpi core temp - temp: %s', temp)
            # self.log.debug('rpi core temp - err: %s', err)
            # self.log.debug('rpi core temp - retcode: %s', retcode)
            temp = temp.replace("temp=", "").replace("'C", "")
            if temp.startswith("VCHI initialization failed"):
                self.log.info(
                    "Unable to get rPi temp.  To resolve, add the 'video' group to the 'dd-agent' user"
                    " by running `sudo usermod -aG video dd-agent`"
                )
                temp = 0.0
        else:
            self.log.info(
                "The command typically used to get the core temperature, /usr/bin/vcgencmd,"
                "is not available on this system."
            )
            temp = 0.0
        return float(temp)

    def seconds_to_minutes(self, seconds):
        sec = seconds
        if not sec:
            return 0
        else:
            return int(sec / 60)

    # Get stats from REST API as json
    def get_job_info(self, server, key, timeout):
        PATH = "/api/job"
        url = server + PATH
        headers = {"X-Api-Key": key, "content-type": "application/json"}
        req = requests.get(url, timeout=timeout, headers=headers)
        return req.json()

    def get_tool_temp(self, server, key, timeout):
        PATH = "/api/printer/tool"
        url = server + PATH
        headers = {"X-Api-Key": key, "content-type": "application/json"}
        req = requests.get(url, timeout=timeout, headers=headers)
        return req.json()

    def get_bed_temp(self, server, key, timeout):
        PATH = "/api/printer/bed"
        url = server + PATH
        headers = {"X-Api-Key": key, "content-type": "application/json"}
        req = requests.get(url, timeout=timeout, headers=headers)
        return req.json()

    def check(self, instance):
        octo_api_key = instance.get('octo_api_key')
        # self.log.info('octo_api_key (from config): %s', octo_api_key)
        # self.log.info('octo_server: %s', SERVER)
        rpi_core_temp = self.get_rpi_core_temp()
        self.gauge("octoprint.rpi_core_temp", rpi_core_temp)

        # get api data
        x = self.get_job_info(SERVER, octo_api_key, TIMEOUT)

        # # Job State
        state = x["state"]
        # States: Printing, Paused, Cancelled, Operational...
        # The proper thing would be a a case/switch statement
        if state == "Operational":
            printer_state = 0
        elif state == "Paused":
            printer_state = 1
        elif state == "Printing":
            printer_state = 2
        else:
            printer_state = -1
        self.gauge("octoprint.printer_state", printer_state)

        # Job File Name
        # job_name = x["job"]["file"]["name"] or ""

        # Print Job Percent Completed and Time Estimate
        est_print_time = self.seconds_to_minutes(x["job"]["estimatedPrintTime"])
        pct_completed = x["progress"]["completion"]
        self.gauge("octoprint.est_print_time", est_print_time)
        self.gauge("octoprint.pct_completed", pct_completed)

        # Print Job Elapsed and Remaining Times
        print_job_time = self.seconds_to_minutes(x["progress"]["printTime"])
        print_job_time_left = self.seconds_to_minutes(x["progress"]["printTimeLeft"])
        self.gauge("octoprint.print_job_time", print_job_time)
        self.gauge("octoprint.print_job_time_left", print_job_time_left)

        # # Extruder Temperatures
        y = self.get_tool_temp(SERVER, octo_api_key, TIMEOUT)
        # print(toolname)
        for key in y.keys():
            toolname = key
            current_tool_temp = y[toolname]["actual"]
            target_tool_temp = y[toolname]["target"]
            self.gauge("octoprint." + toolname + ".current_tool_temp", current_tool_temp)
            self.gauge("octoprint." + toolname + ".target_tool_temp", target_tool_temp)

        # # Bed Temperatures
        z = self.get_bed_temp(SERVER, octo_api_key, TIMEOUT)
        print(z)
        for key in z.keys():
            bedname = key
            current_bed_temp = z[bedname]["actual"]
            target_bed_temp = z[bedname]["target"]
            self.gauge("octoprint." + bedname + ".current_bed_temp", current_bed_temp)
            self.gauge("octoprint." + bedname + ".target_bed_temp", target_bed_temp)
