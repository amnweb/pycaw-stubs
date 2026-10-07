from enum import Enum, IntEnum
from typing import Any, TypeAlias

_GUID: TypeAlias = Any  # actually comtypes.GUID

IID_Empty: _GUID
CLSID_MMDeviceEnumerator: _GUID
CLSID_CPolicyConfigClient: _GUID

class ERole(Enum):
    eConsole = 0
    eMultimedia = 1
    eCommunications = 2
    ERole_enum_count = 3

class EDataFlow(Enum):
    eRender = 0
    eCapture = 1
    eAll = 2
    EDataFlow_enum_count = 3

class DEVICE_STATE(Enum):
    ACTIVE = 0x00000001
    DISABLED = 0x00000002
    NOTPRESENT = 0x00000004
    UNPLUGGED = 0x00000008
    MASK_ALL = 0x0000000F

class AudioDeviceState(Enum):
    Active = 0x1
    Disabled = 0x2
    NotPresent = 0x4
    Unplugged = 0x8

class STGM(Enum):
    STGM_READ = 0x00000000

class AUDCLNT_SHAREMODE(Enum):
    AUDCLNT_SHAREMODE_SHARED = 0x00000000
    AUDCLNT_SHAREMODE_EXCLUSIVE = 0x00000001

class AudioSessionState(IntEnum):
    Inactive = 0
    Active = 1
    Expired = 2
