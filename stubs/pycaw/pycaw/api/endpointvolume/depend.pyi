from ctypes import Array, Structure, _CField, _Pointer, c_float, c_long, c_uint
from typing import Any, TypeAlias

_GUID: TypeAlias = Any  # actually comtypes.GUID

class AUDIO_VOLUME_NOTIFICATION_DATA(Structure):
    guidEventContext: _CField[_GUID, _GUID, _GUID]
    bMuted: _CField[c_long, int, int]
    fMasterVolume: _CField[c_float, float, float]
    nChannels: _CField[c_uint, int, int]
    afChannelVolumes: _CField[Array[c_float], Array[c_float], Array[c_float]]

PAUDIO_VOLUME_NOTIFICATION_DATA: TypeAlias = _Pointer[AUDIO_VOLUME_NOTIFICATION_DATA]
