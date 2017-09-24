# Neo4j Integration

## Overview

Get metrics from neo4j service in real time to:

* Visualize and monitor neo4j states
* Be notified about neo4j failovers and events.

## Installation

Install the `dd-check-neo4j` package manually or with your favorite configuration manager

## Configuration

Edit the `neo4j.yaml` file to configure the servers to monitor:

* neo4j_url: set to the url of the server (i.e http://ec2-54-85-23-10.compute-1.amazonaws.com)
* port: set to the http port used by neo4j. Default is 7474
* username: set to a valid neo4j username
* password: set to the password for the username
* connect_timeout: setting for the length of time to attempt to connect to the neo4j server
* server_name: set to what should be displayed in DataDog
* version: set to the neo4j versin

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        neo4j
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The neo4j check is compatible with all major platforms
