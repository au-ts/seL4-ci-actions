# Copyright 2021, Proofcraft Pty Ltd
# Copyright 2026, UNSW
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Parse builds.yml and run sel4test hardware builds and runs on each of the build definitions.

Expects seL4-platforms/ to be co-located or otherwise in the PYTHONPATH.
Expects microkit/build_sdk.py to be co-located or otherwise in the PYTHONPATH
"""

from builds import Build, run_build_script, run_builds, load_builds, junit_results
from builds import release_mq_locks, SKIP
from platforms import Platform, gh_output

from pprint import pprint
from typing import List

import json
import os
import sys

def hw_run(manifest_dir: str, build: Build) -> int:
    """Run one hardware test."""

    if build.is_disabled():
        print(f"Test {build.name} disabled, skipping.")
        return SKIP

    script, final = build.hw_run(f"{build.name}")

    return run_build_script(manifest_dir, build, script, final_script=final, junit=False)


def verification_equals_release(build: Build) -> bool:
    """Return whether in this build release and verification settings are equivalent."""

    plat = build.get_platform()
    # TX2 currently still set AArch64SErrorIgnore=ON for release mode
    return plat.arch == 'riscv' or (plat.arch == 'arm' and not plat.name == 'TX2')


def hw_test_filter(build: Build) -> bool:
    plat = build.get_platform()

    if plat.no_hw_build:
        return False

    return True



# If called as main, run all builds from builds.yml
if __name__ == '__main__':
    # builds = load_builds(os.path.dirname(__file__) + "/builds.yml", filter_fun=hw_test_filter)
    builds = []

    if len(sys.argv) > 1 and sys.argv[1] == '--hw':
        sys.exit(run_builds(builds, hw_run))

    if len(sys.argv) > 1 and sys.argv[1] == '--post':
        release_mq_locks(builds)
        sys.exit(0)

    print("unknown action, running hw builds from MICROKIT_SDK")
    sys.exit(run_builds(builds, hw_run))

