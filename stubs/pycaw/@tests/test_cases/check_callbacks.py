from __future__ import annotations

from ctypes import _Pointer
from typing import Any
from typing_extensions import assert_type, override

from pycaw.api.mmdeviceapi.depend.structures import PROPERTYKEY
from pycaw.callbacks import AudioEndpointVolumeCallback, AudioSessionEvents, AudioSessionNotification, MMNotificationClient
from pycaw.utils import AudioSession, AudioUtilities


class SessionCreated(AudioSessionNotification):
    @override
    def on_session_created(self, new_session: AudioSession) -> None:
        assert_type(new_session.ProcessId, int)


class SessionEvents(AudioSessionEvents):
    @override
    def on_simple_volume_changed(self, new_volume: float, new_mute: int, event_context: _Pointer[Any]) -> None:
        pass

    @override
    def on_channel_volume_changed(
        self, channel_count: int, new_channel_volume_array: list[float], changed_channel: int, event_context: _Pointer[Any]
    ) -> None:
        pass

    @override
    def on_state_changed(self, new_state: str, new_state_id: int) -> None:
        pass

    @override
    def on_session_disconnected(self, disconnect_reason: str, disconnect_reason_id: int) -> None:
        pass


class VolumeCallback(AudioEndpointVolumeCallback):
    @override
    def on_notify(
        self, new_volume: float, new_mute: int, event_context: _Pointer[Any], channels: int, channel_volumes: list[float]
    ) -> None:
        pass


class DeviceMonitor(MMNotificationClient):
    @override
    def on_default_device_changed(self, flow: str, flow_id: int, role: str, role_id: int, default_device_id: str | None) -> None:
        pass

    @override
    def on_device_added(self, added_device_id: str) -> None:
        pass

    @override
    def on_property_value_changed(self, device_id: str, property_struct: PROPERTYKEY, fmtid: Any, pid: int) -> None:
        pass


assert_type(AudioSessionEvents.AudioSessionState, tuple[str, ...])
assert_type(MMNotificationClient.DeviceStates, dict[int, str])

speakers = AudioUtilities.GetSpeakers()
callback = VolumeCallback()
speakers.EndpointVolume.RegisterControlChangeNotify(callback)
speakers.EndpointVolume.UnregisterControlChangeNotify(callback)

for session in AudioUtilities.GetAllSessions():
    session.register_notification(SessionEvents())

manager = AudioUtilities.GetAudioSessionManager()
notification = SessionCreated()
manager.RegisterSessionNotification(notification)
manager.GetSessionEnumerator()
manager.UnregisterSessionNotification(notification)

enumerator = AudioUtilities.GetDeviceEnumerator()
enumerator.RegisterEndpointNotificationCallback(DeviceMonitor())


class MonitorWithInit(MMNotificationClient):
    def __init__(self) -> None:
        super().__init__()
        self.events: list[str] = []


class VolumeCallbackWithInit(AudioEndpointVolumeCallback):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class SessionEventsWithInit(AudioSessionEvents):
    def __init__(self) -> None:
        super().__init__()


class SessionCreatedWithInit(AudioSessionNotification):
    def __init__(self) -> None:
        super().__init__()


MonitorWithInit()
VolumeCallbackWithInit("speakers")
MMNotificationClient(1)  # type: ignore
