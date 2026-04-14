#!/bin/bash
#
# Copyright 2021, Proofcfraft Pty Ltd
# Copyright 2026, UNSW
#
# SPDX-License-Identifier: BSD-2-Clause
#

# Script used for microkit-hw composite action

set -e

if [ ! -n "${INPUT_XML}" ];
then
  echo "Invalid use: no supplied XML" >&2
  exit 1
fi
checkout-manifest.sh

fetch-branches.sh
