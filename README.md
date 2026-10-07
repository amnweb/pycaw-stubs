# pycaw-stubs

Type stubs for [pycaw](https://github.com/AndreMiras/pycaw) (Python Core Audio
Windows Library), so that pyright, mypy, and other type checkers understand its
API instead of reporting errors such as:

```
error: "GetMasterVolumeLevelScalar" is not a known attribute of ...
error: "EndpointVolume" is not a known attribute of "None" (reportOptionalMemberAccess)
```

pycaw creates its COM interface methods at runtime, so type checkers cannot
see them in its source code. These stubs declare those methods, along with the
`AudioUtilities`, `AudioDevice`, `AudioSession`, callback and `magic` APIs.

This is an independent project, not part of pycaw.

## Installation

```shell
pip install pycaw-stubs
```

Type checkers pick the stubs up automatically; no configuration is needed.

```python
from pycaw.pycaw import AudioUtilities

volume = AudioUtilities.GetSpeakers().EndpointVolume
level = volume.GetMasterVolumeLevelScalar()  # float
low, high, step = volume.GetVolumeRange()  # tuple[float, float, float]
volume.SetMasterVolumeLevelScalar(0.5, None)

for session in AudioUtilities.GetAllSessions():
    if session.Process is not None:  # psutil.Process | None
        print(session.Process.name(), session.SimpleAudioVolume.GetMasterVolume())
```

The stubs work with Python 3.10 and later, in both standard and strict mode of
pyright and mypy.

## Versions

The version number is `<pycaw version>.<stub release date>`. For example,
`pycaw-stubs 20260927.20261007` describes `pycaw 20260927`. Install the stubs
whose first part matches your pycaw version where possible.

## Limitations

comtypes, which pycaw is built on, has no type information. Its types
(`IUnknown`, `GUID`, `COMObject`) are therefore treated as `Any`:

* Methods that pycaw declares, such as `GetMasterVolumeLevelScalar()`, are
  fully typed.
* Methods that come from comtypes, such as `QueryInterface()`, `AddRef()` and
  `Release()`, are accepted but return `Any`. With `mypy --strict`, returning
  such a value directly from a typed function reports `no-any-return`; assign
  it to an annotated variable first:

  ```python
  volume: IAudioEndpointVolume = interface.QueryInterface(IAudioEndpointVolume)
  ```

  The typed helpers, such as `AudioUtilities.GetSpeakers().EndpointVolume`,
  avoid this.
* If your own code imports comtypes, pyright's strict mode reports
  `Stub file not found for "comtypes"`. That message is about comtypes, not
  these stubs.

## Contributing

Bug reports and fixes are welcome at
[github.com/amnweb/pycaw-stubs](https://github.com/amnweb/pycaw-stubs/issues).
See [CONTRIBUTING.md](https://github.com/amnweb/pycaw-stubs/blob/main/CONTRIBUTING.md)
for how to run the checks and update the stubs.

## License

MIT, see [LICENSE](https://github.com/amnweb/pycaw-stubs/blob/main/LICENSE).
pycaw itself is MIT-licensed by Andre Miras.
