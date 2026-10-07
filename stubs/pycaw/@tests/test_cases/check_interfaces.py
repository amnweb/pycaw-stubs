from __future__ import annotations

from ctypes import POINTER, _Pointer, cast
from typing_extensions import assert_type

from pycaw.api.audioclient import IAudioClient
from pycaw.api.audioclient.depend import WAVEFORMATEX
from pycaw.api.mmdeviceapi.depend import PROPERTYKEY, PROPVARIANT, IPropertyStore
from pycaw.constants import CLSID_MMDeviceEnumerator, IID_Empty, STGM, EDataFlow, ERole
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioMeterInformation, IMMDevice, IMMDeviceEnumerator

_ = CLSID_MMDeviceEnumerator

enumerator: IMMDeviceEnumerator = AudioUtilities.GetDeviceEnumerator()
device = enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, ERole.eMultimedia.value)
assert_type(device, IMMDevice)
assert_type(device.GetId(), str)
assert_type(device.GetState(), int)
collection = enumerator.EnumAudioEndpoints(EDataFlow.eAll.value, 0xF)
assert_type(collection.GetCount(), int)
assert_type(collection.Item(0), IMMDevice)
assert_type(collection[0], IMMDevice)
assert_type(collection(0), IMMDevice)

# The classic README pattern: Activate + QueryInterface / cast
interface = device.Activate(IAudioEndpointVolume._iid_, 23, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume_ptr = cast(interface, POINTER(IAudioEndpointVolume))
assert_type(volume_ptr, "_Pointer[IAudioEndpointVolume]")

# IAudioEndpointVolume
endpoint = AudioUtilities.GetSpeakers().EndpointVolume
assert_type(endpoint.GetMasterVolumeLevel(), float)
assert_type(endpoint.GetMasterVolumeLevelScalar(), float)
assert_type(endpoint.GetVolumeRange(), tuple[float, float, float])
assert_type(endpoint.GetVolumeStepInfo(), tuple[int, int])
assert_type(endpoint.GetMute(), int)
assert_type(endpoint.GetChannelCount(), int)
assert_type(endpoint.GetChannelVolumeLevelScalar(0), float)
endpoint.SetMasterVolumeLevel(-20.0, None)
endpoint.SetMasterVolumeLevelScalar(0.5, None)
endpoint.SetMute(1, None)
endpoint.SetMute(True, None)
endpoint.SetChannelVolumeLevelScalar(0, 0.5, IID_Empty)
endpoint.VolumeStepUp(None)
endpoint.SetMasterVolumeLevelScalar("0.5", None)  # type: ignore
endpoint.SetMasterVolumeLevelScalar(0.5)  # type: ignore

meter: IAudioMeterInformation = interface.QueryInterface(IAudioMeterInformation)
assert_type(meter.GetPeakValue(), float)

# IAudioClient
client: IAudioClient = device.Activate(IAudioClient._iid_, 23, None)
mix_format = client.GetMixFormat()
assert_type(mix_format, "_Pointer[WAVEFORMATEX]")
assert_type(mix_format.contents.nChannels, int)
assert_type(mix_format.contents.nSamplesPerSec, int)
assert_type(client.GetDevicePeriod(), tuple[int, int])
assert_type(client.GetBufferSize(), int)

# Property store
store = device.OpenPropertyStore(STGM.STGM_READ.value)
assert_type(store, IPropertyStore)
key = store.GetAt(0)
assert_type(key, PROPERTYKEY)
assert_type(key.pid, int)
value = store.GetValue(key)
assert_type(value, PROPVARIANT)
assert_type(value.vt, int)
value.clear()
