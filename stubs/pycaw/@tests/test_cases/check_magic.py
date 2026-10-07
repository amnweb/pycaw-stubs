from __future__ import annotations

from typing_extensions import assert_type

from pycaw.constants import AudioSessionState
from pycaw.magic import MagicApp, MagicManager, MagicSession


def on_volume(volume: float) -> None:
    pass


def on_mute(mute: int) -> None:
    pass


def on_state(state: AudioSessionState) -> None:
    pass


app = MagicApp({"msedge.exe"}, volume_callback=on_volume, mute_callback=on_mute, state_callback=on_state)
MagicApp("msedge.exe")
assert_type(app.app_execs, set[str])
assert_type(app.state, "AudioSessionState | None")
assert_type(app.volume, "float | None")
assert_type(app.mute, "int | None")
app.volume = 0.5
app.mute = True
assert_type(app.toggle_mute(), bool)
assert_type(app.step_volume(-0.1), "float | None")
MagicApp({"msedge.exe"}, volume_callback="not callable")  # type: ignore


class MySession(MagicSession):
    def __init__(self) -> None:
        super().__init__(volume_callback=self.custom_volume_callback)
        print(self.magic_root_session.app_exec)

    def custom_volume_callback(self, volume: float) -> None:
        pass


MagicManager.magic_session(MySession)
assert_type(MagicManager.str(), str)
assert_type(MagicManager.magic_activated, "bool | None")
