#!/bin/bash
#
# Copyright 2021, Proofcraft Pty Ltd
#
# SPDX-License-Identifier: BSD-2-Clause
#

# TODO: move elsewhere
echo "::group::Setting up"
# "${GITHUB_WORKSPACE}/microkit/.github/install_ubuntu_deps.sh"

wget -O aarch64-toolchain.tar.gz https://sel4-toolchains.s3.us-east-2.amazonaws.com/arm-gnu-toolchain-12.2.rel1-x86_64-aarch64-none-elf.tar.xz%3Frev%3D28d5199f6db34e5980aae1062e5a6703%26hash%3DF6F5604BC1A2BBAAEAC4F6E98D8DC35B
tar xf aarch64-toolchain.tar.gz
echo "$(pwd)/arm-gnu-toolchain-12.2.rel1-x86_64-aarch64-none-elf/bin" >> $GITHUB_PATH
export PATH="$(pwd)/arm-gnu-toolchain-12.2.rel1-x86_64-aarch64-none-elf/bin":$PATH



echo "::endgroup::"

hw-steps.sh
