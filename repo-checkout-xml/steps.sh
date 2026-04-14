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

# modification of repo-checkout that looks normal

: ${REPO:="repo"}

# repo expects git to be set up; provide defaults if they don't exist
git config user.name > /dev/null || \
  git config --global user.name "repo"
git config user.email > /dev/null || \
  git config --global user.email "repo@no.mail"
git config color.ui > /dev/null || \
  git config --global color.ui false

echo "Using supplied manifest XML"
TEST_XML="the-test.xml"
echo "${INPUT_XML}" | nl-unescape.sh > ".repo/manifests/${TEST_XML}"
$REPO init -m "${TEST_XML}"

$REPO sync -j 4

repo-util hashes

echo "::endgroup::"
