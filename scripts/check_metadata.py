"""Validate stubs/pycaw/METADATA.toml and keep pyproject.toml in sync with it.

Usage: python scripts/check_metadata.py [RELEASE_TAG]

When RELEASE_TAG (e.g. "v20260927.20261007") is given, it must match the
package version in pyproject.toml.
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "stubs" / "pycaw" / "METADATA.toml"
PYPROJECT = ROOT / "pyproject.toml"

# Keys documented in typeshed's CONTRIBUTING.md.
METADATA_KEYS = {
    "version",
    "dependencies",
    "optional-dependencies",
    "extra-description",
    "stub-distribution",
    "upstream-repository",
    "obsolete-since",
    "no-longer-updated",
    "upload",
    "partial-stub",
    "requires-python",
    "tool",
}
STUBTEST_KEYS = {
    "skip",
    "ignore-missing-stub",
    "stubtest-dependencies",
    "apt-dependencies",
    "brew-dependencies",
    "choco-dependencies",
    "extras",
    "supported-platforms",
    "ci-platforms",
    "mypy-plugins",
    "mypy-plugins-config",
    "install-environment",
}


def main() -> int:
    metadata = tomllib.loads(METADATA.read_text(encoding="utf-8"))
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    errors: list[str] = []

    if unknown := set(metadata) - METADATA_KEYS:
        errors.append(f"Unknown METADATA.toml keys: {sorted(unknown)}")
    if unknown := set(metadata.get("tool", {}).get("stubtest", {})) - STUBTEST_KEYS:
        errors.append(f"Unknown [tool.stubtest] keys: {sorted(unknown)}")

    upstream_version = metadata.get("version")
    if not isinstance(upstream_version, str) or not upstream_version:
        errors.append("METADATA.toml must define a 'version' string")
        upstream_version = ""
    version = project["version"]
    if not re.fullmatch(re.escape(upstream_version) + r"\.\d{8}", version):
        errors.append(
            f"pyproject.toml version {version!r} must be '<METADATA version>.<YYYYMMDD>', "
            f"i.e. start with {upstream_version!r}"
        )

    if sorted(project.get("dependencies", [])) != sorted(metadata.get("dependencies", [])):
        errors.append("pyproject.toml [project] dependencies must match METADATA.toml dependencies")

    if len(sys.argv) > 1:
        tag = sys.argv[1].removeprefix("refs/tags/")
        if tag.removeprefix("v") != version:
            errors.append(f"Release tag {tag!r} does not match package version {version!r}")

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if not errors:
        print(f"OK: pycaw-stubs {version} for pycaw {upstream_version}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
