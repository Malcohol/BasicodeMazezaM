import wave

from sys import stdout
from argparse import ArgumentParser, FileType
from math import sin, floor, pi

# Basicode constants
shortWaveDuration = 1.0/2400.0
longWaveDuration = 1.0/1200.0
leaderDuration = 5.0

# Constants for the wav files we generate.
sampleWidthInBytes = 1
sampleRate = 44100

class WaveBuilder:
    def __init__(self, wavFile : wave.Wave_write, waveType : str):
        self.samplePeriod = 1.0 / sampleRate
        self.excessTime = 0.0
        self.waveType = waveType
        self.wavFile = wavFile
        self.checksum = 0

    def __writeSingleFrame(self, sample : int):
        self.wavFile.writeframes(sample.to_bytes(1, 'little'))

    def __addWave(self, waveDuration : float):
        d = self.excessTime
        while d < waveDuration:
            if self.waveType == "square":
                self.__writeSingleFrame(255 if ((d / waveDuration) < 0.5) else 0)
            elif self.waveType == "sin":
                angle = 2.0 * pi * (d / waveDuration)
                self.__writeSingleFrame(floor((1.0 + sin(angle)) * 0.5 * 255.99))
            else:
                assert(False)
            d += self.samplePeriod
        self.excessTime = d - waveDuration

    def addByte(self, b : int):
        assert(b >= 0)
        assert(b <= 255)
        self.checksum = self.checksum ^ b
        b = (1 << 10) | (1 << 9) | (b << 1)
        for i in range (0, 11):
            if (b & 1):
                self.__addWave(shortWaveDuration)
                self.__addWave(shortWaveDuration)
            else:
                self.__addWave(longWaveDuration)
            b = b >> 1

    def addLeaderOrTrailer(self):
        count : int = floor(leaderDuration / shortWaveDuration)
        for i in range(0, count):
            self.__addWave(shortWaveDuration)

    def addChecksum(self):
        self.addByte(self.checksum)

parser = ArgumentParser()
parser.add_argument("file", type=FileType("r"))
parser.add_argument("-o", "--output", action="store", required=True)
parser.add_argument("-w", "--wavetype", choices=["square", "sin"], default="square", action="store")
parsedArgs = parser.parse_args()

wavFile = wave.open(parsedArgs.output, "wb")
wavFile.setnchannels(1)
wavFile.setsampwidth(sampleWidthInBytes)
wavFile.setframerate(sampleRate)

prog = parsedArgs.file.read().replace("\r\n", "\r").replace("\n", "\r") + "\r"

wavBuilder = WaveBuilder(wavFile, parsedArgs.wavetype)

wavBuilder.addLeaderOrTrailer()
wavBuilder.addByte(0x80 | 0x02)

for c in prog:
    b : int = ord(c)
    assert(b >= 0x00)
    assert(b <= 0x7f)
    wavBuilder.addByte(0x80 | b)

wavBuilder.addByte(0x80 | 0x03)
wavBuilder.addChecksum()
wavBuilder.addLeaderOrTrailer()
wavFile.close()

