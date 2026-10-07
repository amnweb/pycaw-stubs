# Contributing to pycaw-stubs

The stubs follow typeshed's
[CONTRIBUTING.md](https://github.com/python/typeshed/blob/main/CONTRIBUTING.md)
and [stub style guide](https://typing.readthedocs.io/en/latest/guides/writing_stubs.html).
`stubs/pycaw` uses typeshed's layout, so it can be copied into typeshed as is.

comtypes is untyped, so its types are aliased to `Any`, for example
`_IUnknown: TypeAlias = Any  # actually comtypes.IUnknown`.

## Running the checks

```shell
pip install -r requirements-tests.txt
pre-commit install

ruff check . && black --check . && flake8 .
python scripts/check_metadata.py
pyright -p pyrightconfig.json
pyright -p pyrightconfig.testcases.json
```

Stubtest needs Windows, since pycaw imports comtypes:

```shell
pip install pycaw==20260927
set MYPYPATH=stubs\pycaw
python -m mypy.stubtest pycaw --strict-type-check-only --allowlist stubs\pycaw\@tests\stubtest_allowlist.txt
```

CI runs all of these, plus mypy on Python 3.10 to 3.14.

## Updating for a new pycaw release

1. Set `version` in `stubs/pycaw/METADATA.toml` to the new pycaw version.
2. Fix the `.pyi` files until stubtest passes, and add test cases in
   `stubs/pycaw/@tests/test_cases/` for new or changed APIs.
3. Set `version` in `pyproject.toml` to `<pycaw version>.<YYYYMMDD>`.

For a stubs-only fix, bump just the date part.
