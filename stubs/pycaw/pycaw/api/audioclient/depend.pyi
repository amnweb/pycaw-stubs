from ctypes import Structure, _CField, c_ulong, c_ushort

class WAVEFORMATEX(Structure):
    wFormatTag: _CField[c_ushort, int, int]
    nChannels: _CField[c_ushort, int, int]
    nSamplesPerSec: _CField[c_ulong, int, int]
    nAvgBytesPerSec: _CField[c_ulong, int, int]
    nBlockAlign: _CField[c_ushort, int, int]
    wBitsPerSample: _CField[c_ushort, int, int]
    cbSize: _CField[c_ushort, int, int]
