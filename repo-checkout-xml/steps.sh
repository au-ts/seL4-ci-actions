#!/bin/bash
#
# Copyright 2021, Proofcfraft Pty Ltd
# Copyright 2026, UNSW
#
# SPDX-License-Identifier: BSD-2-Clause
#

set -e

echo "::group::Setting up"

mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
PATH=~/bin:$PATH

pip3 install -U PyGithub

echo "::endgroup::"

echo "::group::Repo checkout"

# uses INPUT_XML
checkout-manifest.sh
fetch-branches.sh

echo "::endgroup::"
