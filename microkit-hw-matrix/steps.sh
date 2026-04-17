#!/bin/bash
#
# Copyright 2021, Proofcraft Pty Ltd
#
# SPDX-License-Identifier: BSD-2-Clause
#

# generic steps to invoke hardware builds on the machine queue
# expects a standard `build.py --hw` invocation to work in directory INPUT_ACTION_NAME

set -e

echo "::group::Setting up"
export ACTION_DIR="${SCRIPTS}/.."

# python env
sudo apt-get install -y --no-install-recommends libffi-dev
pip3 install --user "junitparser==3.*" sel4-deps
export PYTHONPATH="${ACTION_DIR}/seL4-platforms"

echo "::endgroup::"

# start builds
python3 "${ACTION_DIR}/${INPUT_ACTION_NAME}/build.py" --matrix
