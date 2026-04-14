# Copyright 2021, Proofcraft Pty Ltd
# Copyright 2026, UNSW
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Parse builds.yml and run sel4test hardware builds and runs on each of the build definitions.

Expects seL4-platforms/ to be co-located or otherwise in the PYTHONPATH.
Expects TEST_CASES environment variable to be a JSON.
"""

from builds import Build, run_build_script, run_builds, filtered, get_env_filters
from builds import release_mq_locks, SKIP
from platforms import Platform

from pprint import pprint
from typing import List

import json
import os
import sys

# class MicrokitBuild(Build):
#     def get_platform(self) -> Platform:
#         return microkit_platforms


def hw_run(manifest_dir: str, build: Build) -> int:
    """Run one hardware test."""

    if build.is_disabled():
        print(f"Test {build.name} disabled, skipping.")
        return SKIP

    script, final = build.hw_run(f"{build.name}")

    return run_build_script(manifest_dir, build, script, final_script=final, junit=False)




def hw_test_filter(build: Build) -> bool:
    plat = build.get_platform()

    if plat.no_hw_test:
        return False

    return True


def load_builds_microkit(filter_fun=lambda x: True) -> List[Build]:
    test_cases: list[dict] = os.environ["TEST_CASES"]

    env_filters = get_env_filters()

    DEFAULTS = {
        "success": "<TODO>",
    }

    builds = []
    for test_case in test_cases:
        platform = test_case["platform"]
        config = test_case["config"]
        march = test_case["march"]

        build = Build({ "platform" : platform })

        build = build if filter_fun(build) else None
        build = filtered(build, env_filters)
        if build:
            builds.append(build)

    return builds


# If called as main, run all builds from builds.yml
if __name__ == '__main__':
    builds = load_builds_microkit(filter_fun=hw_test_filter)

    if len(sys.argv) > 1 and sys.argv[1] == '--hw':
        sys.exit(run_builds(builds, hw_run))

    if len(sys.argv) > 1 and sys.argv[1] == '--post':
        release_mq_locks(builds)
        sys.exit(0)

    print("unknown action, running hw builds from MICROKIT_SDK")
    sys.exit(run_builds(builds, hw_run))

