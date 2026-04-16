# Copyright 2021, Proofcraft Pty Ltd
# Copyright 2026, UNSW
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Parse builds.yml and run sel4test hardware builds and runs on each of the build definitions.

Expects seL4-platforms/ to be co-located or otherwise in the PYTHONPATH.
Expects TEST_CASES environment variable to be a JSON.
"""

from builds import Build, Run, run_build_script, run_builds, filtered, get_env_filters
from builds import release_mq_locks, SKIP, build_for_platform
from platforms import Platform

from pathlib import Path
from pprint import pprint
from typing import List, Any, Optional

import copy
import json
import os
import sys


class MicrokitRun(Run):
    def hw_run(self, log):
        build = self.build

        script, final = super().hw_run(log)

        # remove tar command
        assert script[0][0] == "tar"
        script.pop(0)

        return (script, final)


class MicrokitBuild(Build):
    def __init__(self, board: str, config: str, defaults: dict):
        platform = board.upper()

        super().__init__(
            {
                f"{platform}_{config}": {
                    "platform": platform,
                    "microkit_board": board,
                    "microkit_config": config,
                }
            },
            defaults,
        )
        self.update_settings()

        self.files = [Path(f"{self.name}-loader.img").as_posix()]

    def hw_run(self, log):
        return MicrokitRun(self).hw_run(log)


def hw_run(manifest_dir: str, build: MicrokitBuild) -> int:
    """Run one hardware test."""

    if build.is_disabled():
        print(f"Test {build.name} disabled, skipping.")
        return SKIP

    script, final = build.hw_run(f"{build.name}")

    return run_build_script(
        manifest_dir, build, script, final_script=final, junit=False
    )


def hw_test_filter(build: MicrokitBuild) -> bool:
    plat = build.get_platform()

    if plat.no_hw_test:
        return False

    if "debug" not in build.microkit_config:
        return False

    return True


def hw_build(manifest_dir: str, build: MicrokitBuild) -> int:
    """Run one hardware build"""

    MICROKIT_SDK = Path(os.environ["MICROKIT_SDK"])
    GITHUB_WORKSPACE = Path(os.environ["GITHUB_WORKSPACE"])
    BUILD_DIR = GITHUB_WORKSPACE / "builds" / build.name
    microkit_board = build.microkit_board
    microkit_config = build.microkit_config

    script = [
        ["mkdir", "-p", BUILD_DIR.as_posix()],
        [
            "make",
            "-C",
            (MICROKIT_SDK / "example" / "hello").as_posix(),
            f"BUILD_DIR={BUILD_DIR}",
            f"MICROKIT_SDK={MICROKIT_SDK}",
            f"MICROKIT_BOARD={microkit_board}",
            f"MICROKIT_CONFIG={microkit_config}",
        ],
        [
            "cp",
            (BUILD_DIR / "loader.img").as_posix(),
            (GITHUB_WORKSPACE / "{build.name}.loader.img").as_posix(),
        ],
    ]

    return run_build_script(manifest_dir, build, script)


def load_builds_microkit(filter_fun=lambda x: True) -> List[MicrokitBuild]:
    test_cases: list[dict] = json.loads(os.environ["TEST_CASES"])

    env_filters = get_env_filters()

    DEFAULTS = {
        "success": "hello, world",
    }

    builds = []
    for test_case in test_cases:
        platform = test_case["platform"]
        config = test_case["config"]

        build: Optional[MicrokitBuild] = MicrokitBuild(platform, config, DEFAULTS)

        build = build if filter_fun(build) else None
        build = filtered(build, env_filters)
        if build:
            builds.append(build)

    return builds


# If called as main, run all builds from builds.yml
if __name__ == "__main__":
    builds = load_builds_microkit(filter_fun=hw_test_filter)

    if len(sys.argv) > 1 and sys.argv[1] == "--hw":
        sys.exit(run_builds(builds, hw_run))

    if len(sys.argv) > 1 and sys.argv[1] == "--post":
        release_mq_locks(builds)
        sys.exit(0)

    sys.exit(run_builds(builds, hw_build))
