# Contributing to pycaw-stubs

The stubs follow typeshed's
[CONTRIBUTING.md](https://github.com/python/typeshed/blob/main/CONTRIBUTING.md)
and the [stub style guide](https://typing.readthedocs.io/en/latest/guides/writing_stubs.html).
They are laid out like a typeshed distribution, so they can be sent upstream
with little or no change.

## Repository layout

```
stubs/pycaw/                  # same layout as typeshed's stubs/<distribution>/
├── METADATA.toml             # typeshed metadata: upstream version, dependencies, stubtest settings
├── @tests/
│   ├── stubtest_allowlist.txt
│   └── test_cases/           # typeshed-style regression tests (assert_type / "type: ignore")
└── pycaw/                    # the .pyi files, mirroring the pycaw package
pyproject.toml                # builds the PyPI package (stubs/pycaw/pycaw -> pycaw-stubs/)
pyrightconfig*.json, .flake8  # typeshed's checker settings
scripts/check_metadata.py     # keeps METADATA.toml and pyproject.toml consistent
```

comtypes has no `py.typed` marker, so following typeshed's guidance for untyped
dependencies, its types are aliased to `Any` in the stubs, for example
`_IUnknown: TypeAlias = Any  # actually comtypes.IUnknown`.

## Running the checks

```shell
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-tests.txt

ruff check . && black --check . && flake8 .                 # lint and format, as typeshed's pre-commit does
python scripts/check_metadata.py                            # METADATA.toml and pyproject.toml are consistent
pyright -p pyrightconfig.json                               # stubs, typeshed's strict settings
pyright -p pyrightconfig.testcases.json                     # test cases
(cd stubs/pycaw && mypy pycaw --platform win32 --strict --allow-untyped-defs \
  --allow-incomplete-defs --allow-subclassing-any --explicit-package-bases)
pip install . && mypy "stubs/pycaw/@tests/test_cases" --platform win32 --strict \
  --disable-error-code=empty-body --warn-unused-ignores
```

`pre-commit install` sets up the same ruff, black and flake8-pyi hooks typeshed
uses.

[stubtest](https://mypy.readthedocs.io/en/stable/stubtest.html) compares the
stubs with the real pycaw module. pycaw imports comtypes, which works only on
Windows, so run stubtest on Windows (CI runs it on `windows-latest` for Python
3.10 to 3.14):

```shell
pip install pycaw==20260927 -r requirements-tests.txt
set MYPYPATH=stubs\pycaw
python -m mypy.stubtest pycaw --strict-type-check-only --allowlist stubs\pycaw\@tests\stubtest_allowlist.txt
```

## Updating for a new pycaw release

1. Set `version` in `stubs/pycaw/METADATA.toml` to the new pycaw version and
   push. CI's stubtest job installs that pycaw version and lists everything in
   the stubs that no longer matches it.
2. Update the `.pyi` files until stubtest passes, and add test cases in
   `stubs/pycaw/@tests/test_cases/` for new or changed APIs.
3. Set `version` in `pyproject.toml` to `<pycaw version>.<today as YYYYMMDD>`.

CI also type checks pycaw's own examples from that release with pyright.

To release a fix without a new pycaw version, change only the date part of the
version in `pyproject.toml`.

When a pycaw release ships its own `py.typed` with typed COM interfaces, these
stubs are no longer needed: say so in the README and stop publishing.

## Releasing

Releases go to PyPI through
[Trusted Publishing](https://docs.pypi.org/trusted-publishers/), so no API
token is stored in the repository.

One-time setup:

1. On PyPI, add a *pending* trusted publisher (Account settings → Publishing):
   project `pycaw-stubs`, owner `amnweb`, repository `pycaw-stubs`, workflow
   `publish.yml`, environment `pypi`. To try a release first, do the same on
   [TestPyPI](https://test.pypi.org) with environment `testpypi`.
2. In GitHub, create the environments `pypi` and `testpypi` (Settings →
   Environments). Adding required reviewers to `pypi` is recommended.

Each release:

1. Bump the version as described above and merge to `main`.
2. Create a GitHub release with the tag `v<version>`, for example
   `v20260927.20261007`. Publishing the release runs `publish.yml`, which checks
   that the tag matches the package version, builds, and uploads to PyPI.

To try the pipeline without a release, run the *Publish to PyPI* workflow
manually and choose `testpypi`. PyPI never accepts the same version twice.

## Contributing the stubs to typeshed

`stubs/pycaw` can be copied into typeshed's `stubs/` directory as is. Before
opening a pull request there, check that pycaw still ships no `py.typed` file:
typeshed only accepts stubs for packages without their own type information.
