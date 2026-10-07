import builtins
from collections.abc import Callable, Iterable
from ctypes import _Pointer
from logging import Logger
from typing import Any, Concatenate, ParamSpec, TypeAlias, TypeVar
from typing_extensions import Self

from pycaw.api.audiopolicy import IAudioSessionControl
from pycaw.constants import AudioSessionState

__all__ = ("MagicManager", "MagicApp", "MagicSession")

_GUID: TypeAlias = Any  # actually comtypes.GUID
_COMObject: TypeAlias = Any  # actually comtypes.COMObject

_S = TypeVar("_S")
_P = ParamSpec("_P")
_R = TypeVar("_R")

log: Logger

class MagicManager(_COMObject):
    magic_activated: bool | None
    magic_root_sessions: dict[int, _MagicRootSession]
    expired_magic_root_sessions: set[_MagicRootSession]
    iid_count: int
    magic_apps: set[MagicApp]
    MagicSessionConfigured: tuple[type[MagicSession], tuple[Any, ...], dict[builtins.str, Any]] | None
    magic_sessions: dict[int, MagicSession]
    @classmethod
    def str(cls) -> builtins.str: ...
    @classmethod
    def activate_magic(cls) -> None: ...
    @classmethod
    def OnSessionCreated(cls, ctl: IAudioSessionControl) -> None: ...
    @classmethod
    def magic_session(cls, MagicSessionClass: type[MagicSession], *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def add_magic_app(cls, magic_app: MagicApp, app_execs: Iterable[builtins.str]) -> None: ...
    @classmethod
    def remove_session(cls, iid: int, magic_app: MagicApp | None = None) -> None: ...
    @classmethod
    def empty_trash(cls) -> None: ...
    @classmethod
    def clean_up(cls) -> None: ...
    @classmethod
    def unregister_all(cls) -> None: ...

def for_session_in_sessions(
    func: Callable[Concatenate[_S, _MagicRootSession, _P], _R],
) -> Callable[Concatenate[_S, _P], _R | None]: ...

class _MagicAudioControl:
    def toggle_mute(self) -> bool: ...
    def step_volume(self, step: float = 0.1) -> float | None: ...

class MagicApp(_MagicAudioControl):
    guid: _Pointer[_GUID]
    app_execs: set[str]
    magic_root_sessions: dict[int, _MagicRootSession]
    volume_callback: Callable[[float], object] | None
    mute_callback: Callable[[int], object] | None
    state_callback: Callable[[AudioSessionState], object] | None
    session_callback: Callable[[_MagicRootSession], object] | None
    advanced_volume_callback: Callable[[float, _MagicGuidCompare], object] | None
    advanced_mute_callback: Callable[[int, _MagicGuidCompare], object] | None
    def __init__(
        self,
        app_execs: str | Iterable[str],
        volume_callback: Callable[[float], object] | None = None,
        advanced_volume_callback: Callable[[float, _MagicGuidCompare], object] | None = None,
        mute_callback: Callable[[int], object] | None = None,
        advanced_mute_callback: Callable[[int, _MagicGuidCompare], object] | None = None,
        state_callback: Callable[[AudioSessionState], object] | None = None,
        session_callback: Callable[[_MagicRootSession], object] | None = None,
    ) -> None: ...
    def add_magic_root_session(self, iid: int, magic_root_session: _MagicRootSession) -> None: ...
    @property
    def state(self) -> AudioSessionState | None: ...

    @property
    def volume(self) -> float | None: ...
    @volume.setter
    def volume(self, volume: float) -> None: ...

    @property
    def mute(self) -> int | None: ...
    @mute.setter
    def mute(self, mute: int) -> None: ...

class MagicSession(_MagicAudioControl):
    guid: _Pointer[_GUID]
    magic_root_session: _MagicRootSession
    volume_callback: Callable[[float], object] | None
    mute_callback: Callable[[int], object] | None
    state_callback: Callable[[AudioSessionState], object] | None
    advanced_volume_callback: Callable[[float, _MagicGuidCompare], object] | None
    advanced_mute_callback: Callable[[int, _MagicGuidCompare], object] | None
    def __init__(
        self,
        volume_callback: Callable[[float], object] | None = None,
        advanced_volume_callback: Callable[[float, _MagicGuidCompare], object] | None = None,
        mute_callback: Callable[[int], object] | None = None,
        advanced_mute_callback: Callable[[int, _MagicGuidCompare], object] | None = None,
        state_callback: Callable[[AudioSessionState], object] | None = None,
    ) -> None: ...
    @classmethod
    def initialize(cls, new_magic_root_session: _MagicRootSession, *args: Any, **kwargs: Any) -> Self: ...
    @property
    def state(self) -> AudioSessionState: ...

    @property
    def volume(self) -> float | None: ...
    @volume.setter
    def volume(self, volume: float) -> None: ...

    @property
    def mute(self) -> int | None: ...
    @mute.setter
    def mute(self, mute: int) -> None: ...

class _MagicGuidCompare:
    master: _Pointer[_GUID]
    changer: _Pointer[_GUID]
    compare: bool
    def __init__(self, master_guid: _Pointer[_GUID], changer_guid: _Pointer[_GUID]) -> None: ...
    def __bool__(self) -> bool: ...

class _MagicRootSession(_COMObject):
    app_exec: str | None
    magic_manager: type[MagicManager]
    iid: int
    magic_app: MagicApp | None
    magic_session: MagicSession | None
    volume: float | None
    mute: int | None
    state: AudioSessionState
    pid: int
    def __init__(self, ctl: IAudioSessionControl, iid: int, magic_manager: type[MagicManager]) -> None: ...
    def use_magic_app(self, magic_app: MagicApp) -> None: ...
    def use_magic_session(self, magic_session: MagicSession) -> None: ...
    def OnSimpleVolumeChanged(self, new_volume: float, new_mute: int, event_context: _Pointer[_GUID]) -> None: ...
    def OnStateChanged(self, new_state_id: int) -> None: ...
    def register_notification(self) -> None: ...
    def unregister_notification(self) -> None: ...
