from ctypes import Structure, Union, _CField, c_long, c_short, c_ulong, c_ulonglong, c_ushort, c_wchar_p
from typing import Any, TypeAlias

_GUID: TypeAlias = Any  # actually comtypes.GUID

class PROPVARIANT_UNION(Union):
    lVal: _CField[c_long, int, int]
    uhVal: _CField[c_ulonglong, int, int]
    boolVal: _CField[c_short, int, int]
    pwszVal: _CField[c_wchar_p, str | None, str | None]
    puuid: _CField[_GUID, _GUID, _GUID]

class PROPVARIANT(Structure):
    vt: _CField[c_ushort, int, int]
    reserved1: _CField[c_ushort, int, int]
    reserved2: _CField[c_ushort, int, int]
    reserved3: _CField[c_ushort, int, int]
    union: _CField[PROPVARIANT_UNION, PROPVARIANT_UNION, PROPVARIANT_UNION]
    def GetValue(self) -> Any: ...  # bool | str | int | None, depending on vt
    def clear(self) -> None: ...

class PROPERTYKEY(Structure):
    fmtid: _CField[_GUID, _GUID, _GUID]
    pid: _CField[c_ulong, int, int]
