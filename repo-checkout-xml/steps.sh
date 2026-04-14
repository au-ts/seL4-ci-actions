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
# repo expects git to be set up; provide defaults if they don't exist
git config user.name > /dev/null || \
  git config --global user.name "repo"
git config user.email > /dev/null || \
  git config --global user.email "repo@no.mail"
git config color.ui > /dev/null || \
  git config --global color.ui false

echo "Using supplied manifest XML"

mkdir .repo_manifest
pushd .repo_manifest
    MANIFEST_GIT=$(pwd)
    git init --quiet
    echo "${INPUT_XML}" | nl-unescape.sh > default.xml
    git add default.TEST_XML
    git commit -m "init"
popd

$REPO init -u "file://${MANIFEST_GIT}/"

$REPO sync -j 4

# fetch tags
$REPO forall -c git fetch --tags

repo-util hashes

echo "::endgroup::"
