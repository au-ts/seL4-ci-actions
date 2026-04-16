#!/bin/bash
#
# Copyright 2021, Proofcraft Pty Ltd
#
# SPDX-License-Identifier: BSD-2-Clause
#

set -e
set -x

echo "::group::Setting up"

mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
PATH=~/bin:$PATH

if [ true ]; then
  python3 -m venv .venv
  source .venv/bin/activate
fi

pip3 install -U PyGithub

echo "::endgroup::"

echo "::group::Repo checkout"

export REPO_MANIFEST="${INPUT_MANIFEST}"
export REPO_BRANCH="${INPUT_MANIFEST_BRANCH}"
if [[ "$INPUT_MANIFEST_REPO" =~ "/" ]]; then
  export MANIFEST_URL="https://github.com/${INPUT_MANIFEST_REPO}"
else
  export MANIFEST_URL="https://github.com/seL4/${INPUT_MANIFEST_REPO}"
fi
checkout-manifest.sh

fetch-branches.sh

echo "::endgroup::"

XML="$(repo manifest -r --suppress-upstream-revision | nl-escape.sh)"

if [ -z "${GITHUB_OUTPUT}" ]; then
  echo "Warning: GITHUB_OUTPUT not set"
  GITHUB_OUTPUT="github.output"
fi
echo "xml=${XML}" >> ${GITHUB_OUTPUT}
