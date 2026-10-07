from __future__ import annotations

import psutil
from typing_extensions import assert_type

from pycaw.api.audioclient import IChannelAudioVolume, ISimpleAudioVolume
from pycaw.api.audiopolicy import IAudioSessionControl2, IAudioSessionManager2
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.api.mmdeviceapi import IMMDevice, IMMDeviceEnumerator
from pycaw.constants import AudioDeviceState, ERole
from pycaw.utils import AudioDevice, AudioSession, AudioUtilities

# AudioUtilities
speakers = AudioUtilities.GetSpeakers()
assert_type(speakers, AudioDevice)
assert_type(AudioUtilities.GetMicrophone(), IMMDevice)
assert_type(AudioUtilities.GetAudioSessionManager(), IAudioSessionManager2)
assert_type(AudioUtilities.GetAllSessions(), list[AudioSession])
assert_type(AudioUtilities.GetProcessSession(123), "AudioSession | None")
assert_type(AudioUtilities.GetAllDevices(), list[AudioDevice])
assert_type(AudioUtilities.GetAllDevices(data_flow=0, device_state=1), list[AudioDevice])
assert_type(AudioUtilities.GetDeviceEnumerator(), IMMDeviceEnumerator)
assert_type(AudioUtilities.CreateDevice(None), None)
assert_type(AudioUtilities.CreateDevice(AudioUtilities.GetMicrophone()), AudioDevice)
assert_type(AudioUtilities.GetEndpointDataFlow("device-id"), str)
assert_type(AudioUtilities.GetEndpointDataFlow("device-id", 0), str)
assert_type(AudioUtilities.GetEndpointDataFlow("device-id", 1), int)


def data_flow(output_type: int) -> None:
    assert_type(AudioUtilities.GetEndpointDataFlow("device-id", output_type), "str | int")


AudioUtilities.SetDefaultDevice("device-id")
AudioUtilities.SetDefaultDevice("device-id", [ERole.eConsole, ERole.eMultimedia])
AudioUtilities.SetDefaultDevice("device-id", [0])  # type: ignore

# AudioDevice
assert_type(speakers.id, str)
assert_type(speakers.state, AudioDeviceState)
assert_type(speakers.FriendlyName, "str | None")
assert_type(speakers.EndpointVolume, IAudioEndpointVolume)
assert_type(speakers.AudioSessionManager, IAudioSessionManager2)
assert_type(speakers.volume_percent, float)
speakers.volume_percent = 50
speakers.volume_percent = 12.5
speakers.volume_percent = "50"  # type: ignore

# AudioSession
for session in AudioUtilities.GetAllSessions():
    assert_type(session.Process, "psutil.Process | None")
    assert_type(session.ProcessId, int)
    assert_type(session.Identifier, str)
    assert_type(session.InstanceIdentifier, str)
    assert_type(session.State, int)
    assert_type(session.DisplayName, str)
    assert_type(session.IconPath, str)
    assert_type(session.SimpleAudioVolume, ISimpleAudioVolume)
    assert_type(session.channelAudioVolume(), IChannelAudioVolume)
    session.DisplayName = "name"
    session.IconPath = "path"
    session.unregister_notification()


def wrap(ctl: IAudioSessionControl2) -> AudioSession:
    return AudioSession(ctl)
