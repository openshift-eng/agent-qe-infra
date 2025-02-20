#!/bin/bash

set -o nounset
set -o errexit
set -o pipefail

export AUX_HOST="test"
export IP_STACK="v4"
export NETWORK_TYPE="static"
export INTERNAL_NET_IP="192.168.90.111"
export UNCONFIGURED_INSTALL="false"

jinjanate --import-env= ../agent-config.yaml.j2 inventory.yaml -o "./templated-agent-config.yaml"